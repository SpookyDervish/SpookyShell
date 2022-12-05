import pickle

from command import BaseCommand
from util import read_data, print_but_cooler


class Command(BaseCommand):
    """ Empties [bold]data.dat[/bold] and clears all saved data (blocked ips, saved ips, groups, pins, etc).

    Empties [bold]data.dat[/bold] to clear all data.
    Will create [bold]data.dat[/bold] if it doesn't exist.

    Can be used for troubleshooting purposes.

    Examples:
        • clrcache
    """
    HELP = "Empties [bold]data.dat[/bold] and clears all saved data (blocked ips, saved ips, groups, pins, etc)."

    MIN_ARGS = 0
    MAX_ARGS = 0

    ARGUMENTS = {}

    def run(self, cmd_args, *args):
        # We run this function to make sure the file exists
        read_data("../data.dat")

        # Empty the file with some trickery ;)
        open("../data.dat", "w").close()

        # Now write some empty data
        pickle.dump([[],[],[]], open("../data.dat", "wb"))

        print_but_cooler(args[0], "Shell", "Successfully cleared all saved data.", "bold green")