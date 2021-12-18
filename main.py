from lib import nChoice, run

def main() -> None:
    while True:
        usr = run()
        
        match nChoice("Restart", "Show previous scores and restart", "Quit"):
            case 2:
                print(f"Your previous scores are: {', '.join([str(x) for x in usr.getScores()])}")
            case 3: 
                break
        
        print()
        
if __name__ == "__main__": main()