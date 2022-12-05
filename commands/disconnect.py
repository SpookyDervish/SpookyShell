import socket

from command import BaseCommand, Argument
from main import get_target
from util import print_but_cooler


class Command(BaseCommand):
    """Disconnect a target from the list of connections.

    Removes the specified client using their id from the list of available connections.
    Although, the client can always reconnect.

    If you wish to permanantly remove a target, use the [bold]block[/bold] command.

    Args:
        id (integer): The id of the target the command will remove from the list of avilable clients.

    Examples:
        • disconnect 0
        • disconnect 1
        • disconnect 2
    """
    HELP = "Disconnect a target from the list of connections."

    MIN_ARGS = 1
    MAX_ARGS = 1

    ARGUMENTS = {
        "id": Argument(
            int,
            None,
            "The id of the target the command will remove from the list of avilable clients.",
            required=True
        )
    }

    def run(self, cmd_args, *args):
        try:
            conn = get_target(cmd_args, args[1])

            if conn != None:
                conn.shutdown(2)
                conn.close()
                print_but_cooler(args[0], "Shell", f"Removed target {cmd_args[0]}.", "bold green")
        except socket.error:
            print_but_cooler(args[0], "Error", f"Failed to remove target {cmd_args[0]}.", "bold red")