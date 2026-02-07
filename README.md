# CREAI AI Assistant

A lightweight, offline command-line assistant you can run on your PC. It offers a few built-in commands for quick tasks and can run shell commands when requested.

## Features
- Show current time and date.
- Open files or folders with the OS default program.
- Run simple shell commands.

## Getting Started

```bash
python3 assistant.py
```

Type `help` to see available commands.

You can also run a single command non-interactively:

```bash
python3 assistant.py time
python3 assistant.py run ls -la
```

## Notes
- The `run` command executes commands as your current user.
- The `open` command uses the OS default opener (`open`, `xdg-open`, or `start`).
