import pickle

from command import BaseCommand, Argument
from util import read_data, print_but_cooler
from main import get_blocked_ips


class Command(BaseCommand):
    """Remove an ip from the blocked list.

    Unblocked ips can reconnect and will appear in the table when running the [bold]list[/bold] command.
    If an ip is already unblocked, then the command will display an error.

    Args:
        ip (string): The ip to remove from the blocked list.

    Examples:
        • unblock 127.0.0.1
        • unblock 0.0.0.0
    """
    HELP: str = "Remove an ip from the blocked list."
    MIN_ARGS = 1
    MAX_ARGS = 1

    ARGUMENTS = {
        "ip": Argument(
            str,
            None,
            "The ip to remove from the blocked list.",
            required=True
        )
    }

    def run(self, cmd_args, *args):
        data = read_data("../data.dat")
        blocked = get_blocked_ips("../data.dat")
        
        if cmd_args[0] not in blocked:
            print_but_cooler(args[0], "Error", "The specified ip is already unblocked.", "bold red")
            return

        blocked.remove(cmd_args[0])
        data[0] = blocked
        pickle.dump(data, open("../data.dat", "wb"))
        print_but_cooler(args[0], "Shell", f"Successfully unblocked {cmd_args[0]}", "bold green")