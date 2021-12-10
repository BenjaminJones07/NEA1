import os, json

class DBFileNotExist(Exception):
    def __init__(self): super.__init__("The database file does not exist")
class FileNotSupported(Exception):
    def __init__(self): super.__init__("The database is not of a supported type")

class DB:
    def __init__(self, filename):
        if not filename[-5:] == ".json": raise FileNotSupported
        if not os.path.isfile(filename): raise DBFileNotExist
        self.data, self.file = json.load(open(filename)), filename

    def save(self): json.dump(self.data, open(self.file, "w"))

    userExists = lambda self, un: un in self.data["users"]
    userAuth = lambda self, un, pw: self.data["users"][un]["pw"] == pw if self.userExists(un) else False
    def addUser(self, un, pw):
        if not pw or pw == "" or self.userExists(un): return False
        self.data["users"][un]["pw"] = pw
        self.save()
        return True

if __name__ == "__main__":
    db = DB("test.json")
    print(db.userExists("Ben"))
    print(db.userExists("Test"))
    print(db.userAuth("Ben", "Test"))
    print(db.userAuth("Ben", "Nah"))