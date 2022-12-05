import os
import importlib

from command import BaseCommand, Argument
from module import NoValue
from util import print_but_cooler, yes_no_prompt


class Command(BaseCommand):
    HELP = "Runs the specified module."

    MIN_ARGS = 1
    MAX_ARGS = 1

    ARGUMENTS = {
        "module": Argument(
            str,
            None,
            "The module to run.",
            required=True
        )
    }

    def run(self, cmd_args, *args):
        modules_folder = os.path.join(os.getcwd(), "modules")
        module_args = []

        if not os.path.exists(modules_folder):
            prompt = yes_no_prompt(args[0], "Your [bold]modules[/bold] folder doesn't exist! Create it? ")

            if prompt == True:
                os.mkdir(modules_folder)
            else:
                return

        if len(args) < 1:
            print_but_cooler(args[0], "Error", "No module specified.", "bold red")
            return

        found = False
        for file in os.listdir(modules_folder):
            if file.endswith(".py"):
                file_name = file[:len(file) - 3]
                
                if file_name == cmd_args[0]:
                    found = True

                    modules = importlib.import_module("modules." + file_name)
                    module_class = modules.Module()

                    min_args = 0
                    max_args = len(module_class.ARGUMENTS)

                    for k, v in {**module_class.ARGUMENTS}.items():
                        if v.default == NoValue:
                            min_args += 1
                        else:
                            if len(args) < 2:
                                module_args.append(v.default)
                                min_args += 1

                    if len(module_args) - 1 == max_args:
                        module_class.run(args[1:], args[0], args[1], args[2])
                    elif len(module_args) - 1 < min_args or len(args) - 1 > max_args:
                        print_but_cooler(args[0], "Error", f"{file_name} takes exactly {len(module_class.ARGUMENTS)} arguments.", "bold red")
                    else:
                        print_but_cooler(args[0], "Error", f"An unkown error occured when running {file_name}", "bold red")

                    break            
        
        if found == False:
            print_but_cooler(args[0], "Error", "The specified module doesn't exist!", "bold red")