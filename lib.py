from typing import Optional
import authio, shapeslib, random

# Display choices and request input until valid
def nChoice(*args: str) -> int:
    [print(f"{x+1}) {s}") for (x,s) in enumerate(args)]
    while True:
        if not (choosed := input("Choice: ")).isdigit(): continue
        if not int(choosed) - 1 >= 0 and int(choosed) - 1 < len(args): continue
        return int(choosed)

# Display a choice with a randomly placed correct answer and an exit message as the last choice, return True on correct, False on wrong, None on exit
def randChoice(correct: str, end: str, *args: str) -> Optional[bool]: 
    argsList = list(*args)
    argsList.insert(place := random.randint(0, len(argsList)), correct)
    choice = nChoice(*argsList, end)-1
    return (place == choice) if not choice == len(argsList) else None

def run() -> authio.User:
    uh, user = authio.UserHandler(), None
    
    match nChoice("Login", "Register"):
        case 1:
            authFunc, output = uh.login, "Username or password incorrect."
        case 2:
            authFunc, output = uh.reg, "User already exists."
    
    print()
    
    while not user:
        user = authFunc(input("Username: "), input("Password: "))
        if not user: print(output)
        
    print()
    
    # User now exists, and must continue to exist for the duration of the function
    
    print("Pick a shape to practice!")
    shape = shapeslib.shapesArr[nChoice("Circle", "Rectangle", "Triangle") - 1]()
    
    print()
    
    while True:
        shape.generate()
        print(f"What is the area of a {str(shape).lower()}?")
        
        match randChoice(shape.getArea(), "Exit", shape.wrongAreas()):
            case None:
                break
            case True:
                print("Well done!")
            case False:
                print("Nope")
            
        print()
        
    print()
    
    return user