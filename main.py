from lib import nChoice, run

def main() -> None:
    while True:
        usr, q = run(), True
        if (choice := nChoice("Restart", "Show previous scores", "Quit")) == 1: q = False
        elif choice == 2: print(f"Your previous scores are: {', '.join([str(x) for x in usr.getScores()])}")
        if q: quit()

main()