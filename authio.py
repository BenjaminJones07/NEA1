# Imports
from typing import List, Optional, Union, ForwardRef, Dict
import os, json, hashlib

# Helper functions
def userFormat(pw: str, scores: List[int] = []) -> Dict[str, Union[str, List[int]]]:
    return {"pw": pw, "scores": scores}

def strength(pw: str) -> bool:
    return True

def hashStr(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# Exceptions
class FileNotExist(Exception):
    def __init__(self): super.__init__("The file does not exist.")
class FileNotSupported(Exception):
    def __init__(self): super.__init__("The file is not of a supported type (JSON).")
class SaveError(Exception):
    def __init__(self): super.__init__("The user object could not be saved.")

# Classes
class FSIO:
    def __init__(self, filename: str = "test.json") -> None:
        if not filename[-5:] == ".json": raise FileNotSupported
        if not os.path.isfile(filename): raise FileNotExist
        self.data, self.file = json.load(open(filename)), filename

    def save(self) -> bool:
        if not os.path.isfile(self.file): return False
        json.dump(self.data, open(self.file, "w"), indent=4)
        return True

    def userExists(self, un: str) -> bool:
        return un in self.data

    def getUser(self, un: str) -> Optional[ForwardRef("User")]:
        return User(un, self.data[un], fs=self) if self.userExists(un) else None

    def updateUser(self, un: str, obj: Dict[str, Union[str, List[int]]]) -> bool:
        self.data[un] = obj
        return self.save()

    def addUser(self, un: str, obj: Dict[str, Union[str, List[int]]]) -> Optional[ForwardRef("User")]:
        if self.userExists(un): return None
        if not self.updateUser(un, obj): return None
        return self.getUser(un)

class User:
    def __init__(self, un: str, obj: Dict[str, Union[str, List[int]]], fs: FSIO) -> None:
        self.un, self.pw, self._scores, self._fs = un, obj["pw"], obj["scores"], fs

    def saveUsr(self) -> None:
        if not self._fs.updateUser(self.un, userFormat(self.pw, self._scores)): raise SaveError

    def getScores(self) -> List[int]:
        return self._scores

    def addScore(self, score: int) -> List[int]:
        self.scores.append(score)
        self.saveUsr()

    def __str__(self) -> str:
        return f"User({self.un=}, {self._scores=})"

class UserHandler:
    def __init__(self, fs: FSIO = FSIO()) -> None:
        self.fs = fs

    def reg(self, un: str, pw: str) -> Optional[User]:
        if 0 in [len(un), len(pw)] or not strength(pw): return None # len(un) == 0 or len(pw) == 0
        return self.fs.addUser(un, userFormat(hashStr(pw)))

    def login(self, un: str, pw: str) -> Optional[User]: #TODO
        if 0 in [len(un), len(pw)] or not (usr := self.fs.getUser(un)): return None
        if not usr.pw == hashStr(pw): return None
        return usr


if __name__ == "__main__":
    uh = UserHandler()

    print(uh.login("Ben", "Nah"))
    print(uh.login("Ben", "Test"))
    print(uh.login("Test", "Nah"))

    print(uh.reg("Ben", "Test"))
    print(uh.reg("Test", "Nah"))