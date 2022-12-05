import pickle

from command import BaseCommand, Argument
from util import read_data, print_but_cooler
from main import get_saved_ips


class Command(BaseCommand):
    """Removes an ip from the saved list.

    Edits [bold]data.dat[/bold] and removes the specified ip entry from the file.
    The ip will no longer appear in the client list.

    Args:
        ip (string): The ip to remove.
    """
    HELP = "Removes an ip from the saved list."

    MIN_ARGS = 1
    MAX_ARGS = 1

    ARGUMENTS = {
        "ip": Argument(
            str,
            None,
            "The ip to remove from the saved list.",
            required=True
        )
    }

    def run(self, cmd_args, *args):
        data = read_data("../data.dat")
        saved = get_saved_ips("../data.dat")
        
        if cmd_args[0] not in saved:
            print_but_cooler(args[0], "Error", "The specified ip is already removed.\n", "bold red")
            return

        saved.remove(cmd_args[0])
        data[1] = saved

        pickle.dump(data, open("../data.dat", "wb"))
        print_but_cooler(args[0], "Shell", f"Successfully saved {cmd_args[0]}", "bold green")