# ==// IMPORTS \\==#
from typing import Any, Dict, Callable, Optional
from dataclasses import dataclass


# ==// VARIABLES \\==#
LOADED_MODULES = {}


# ==// CLASSES \\==#
class NoValue:
    """Indicates that the module argument has no default value and is required."""


class ModuleFailed(Exception):
    """Base class for module failure"""


class ModuleNotFound(ModuleFailed):
    """The specified module was not found"""


class IncorrectPlatformError(ModuleFailed):
    """The requested module didn't match the current platform"""


class ArgumentFormatError(ModuleFailed):
    """Format of one of the arguments was incorrect"""


class MissingArgument(ModuleFailed):
    """A required argument is missing"""


class InvalidArgument(ModuleFailed):
    """This argument does not exist and ALLOW_KWARGS was false"""

@dataclass
class Argument:
    """Describes an individual module argument. Arguments to modules are
    always required. If an argument has the default :class:`NoValue` then
    the module will fail if no value is provided by the user."""

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

class BaseModule:
    ARGUMENTS: Dict[str, Argument] = {}
    ALLOW_KWARGS: bool = False
    COLLAPSE_RESULT: bool = False

    def __init__(self):
        self.progress = None
        # Filled in by reload
        self.name = None

    def run(self, cmd_args, *args):
        raise NotImplementedError