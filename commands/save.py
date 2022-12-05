import pickle

from command import BaseCommand, Argument
from util import read_data, print_but_cooler
from main import get_saved_ips, get_blocked_ips


class Command(BaseCommand):
    """Saves an ip to [bold]data.dat[/bold].

    The command writes to [bold]data.dat[/bold] and pickles a
    new entry in the blocked list.

    Saved ips cannot be blocked and will always appear below pinned ips.

    If a saved ip is not available, it will appear with "[[bold red]DISCONNECTED[/bold red]]"
    next to it in the client list.

    Otherwise it will appear with "[[bold green]CONNECTED[/bold green]]" next to it in the
    client list.

    Args:
        ip (string): The ip to save to [bold]data.dat[/bold].

    Examples:
        • save 127.0.1.1
        • save 123.456.78.9
    """
    HELP = "Saves an ip to [bold]data.dat[/bold]."

    MIN_ARGS = 1
    MAX_ARGS = 1

    ARGUMENTS = {
        "ip": Argument(
            str,
            None,
            "The ip to save",
            required=True
        )
    }

    def run(self, cmd_args, *args):
        data = read_data("../data.dat")
        saved = get_saved_ips("../data.dat")
        blocked = get_blocked_ips("../data.dat")
        
        if args[0] in saved:
            print_but_cooler(args[0], "Error", "The specified ip is already saved.\n", "bold red")
            return

        if args[0] in blocked:
            print_but_cooler(args[0], "Error", "You cannot save a blocked ip.\n", "bold red")
            return

        saved.append(cmd_args[0])
        data[1] = saved

        pickle.dump(data, open("../data.dat", "wb"))
        print_but_cooler(args[0], "Shell", f"Successfully saved {cmd_args[0]}", "bold green")