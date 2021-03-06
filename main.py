from lib import nChoice, run

def main() -> None:
    # Loop game until exited
    while True:
        usr = run() # User is returned from game
        
        if not usr: break # Allow for exit from game menus

        # Get user choice
        match nChoice("Restart", "Show previous scores and restart", "Quit"):
            case 1:
                print(f"Your previous score(s) are: {', '.join([str(x) for x in usr.getScores()])}") # Display previous scores
            case 2: 
                break # Exit
        
        # Restart does not need a case as it happens by default
        
        print()
        
if __name__ == "__main__": main()