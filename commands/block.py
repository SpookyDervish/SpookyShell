import pickle

from command import BaseCommand, Argument
from util import read_data, print_but_cooler
from main import get_blocked_ips, get_saved_ips


class Command(BaseCommand):
    """Block an ip from connecting until the [bold]unblock[/bold] command is run on the corosponding ip.

    The command writes to [bold]data.dat[/bold] and pickles a
    new entry in the blocked list.

    Blocked ips will not connect and will not appear in the table of clients when running the [bold]list[/bold]
    command.

    If an ip is already blocked or saved, then the command will display
    an error

    Args:
        ip (string): The ip to add to the blocked list.

    Examples:
        • block 127.0.0.1
        • block 0.0.0.0
    """
    HELP: str = "Block an ip from connecting until the [bold]unblock[/bold] command is run on the corosponding ip."
    MIN_ARGS = 1
    MAX_ARGS = 1

    ARGUMENTS = {
        "ip": Argument(
            str,
            None,
            "The ip to add to the blocked list.",
            required=True
        )
    }

    def run(self, cmd_args, *args):
        data = read_data("../data.dat")
        blocked = get_blocked_ips("../data.dat")
        saved = get_saved_ips("../data.dat")
        
        if cmd_args[0] in blocked:
            print_but_cooler(args[0], "Error", "The specified ip is already blocked.", "bold red")
            return

        if cmd_args[0] in saved:
            print_but_cooler(args[0], "Error", "You cannot block a saved ip.", "bold red")
            return

        blocked.append(cmd_args[0])
        data[0] = blocked
        pickle.dump(data, open("../data.dat", "wb"))
        print_but_cooler(args[0], "Shell", f"Successfully blocked {cmd_args[0]}", "bold green")