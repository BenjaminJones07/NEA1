from typing import Optional, Type
import auth, shapes, random

# Display choices and request input until valid
def nChoice(*args: str) -> int:
    [print(f"{x+1}) {s}") for (x,s) in enumerate(args)]
    while True:
        if not (choosed := input("Choice: ")).isdigit(): continue
        if 0 <= int(choosed) - 1 and int(choosed) - 1 < len(args):
            print()
            return int(choosed)

# Display a choice with a randomly placed correct answer and an exit message as the last choice, return score on correct, None on exit
def randChoice(shape: Type[shapes.baseShape], end: str) -> Optional[int]:
    print(prompt := f"What is the area of a {str(shape).lower()}?")
    argsList = shape.wrongAreas()
    argsList.insert(place := random.randint(0, len(argsList)), shape.getArea())

    match nChoice(*argsList, end) - 1:
        case x if x == len(argsList):
            return None
        case x if x == place:
            return 2
    
    print(f"Incorrect, {(lambda s: s[:1].lower() + s[1:] if s else '')(shape.formula())}")
    choice = x
    while choice == x:
        print(prompt)
        choice = nChoice(*argsList, end)-1 # Get choice
        if choice == x: print("You've already chosen that!")
    return int(choice == place)

def run() -> authio.User:
    uh, user = auth.UserHandler(), None # Initialize user handler and user variable
    
    # User chooses to login or register
    authFuncs = [uh.login, uh.reg]
    authFunc = authFuncs[nChoice("Login", "Register") - 1]
    
    # Loop until valid login/registration
    while not isinstance(user, authio.User):
        user = authFunc(input("Username: "), input("Password: "))
        if isinstance(user, str): print(user)
        
    print()
    
    # User now exists, and must continue to exist for the duration of the function
    
    print("Pick a shape to practice!")
    shape, score = shapes.shapesArr[nChoice("Circle", "Rectangle", "Triangle") - 1](), 0 # Initialize chosen shape and score count
    
    while True:
        shape.generate() # Generate random dimensions for shape
        
        match randChoice(shape, "Exit"):
            case None: # User chose to exit
                break
            case x: # User did not choose to exit
                score += x # Add to score
                if x == 0: print(f"Incorrect, the answer was {shape.getArea()}") # Print correct answer on 0 score
                else: print("Correct!")

        print()
        
    # Save and print score
    user.addScore(score)
    print(f"Your score for this session was {score}!")
    
    # Return user for score access in menu
    return user