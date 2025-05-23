"""
exiftool_session.py

Purpose:
    Provides a persistent session interface for running ExifTool commands efficiently.

Main Functions:
    - ExifToolSession: Class for managing a background ExifTool process and sending commands.
    - run_command(args): Executes ExifTool commands within the session.

Use this module to avoid repeated ExifTool process startup overhead.
"""

import subprocess

class ExifToolSession:
    def __init__(self, exiftool_path="exiftool"):
        self.process = subprocess.Popen(
            [exiftool_path, "-stay_open", "True", "-@", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def run_command(self, args):
        cmd = "\n".join(args + ["-execute\n"])
        self.process.stdin.write(cmd)
        self.process.stdin.flush()
        output = []
        while True:
            line = self.process.stdout.readline()
            if line.strip() == "{ready}":
                break
            output.append(line)
        return output

    def close(self):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()
        self.process.wait()

