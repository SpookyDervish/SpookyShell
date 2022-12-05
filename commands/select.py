import socket

from command import BaseCommand, Argument
from main import get_target, send_commands
from util import print_but_cooler


class Command(BaseCommand):
    """Select a target using their id.

    An id is the index of the target you want to remotely access.
    You can find the index of a target with the [bold]list[/bold] command.

    If an id doesn't exist, it will display an error.

    Otherwise, it will open the remote shell and start a session.

    Args:
        id (integer): The id of the target the command will remotely access.

    Examples:
        • select 0
        • select 1
        • select 2
    """
    HELP = "Select a target using their id."

    MIN_ARGS = 1
    MAX_ARGS = 1

    ARGUMENTS = {
        "id": Argument(
            int,
            None,
            "The id of the target the command will remotely access.",
            required=True
        )
    }

    def run(self, cmd_args, *args):
        conn = get_target(cmd_args, args[1])

        if conn != None:
            #print_but_cooler(console, "Shell", f"Connecting to [reverse pale_turquoise1]{all_addresses[int(args[0])][0]}[/reverse pale_turquoise1][bold white]:[/bold white][reverse pale_green3]{all_addresses[int(args[0])][1]}[/reverse pale_green3]", "bold green")

            with args[0].status(f"Connecting to [reverse pale_turquoise1]{args[2][int(cmd_args[0])][0]}[/reverse pale_turquoise1][bold white]:[/bold white][reverse pale_green3]{args[2][int(cmd_args[0])][1]}[/reverse pale_green3]"):
                name = conn.getpeername()[0]
                host_addr = socket.gethostbyaddr(name)

            print()

            print_but_cooler(args[0], "Info", "Session started.", "bold cyan")

            send_commands(conn, name, host_addr)