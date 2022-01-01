from typing import Optional, Type, Tuple
import authio, shapeslib, random
import PySimpleGUI as sg

def run(user: Optional[authio.User] = None) -> Optional[Tuple[authio.User, int]]:
    layout = [ # Authentication window layout
        [
            sg.Text("Login or Register")
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text(key="-OUT-")
        ],
        [
            sg.In(size=(20, 1), enable_events=True, default_text="Username", key="-UN-"),
            sg.In(size=(20, 1), enable_events=True, default_text="Password", key="-PW-")
        ],
        [
            sg.Button("Login"),
            sg.Button("Register")
        ]
    ]
    
    window = sg.Window("Area Trainer", layout)
    
    uh = authio.UserHandler() # Initialize user handler
    
    while not isinstance(user, authio.User):
        event, values = window.read()
        
        # User chooses to login or register
        
        authFuncs = {"Login": uh.login, "Register": uh.reg}
        
        if event == sg.WIN_CLOSED: # Check for window close
            window.close()
            return None
        
        elif event in authFuncs:
            user = authFuncs[event](values["-UN-"], values["-PW-"])
            if isinstance(user, str): window["-OUT-"].update(user)
        
    window.close() # Authentication complete
    
    # User now exists, and must continue to exist for the duration of the function
    
    layout = [
        [
            sg.Text("Pick a shape to practice!")
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Listbox(
                values = list(shapeslib.shapesArr.keys()), enable_events=True, size=(40, 20), key="-SHAPES-"
            )
        ]
    ]
    
    window = sg.Window("Area Trainer", layout)
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED: # Check for window close
            window.close()
            return None
        
        elif event == "-SHAPES-":
            shape, score = shapeslib.shapesArr[values["-SHAPES-"][0]](), 0
            break
        
    window.close()
    
    # A shape has been chosen and initialized
    
    layout = [
        [
            sg.Text(key="-PROMPT-")
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text(key="-FEEDBACK-")
        ],
        [
            sg.Listbox(
                values = [], enable_events=True, size=(10, 5), key="-AREAS-"
            )
        ],
        [
            sg.Button("Quit")
        ]
    ]
    
    window = sg.Window("Area Trainer", layout, finalize=True, element_justification='c')
    
    done = False
    while not done:
        points, chosen, _ = 2, list(), shape.generate() # Generate random dimensions for shape
        (areas := shape.wrongAreas()).insert(random.randint(0, len(areas)), area := shape.getArea())
        
        window["-PROMPT-"].update(f"What is the area of a {str(shape).lower()}")
        window["-AREAS-"].update(areas)
        
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED: # Check for window close
                window.close()
                return None
            
            elif event == "-AREAS-":
                value = values["-AREAS-"][0]
                
                if value == area:
                    window["-FEEDBACK-"].update("Correct")
                    score += points
                    break
                
                if value in chosen:
                    window["-FEEDBACK-"].update("You've already chosen that!")
                    continue
                
                points, _ = points - 1, chosen.append(value)
                
                if points == 0:
                    window["-FEEDBACK-"].update(f"Incorrect, the answer was {area}") # Print correct answer on 0 score
                    break
                
                window["-FEEDBACK-"].update(f"Incorrect, {(lambda s: s[:1].lower() + s[1:] if s else '')(shape.wrong())}")
                
            elif event == "Quit":
                done = True
                window.close()
                break
        
    # Save and print score
    user.addScore(score)
    
    # Return user for score access in menu
    return (user, score)