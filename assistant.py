#!/usr/bin/env python3
"""Simple offline CLI assistant for basic PC tasks."""

from __future__ import annotations

import datetime
import os
import shlex
import subprocess
import sys
from typing import Callable


CommandHandler = Callable[[list[str]], str]


def handle_help(_: list[str]) -> str:
    return (
        "Available commands:\n"
        "  help                 Show this message\n"
        "  time                 Show current time\n"
        "  date                 Show current date\n"
        "  open <path>           Open a file or folder (uses OS default)\n"
        "  run <command>         Run a shell command (sandboxed to current user)\n"
        "  exit / quit           Leave the assistant\n"
    )


def handle_time(_: list[str]) -> str:
    now = datetime.datetime.now()
    return now.strftime("Current time: %H:%M:%S")


def handle_date(_: list[str]) -> str:
    today = datetime.date.today()
    return today.strftime("Today's date: %Y-%m-%d")


def handle_open(args: list[str]) -> str:
    if not args:
        return "Usage: open <path>"

    target = os.path.expanduser(" ".join(args))
    if not os.path.exists(target):
        return f"Path not found: {target}"

    if sys.platform.startswith("darwin"):
        opener = ["open", target]
    elif os.name == "nt":
        opener = ["cmd", "/c", "start", "", target]
    else:
        opener = ["xdg-open", target]

    try:
        subprocess.Popen(opener)
    except OSError as exc:
        return f"Failed to open: {exc}"

    return f"Opened: {target}"


def handle_run(args: list[str]) -> str:
    if not args:
        return "Usage: run <command>"

    try:
        result = subprocess.run(args, check=False, capture_output=True, text=True)
    except OSError as exc:
        return f"Command failed to start: {exc}"

    output = result.stdout.strip()
    error = result.stderr.strip()
    combined = "\n".join(part for part in [output, error] if part)
    status = f"Exit code: {result.returncode}"
    return "\n".join([status, combined]) if combined else status


HANDLERS: dict[str, CommandHandler] = {
    "help": handle_help,
    "time": handle_time,
    "date": handle_date,
    "open": handle_open,
    "run": handle_run,
}


WELCOME = (
    "CREAI Assistant ready. Type 'help' for commands, 'exit' to quit."
)


def process_command(raw: str) -> str | None:
    if not raw:
        return None

    if raw.lower() in {"exit", "quit"}:
        return "Goodbye!"

    try:
        parts = shlex.split(raw)
    except ValueError as exc:
        return f"Parse error: {exc}"

    command, *args = parts
    handler = HANDLERS.get(command.lower())
    if not handler:
        return "Unknown command. Type 'help' for options."

    return handler(args)


def main() -> None:
    if len(sys.argv) > 1:
        response = process_command(" ".join(sys.argv[1:]))
        if response:
            print(response)
        return

    print(WELCOME)
    while True:
        try:
            raw = input("assistant> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        response = process_command(raw)
        if response is None:
            continue
        print(response)
        if response == "Goodbye!":
            break


if __name__ == "__main__":
    main()
