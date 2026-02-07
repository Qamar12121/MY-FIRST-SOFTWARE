# CREAI AI Assistant

A lightweight, offline command-line assistant you can run on your PC. It offers a few built-in commands for quick tasks and can run shell commands when requested.

## Features
- Show current time and date.
- Open files or folders with the OS default program.
- Run simple shell commands.
- Speak text aloud with a female voice when available.
- Import API keys from a `.env`-style file.
- Use voice commands for simple actions (optional dependency).

## Getting Started

```bash
python3 assistant.py
```

Type `help` to see available commands.

### GUI (Iron Man-inspired HUD)

```bash
python3 gui.py
```

You can also run a single command non-interactively:

```bash
python3 assistant.py time
python3 assistant.py run ls -la
python3 assistant.py speak "Hello from CREAI"
python3 assistant.py import_keys ~/.config/creai.env
python3 assistant.py voice
```

## Notes
- The `run` command executes commands as your current user.
- The `open` command uses the OS default opener (`open`, `xdg-open`, or `start`).
- The `speak` command requires `pyttsx3` (install with `pip install pyttsx3`).
- The `import_keys` command supports lines like `API_KEY=...` or `export API_KEY=...`.
- The `voice` command requires `SpeechRecognition` and a working microphone.
