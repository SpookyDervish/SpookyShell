# ==// IMPORTS \\==#
import sys
import getpass
import hashlib
import pickle
import time
import os

if os.name == "nt":
    from msvcrt import getch
from util import console, print_but_cooler, read_data, clear_screen, yes_no_prompt
from pyfiglet import print_figlet


# ==// FUNCTIONS \\==#
def mpass(prompt='Password: '):
        if sys.stdin is not sys.__stdin__:
            pwd = getpass.getpass(prompt)
            return pwd
        else:
            pwd = ""
            sys.stdout.write(prompt)
            sys.stdout.flush()
            while True:
                key = ord(getch())
                if key == 13:
                    sys.stdout.write('\n')
                    return pwd
                    break
                if key == 8:
                    if len(pwd) > 0:
                        sys.stdout.write('\b' + ' ' + '\b')
                        sys.stdout.flush()
                        pwd = pwd[:-1]
                else:
                    char = chr(key)
                    sys.stdout.write('*')
                    sys.stdout.flush()
                    pwd = pwd + char

def sign_up(quiet: bool):
    while True:
        username = input("Username: ")
        hashed = hashlib.pbkdf2_hmac("sha256", username.encode("utf-8"), b"(*!@#s", 823)

        new_user = hashed.hex()

        data = read_data("data.dat")
        users = data[2]

        if new_user in users:
            print_but_cooler(console, "Error", "User already exists!", "bold red")
        else:
            break

    if os.name == "nt":
        password = mpass()
    else:
        password = console.input("Password: ")
        
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), b"(*!@#s", 823)
    new_pass = hashed.hex()

    data = read_data("data.dat")
    users = data[2]

    users.append([new_user, new_pass])
    data[2] = users

    pickle.dump(data, open("data.dat", "wb"))

    print_but_cooler(console, "Info", "Successfully created the new user!", "bold cyan")
    time.sleep(1)
    clear_screen()
    print_banner(quiet)

def print_banner(quiet: bool = False):
    if quiet == False:
        clear_screen()
        print_figlet("SpookyShell", "Doom", "LIGHT_GREEN")
        console.print((" " * 40) + "By: SpookyDervish", style="bold")
        print("")
        print("")

def check_login(hex: str):
    data = read_data("data.dat")
    users = data[2]

    for user in users:
        if hex == user[0]:
            return True
    
    return False

def login_screen(quiet: bool = False):
    """The main login screen for SpookyShell
    """
    print = console.print
    input = console.input

    while True:
        print_banner(quiet)

        print("*** [bold]Operator Login[/bold] ***\n")

        print("[bold light_goldenrod2]=========================[/bold light_goldenrod2]")
        print("[bold][1][/bold] Login")
        print("[bold][2][/bold] Register")
        print("[bold][3][/bold] Exit")
        print("[bold light_goldenrod2]=========================[/bold light_goldenrod2]\n")

        user_input = input("[bold]>[/bold] ")
        
        if user_input == "1":
            data = read_data("data.dat")
            users = data[2]

            if not any(users):
                print_but_cooler(console, "Error", "The list of users is empty!", "bold red")
                
                prompt = yes_no_prompt(console, "Create new user? ")
                
                if prompt == True:
                    sign_up(quiet)
            else:
                while True:
                    username = input("Username: ")
                    hashed = hashlib.pbkdf2_hmac("sha256", username.encode("utf-8"), b"(*!@#s", 823)

                    user_input = hashed.hex()

                    if check_login(user_input):
                        print(f"Welcome [bold]{username}[/bold]!")
                        break
                    else:
                        print_but_cooler(console, "Error", "The specified user does not exist.", "bold red")
                while True:
                    if os.name == "nt":
                        password = mpass()
                    else:
                        password = console.input("Password: ")
                    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), b"(*!@#s", 823)

                    pass_input = hashed.hex()

                    for user in users:
                        if user[0] == user_input and user[1] == pass_input:
                            print_banner(quiet)

                            return True
                        else:
                            print_but_cooler(console, "Error", "Invalid password!", "bold red")
                            time.sleep(2)
        elif user_input == "2":
            sign_up(quiet)
        elif user_input == "3":
            console.print("Goodbye!")
            break
        else:
            print_but_cooler(console, "Error", "Invalid selection!", "bold red")
            time.sleep(2)
    
    return False
