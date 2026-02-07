#!/usr/bin/env python3
"""Simple CREAI GUI inspired by an Iron Man-style HUD."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


ACCENT = "#ff3b30"
BACKGROUND = "#0b0f14"
PANEL = "#131a22"
TEXT = "#e6eef8"


class CreaiGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CREAI Assistant")
        self.configure(background=BACKGROUND)
        self.geometry("720x420")
        self.minsize(640, 360)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=BACKGROUND)
        style.configure("Header.TLabel", background=BACKGROUND, foreground=ACCENT, font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background=BACKGROUND, foreground=TEXT, font=("Segoe UI", 11))
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Accent.TButton", background=ACCENT, foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#ff5c55")])

        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(20, 10))

        title = ttk.Label(header, text="CREAI HUD", style="Header.TLabel")
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Iron Man-inspired command console",
            style="Sub.TLabel",
        )
        subtitle.pack(anchor="w")

        body = ttk.Frame(self, style="TFrame")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        left_panel = ttk.Frame(body, style="Panel.TFrame")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_panel = ttk.Frame(body, style="Panel.TFrame")
        right_panel.pack(side="left", fill="both", expand=True, padx=(10, 0))

        ttk.Label(left_panel, text="System Status", style="Panel.TLabel").pack(anchor="w", padx=16, pady=(16, 4))
        ttk.Label(left_panel, text="• Power: Stable", style="Panel.TLabel").pack(anchor="w", padx=16)
        ttk.Label(left_panel, text="• Network: Online", style="Panel.TLabel").pack(anchor="w", padx=16)
        ttk.Label(left_panel, text="• Modules: Ready", style="Panel.TLabel").pack(anchor="w", padx=16)

        ttk.Label(right_panel, text="Quick Actions", style="Panel.TLabel").pack(anchor="w", padx=16, pady=(16, 8))
        ttk.Button(right_panel, text="Launch Assistant", style="Accent.TButton").pack(anchor="w", padx=16, pady=4)
        ttk.Button(right_panel, text="Open Logs", style="Accent.TButton").pack(anchor="w", padx=16, pady=4)
        ttk.Button(right_panel, text="Diagnostics", style="Accent.TButton").pack(anchor="w", padx=16, pady=4)

        footer = ttk.Frame(self, style="TFrame")
        footer.pack(fill="x", padx=20, pady=(10, 20))
        ttk.Label(
            footer,
            text="Tip: run the CLI assistant for commands.",
            style="Sub.TLabel",
        ).pack(anchor="w")


def main() -> None:
    app = CreaiGui()
    app.mainloop()


if __name__ == "__main__":
    main()
