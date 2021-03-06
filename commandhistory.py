import os
import sys
import subprocess
import re
import signal

from rich import print as pprint
from rich.console import Console
from rich.syntax import Syntax

RUNFILE = "prettycommandhistory"
HISTORY_FILE = os.getenv("HISTFILE")
HOME_DIR = os.getenv("HOME")
DIR = os.path.dirname(os.path.realpath(__file__))
LENGTH = 10
LENGTH_MAX = 29
EXTENSION_CHARACTER = ["b", "c", "d"]
EXTENSION_COLOR = {
    "b": "[yellow]$[/yellow]",
    "c": "[red]$[/red]",
    "d": "[blue]$[/blue]",
}

# Gracefully exit on ctrl-c.
graceful_exit = lambda a, b: exit(1)
signal.signal(signal.SIGINT, graceful_exit)


def create_command_map() -> dict:
    # Scale number of commands to size of current terminal window
    try:
        LENGTH = int(
            min(int(sys.argv[1]) // 1.2, LENGTH_MAX)
        )
    except Exception as e:
        print("Issue dynamically setting LENGTH:", e)

    # Grab last LENGTH entries of history file
    out = subprocess.Popen(
        ["tail", "-n", str(LENGTH), HISTORY_FILE],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    history, e = out.communicate()
    history = history.decode("utf-8")
    if e:
        raise Exception(e)

    # Create command to line map
    id_ = 1
    cmd_map = {}
    for line in history.split("\n"):
        cmd_start = re.search(r"[\d]+:\d;", line)
        if cmd_start:
            cmd = line[cmd_start.end() :]
            if id_ >= 10:
                ext = EXTENSION_CHARACTER[(id_ // 10) - 1]
                cmd_map[f"{id_%10}{ext}"] = cmd
            else:
                cmd_map[str(id_)] = cmd
            id_ += 1

    return cmd_map


def get_user_selection(cmd_map: dict) -> str:
    # Render history
    print("")
    for k, cmd in cmd_map.items():
        k = _decorate_key(k)
        cmd = _highlight_first(cmd.strip())
        pprint(f" {k}  →  {cmd}")

    # Get user selection
    choice = input(f"\nselect a command → ")
    cmd = cmd_map.get(choice)

    return cmd


def write_to_runfile(cmd: str) -> None:
    # Write selection to file to be executed by shell script
    with open(f"{DIR}/{RUNFILE}", "w") as f:
        # Expand tildes
        cmd = cmd.replace("~", HOME_DIR)
        f.write(cmd)


# Functions for making things look pretty
def _decorate_key(k: int) -> str:
    if len(k) < 2:
        return f"[bold white] {k}[/bold white]"
    ext = k[1]
    color = EXTENSION_COLOR[ext]
    k = k[0] + color.replace("$", ext)

    return f"[bold white]{k}[/bold white]"


OTHER = False


def _highlight_first(cmd: str) -> str:
    global OTHER
    first = cmd.find(" ")
    color = "cyan" if OTHER else "blue"
    OTHER = not OTHER
    if first == -1:
        return f"[bold {color}]{cmd}[/bold {color}]"
    return f"[bold {color}]{cmd[:first]}[/][white not bold]{cmd[first:]}[/]"


if __name__ == "__main__":
    cmd_map = create_command_map()
    cmd = get_user_selection(cmd_map)
    if cmd:
        # pprint(f" → [bold yellow]{cmd}[/bold yellow]")
        write_to_runfile(cmd)
    else:
        exit(1)
