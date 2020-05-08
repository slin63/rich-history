import os
import sys
import subprocess
import re
import signal

from rich import print as pprint
from rich.console import Console
from rich.syntax import Syntax

RUNFILE = "prettycdhistory"
HOME_DIR = os.getenv("HOME")
DIR = os.path.dirname(os.path.realpath(__file__))
LENGTH = 10
LENGTH_MAX = 30
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
    # Scale number of directories to size of current terminal window
    try:
        LENGTH = int(
            min(int(sys.argv[1]) // 1.2, LENGTH_MAX)
        )
    except Exception as e:
        print("Issue dynamically setting LENGTH:", e)

    history = sys.argv[
        3::2
    ]  # Skip every other element, starting from element 1

    # Create directory to line map
    id_ = 0
    cmd_map = {}
    for line in history:
        if id_ >= 10:
            ext = EXTENSION_CHARACTER[(id_ // 10) - 1]
            cmd_map[f"{id_%10}{ext}"] = line
        else:
            cmd_map[str(id_)] = line
        id_ += 1

    return cmd_map


def get_user_selection(cmd_map: dict) -> str:
    # Render history
    print("")
    for k, cmd in cmd_map.items():
        k = _decorate_key(k)
        cmd = _highlight_last(cmd.strip())
        pprint(f" {k}  →  {cmd}")

    # Get user selection
    choice = input(f"\nselect a directory → ")
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


def _highlight_last(cmd: str) -> str:
    global OTHER
    color = "cyan" if OTHER else "blue"
    OTHER = not OTHER

    last = cmd.split('/')[-1]
    beginning = cmd[0:len(cmd)-len(last)]
    last = f"[bold underline {color}]{last}[/]"

    return f"[white not bold]{beginning}[/]{last}"


if __name__ == "__main__":
    cmd_map = create_command_map()
    cmd = get_user_selection(cmd_map)
    if cmd:
        # pprint(f" → [bold yellow]{cmd}[/bold yellow]")
        write_to_runfile(cmd)
    else:
        exit(1)
