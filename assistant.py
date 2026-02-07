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
        "  speak <text>          Speak text aloud with a female voice when possible\n"
        "  import_keys <path>    Import API keys from a .env-style file\n"
        "  voice                Listen for voice commands (optional dependency)\n"
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


def _find_female_voice_id(engine: "pyttsx3.Engine") -> str | None:
    for voice in engine.getProperty("voices"):
        name = getattr(voice, "name", "").lower()
        gender = getattr(voice, "gender", "").lower()
        if "female" in gender or "female" in name or "zira" in name or "samantha" in name:
            return voice.id
    return None


def handle_speak(args: list[str]) -> str:
    if not args:
        return "Usage: speak <text>"

    try:
        import pyttsx3
    except ModuleNotFoundError:
        return "Text-to-speech requires pyttsx3. Install it with: pip install pyttsx3"

    text = " ".join(args)
    engine = pyttsx3.init()
    female_voice_id = _find_female_voice_id(engine)
    if female_voice_id:
        engine.setProperty("voice", female_voice_id)
    engine.say(text)
    engine.runAndWait()
    return "Spoken."


def _parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    if stripped.lower().startswith("export "):
        stripped = stripped[7:].lstrip()

    if "=" not in stripped:
        return None

    key, value = stripped.split("=", 1)
    return key.strip(), value.strip().strip("\"'")


def handle_import_keys(args: list[str]) -> str:
    if not args:
        return "Usage: import_keys <path>"

    path = os.path.expanduser(" ".join(args))
    if not os.path.exists(path):
        return f"Path not found: {path}"

    imported = 0
    with open(path, "r", encoding="utf-8") as file_handle:
        for line in file_handle:
            parsed = _parse_env_line(line)
            if not parsed:
                continue
            key, value = parsed
            if key:
                os.environ[key] = value
                imported += 1

    return f"Imported {imported} key(s)."


def _shutdown_command() -> list[str]:
    if sys.platform.startswith("darwin"):
        return ["shutdown", "-h", "now"]
    if os.name == "nt":
        return ["shutdown", "/s", "/t", "0"]
    return ["shutdown", "-h", "now"]


def _restart_command() -> list[str]:
    if sys.platform.startswith("darwin"):
        return ["shutdown", "-r", "now"]
    if os.name == "nt":
        return ["shutdown", "/r", "/t", "0"]
    return ["shutdown", "-r", "now"]


def _execute_system_command(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except OSError as exc:
        return f"Command failed to start: {exc}"
    if result.returncode != 0:
        error = result.stderr.strip() or result.stdout.strip()
        return f"Command failed: {error or 'Unknown error'}"
    return "Command executed."


def handle_voice(_: list[str]) -> str:
    try:
        import speech_recognition as sr
    except ModuleNotFoundError:
        return (
            "Voice mode requires speech_recognition. Install it with: "
            "pip install SpeechRecognition"
        )

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return "Listening timed out."

    try:
        command = recognizer.recognize_google(audio).lower().strip()
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as exc:
        return f"Speech recognition request failed: {exc}"

    if command.startswith("open "):
        target = command.replace("open ", "", 1).strip()
        return handle_open([target])

    if command in {"shutdown", "shut down"}:
        return (
            "Voice shutdown requested. For safety, run: "
            "python3 assistant.py run " + " ".join(shlex.quote(part) for part in _shutdown_command())
        )

    if command in {"restart", "reboot"}:
        return (
            "Voice restart requested. For safety, run: "
            "python3 assistant.py run " + " ".join(shlex.quote(part) for part in _restart_command())
        )

    return f"Unrecognized voice command: {command}"


HANDLERS: dict[str, CommandHandler] = {
    "help": handle_help,
    "time": handle_time,
    "date": handle_date,
    "open": handle_open,
    "run": handle_run,
    "speak": handle_speak,
    "import_keys": handle_import_keys,
    "voice": handle_voice,
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
