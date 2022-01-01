import PySimpleGUI as sg
from lib import run

options = ["Pick a new shape", "Show previous scores and logout", "Logout", "Quit"]

def main() -> None:
    # Loop game until exited
    usr = None
    
    while True:
        output, event = run(usr), None # Either None or (User, Score) is returned from game
        
        if not output:
            break
        
        (usr, score) = output
        
        layout = [
            [
                sg.Text("Thanks for using my Area Trainer!")
            ],
            [
                sg.Text(f"Your score for this session was {score}")
            ],
            [
                sg.HorizontalSeparator()
            ],
            [sg.Button(s) for s in options]
        ]
        
        window = sg.Window("Area Trainer", layout, finalize=True)
        
        # Get user choice
        while True:
            event, _ = window.read()
            
            if event == sg.WIN_CLOSED: # Check for window close
                window.close()
                quit(0)
            
            elif event in options:
                break
        
        match options.index(event):
            case 1: # Display previous scores and wipe usr
                window.close()
                
                layout = [
                    [
                        sg.Text(f"Your previous score(s) are: {', '.join([str(x) for x in usr.getScores()])}")
                    ],
                    [
                        sg.Button("Continue")
                    ]
                ]
                
                window = sg.Window("Area Trainer", layout)
                
                while True:
                    event, _ = window.read()
            
                    if event == sg.WIN_CLOSED: # Check for window close
                        window.close()
                        quit(0)
                    
                    elif event == "Continue":
                        break
            case 2:
                usr = None
            case 3:
                window.close()
                break
            
        window.close()
        
if __name__ == "__main__": main()