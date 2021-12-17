import authio

def nChoice(*args: str) -> int:
    [print(f"{x+1}) {s}") for (x,s) in enumerate(args)]
    while True:
        if not (choosed := input("Choice: ")).isdigit(): continue
        if not int(choosed)-1 > 0 and int(choosed)-1 < len(args): continue
        return int(choosed)

def run() -> authio.User:
    uh, user = authio.UserHandler(), None
    while not user:
        user = uh.login(input("Username: "), input("Password: "))
        if not user: print("Username or password incorrect.")
    return user