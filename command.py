# ==// IMPORTS \\==#
import os
import importlib
import textwrap

from typing import Any, Dict, Callable
from dataclasses import dataclass
from rich.console import Console


# ==// FUNCTIONS \\==#
def get_command(name: str):
    commands_folder = os.path.join(os.getcwd(), "commands")

    for file in os.listdir(commands_folder):
        if file.endswith(".py"):
            file_name = file[:len(file) - 3]

            if file_name == name:
                commands = importlib.import_module("commands." + file_name)
                command_class = commands.Command()
                return command_class
    return None

def print_command_help(console: Console, name: str):
    command = get_command(name)
    doc = command.__doc__

    if doc == None:
        doc = "This command doesn't have any extra information."

    console.print(textwrap.dedent(doc).strip())


# ==// CLASSES \\==#
class NoValue:
    """Indicates that the command argument has no default value and is required."""

@dataclass
class Argument:
    """Describes an individual command argument. Arguments to commands are
    always required. If an argument has the default :class:`NoValue` then
    the command will fail if no value is provided by the user."""

    type: Callable[[str], Any] = str
    """ A callable which converts a string to the required type
    This function should also return the passed value if it is
    already of that type. A :class:`ValueError` is raised if
    conversion is not possible. """
    default: Any = NoValue
    """ The default value for this argument. If set to :class:`NoValue`, the
    argument **must** be set by the user. """
    help: str = ""
    """ The help text displayed in the ``info`` output. """
    required: bool = False
    """Whether the argument is forced or not."""

class BaseCommand:
    ARGUMENTS: Dict[str, Argument] = {}
    HELP: str = ""
    MIN_ARGS: int = 0
    MAX_ARGS: int = 0
    ALLOW_KWARGS: bool = False
    COLLAPSE_RESULT: bool = False

    def __init__(self):
        self.progress = None
        # Filled in by reload
        self.name = None

    def run(self, cmd_args, *args):
        raise NotImplementedError