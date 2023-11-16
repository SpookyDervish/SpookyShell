import os
import rich.box
import textwrap

from command import BaseCommand, Argument, print_command_help, get_command
from rich.table import Table, Column
from util import print_but_cooler


class Command(BaseCommand):
    """Get a list of commands and information.

    If ran with arguments, it will try to find a command and provide more information on it.
    Otherwise if it cant find a command it will display an error.

    If it cannot find more info on a command it will just show "This command doesn't have any extra information.".

    Args:
        topic (string, optional): If specified, it will provide a more detailed description of a command.

    Examples:
        • help clear
        • help quit
        • help list
    """
    HELP = "Display this message."

    MIN_ARGS = 0
    MAX_ARGS = 1

    ARGUMENTS = {
        "topic": Argument(
            str,
            None,
            "If specified, it will provide a more detailed description of a command.",
            required=False
        )
    }

    def run(self, cmd_args, *args):
        commands = []
        commands_folder = os.path.join(os.getcwd(), "commands")

        for file in os.listdir(commands_folder):
                if file.endswith(".py"):
                    file_name = file[:len(file) - 3]
                    commands.append(file_name)

        if len(cmd_args) > 0:
            if cmd_args[0] == None:
                self.run([], *args)
                return

            found = False
            for command in commands:
                if command == cmd_args[0]:
                    found = True
                    print_command_help(args[0], command)
                    break

            if found == False:
                print_but_cooler(args[0], "Error", f"Did not find a command with the name \"{cmd_args[0]}\".", "bold red")
                return
        else:
            table = Table(
                Column("Command", style="green"),
                Column("Description", no_wrap=True),
                box=rich.box.SIMPLE
            )

            for command in commands:
                cmd = get_command(command)

                help = cmd.HELP

                if help == None:
                    help = ""
                else:
                    help = textwrap.shorten(
                        textwrap.dedent(help).strip().replace("\n", ""), 60
                    )

                table.add_row(command, help)
            
            args[0].print("[bold]Type \"help\" and then the name of a command for more information.[/bold]")
            args[0].print(table)