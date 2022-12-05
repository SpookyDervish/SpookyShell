# ==// IMPORTS \\==#
import sys
import os
import pickle

from rich.console import Console


# ==// VARIABLES \\==#
console = Console()


# ==// FUNCTIONS \\==#
def read_data(file: str):
    data = []

    try:
        data = pickle.load(open(file, "rb"))
    except EOFError:
        # The file is empty, usually happens on first time running
        data = [[],[],[]]
    except FileNotFoundError:
        # The file doesn't exist
        print()
        print_but_cooler(console, "Warn", f"The file [underline]{file}[/underline] does not exist, creating..", "bold gold1")

        os.open(file,os.O_BINARY | os.O_CREAT)

        with open(file, "wb") as f:
            pickle.dump([[],[],[]], f)
            f.close()

        data = read_data(file)

    return data

def print_but_cooler(console: Console, prefix: str, message: str, colour: str):
    """A simple function to format print messages in an easy to read way.\n

    Args:
        console (Console): The rich '`Console`' to print to.\n
        prefix (str): The prefix in the brackets, e.g: '`Info`'\n
        message (str): The message to be printed.\n
        colour (str): The colour of the prefix, e.g: '`bold red`'
    """
    console.print("[", end="")
    console.print(f"[{colour}]{prefix}[/{colour}]", end="")
    console.print(f"] :: {message}")

def yes_no_prompt(console: Console, input: str) -> bool:
    prompt = console.input(input)

    yes_choices = ["y", "yes"]
    no_choices = ["n", "no"]

    if prompt.lower() in yes_choices:
        return True
    elif prompt.lower() in no_choices:
        return False
    else:
        print("\r")
        yes_no_prompt(console, input)

def clear_screen():
    name = sys.platform

    if name == "linux1" or name == "linux2": # Linux
        os.system("clear")
    elif name == "darwin":                   # Mac
        os.system("clear")
    elif name == "win32":                    # Windows
        os.system("cls")

class InteractiveExit(Exception):
    """Indicates we should exit the interactive terminal"""