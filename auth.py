# Imports
from typing import List, Optional, Set, Union, ForwardRef, Dict
import os, json, hashlib

#Globals
SYMBOLS = "~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/"
upper = ''.join([chr(x + 97) for x in range(26)])
nums = ''.join([str(x) for x in range(10)])

# Exceptions
class FileNotSupported(Exception):
    def __init__(self): super.__init__("The file is not of a supported type (JSON).")
class SaveError(Exception):
    def __init__(self): super.__init__("The user object could not be saved.")

# Helper functions
def userFormat(pw: str, scores: List[int] = []) -> Dict[str, Union[str, List[int]]]:
    return {"pw": pw, "scores": scores}

# Ensures data created by each intersection is removed line-by-line
def intersectionCheck(pwSet: Set[chr], check: Union[Set[chr], str]) -> bool:
    return not pwSet.intersection(check)

def strength(pw: str) -> Union[str, bool]:
    pw_asSet = set(pw)
    if len(pw) < 8: return "Password needs at least 8 characters"
    if intersectionCheck(pw_asSet, upper): return "Password needs at least 1 uppercase letter"
    if intersectionCheck(pw_asSet, nums): return "Password needs at least 1 number"
    if intersectionCheck(pw_asSet, SYMBOLS): return "Password needs at least 1 symbol"
    return True

def hashStr(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# Classes
class FSIO:
    def __init__(self, filename: str = "accts.json") -> None:
        if not filename[-5:] == ".json": raise FileNotSupported
        if not os.path.isfile(filename):
            with open(filename, "w") as f: f.write("{}")
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

    def __repr__(self) -> str:
        return f"FSIO({self.data=}, {self.file=})"

class User:
    def __init__(self, un: str, obj: Dict[str, Union[str, List[int]]], fs: FSIO) -> None:
        self.un, self.pw, self._scores, self._fs = un, obj["pw"], obj["scores"], fs

    def saveUsr(self) -> None:
        if not self._fs.updateUser(self.un, userFormat(self.pw, self._scores)): raise SaveError

    def getScores(self) -> List[int]:
        return self._scores

    def addScore(self, score: int) -> None:
        self._scores.append(score)
        self.saveUsr()

    def __repr__(self) -> str:
        return f"User({self.un=}, {self.pw=}, {self._scores=}, self._fs=`{self._fs}`)"

class UserHandler:
    def __init__(self, fs: FSIO = FSIO()) -> None: self.fs = fs

    def reg(self, un: str, pw: str) -> Union[str, User]:
        if 0 in [len(un), len(pw)]: return "One or more input was blank"
        if self.fs.userExists(un): return "User already exists"
        if not (issue := strength(pw)) is True: return issue
        return self.fs.addUser(un, userFormat(hashStr(pw)))

    def login(self, un: str, pw: str) -> Union[str, User]:
        if 0 in [len(un), len(pw)]: return "One or more input was blank"
        if not (usr := self.fs.getUser(un)): return "User does not exist"
        if not usr.pw == hashStr(pw): return "Incorrect password"
        return usr
