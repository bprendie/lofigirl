from textual.app import App, ComposeResult
from textual.containers import Container, Grid
from textual.widgets import Header, Footer, Button, Static, Input
from textual.screen import Screen
from textual import events
import subprocess
import yt_dlp
import os
import argparse
from pathlib import Path

PRESETS = [
    {"name": "Lofi Girl", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"},
    {"name": "Synthwave Lofi", "url": "https://www.youtube.com/watch?v=4xDzrJKXOOY"},
    {"name": "Christmas Lofi", "url": "https://www.youtube.com/watch?v=C4qJeIjNd2U"},
    {"name": "Jazz Lofi", "url": "https://www.youtube.com/watch?v=HuFYqnbVbzY"},
]

# Correctly locate the CSS file relative to the app's path
APP_DIR = Path(__file__).parent
CSS_PATH = APP_DIR / "lofigirl.css"

class QuitScreen(Screen):
    """Screen with a dialog to confirm quitting."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Are you sure you want to quit?", id="question"),
            Button("Yes", variant="error", id="yes"),
            Button("No", variant="primary", id="no"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.app.exit()
        else:
            self.app.pop_screen()
            
    def on_key(self, event: events.Key) -> None:
        if event.key.lower() in ("y", "q"):
            self.app.exit()
        elif event.key.lower() == "n":
            self.app.pop_screen()


class PresetButton(Button):
    def __init__(self, preset: dict, **kwargs):
        super().__init__(preset["name"], **kwargs)
        self.preset = preset

class LofiTUI(App):
    """A Textual TUI for playing lofi streams with mpv."""

    CSS_PATH = str(CSS_PATH)
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        with Container():
            for preset in PRESETS:
                yield PresetButton(preset)
            yield Input(placeholder="Paste your own URL here")
            yield Button("Play Custom URL", id="custom_url_button")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        if isinstance(event.button, PresetButton):
            self.play_stream(event.button.preset)
        elif event.button.id == "custom_url_button":
            input_widget = self.query_one(Input)
            url = input_widget.value
            if url:
                self.play_stream({"name": "Custom Stream", "url": url})


    def play_stream(self, preset: dict):
        """Play the selected stream with mpv."""
        if not preset["url"]:
            return

        with self.suspend():
            try:
                ydl_opts = {'format': 'best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(preset["url"], download=False)
                    url = info['url']
                
                subprocess.run(["mpv", "--vo=tct", url])
            except Exception as e:
                # If something goes wrong, we'll just print the error for now
                # In a real app, you'd want to show a proper error dialog
                print(e)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_request_quit(self) -> None:
        """Push the quit screen."""
        self.push_screen(QuitScreen())

def main():
    """The main entry point for the application."""
    parser = argparse.ArgumentParser(description="A Textual TUI for playing lofi streams with mpv.")
    parser.add_argument("--uninstall", action="store_true", help="Remove the application data directory.")
    args = parser.parse_args()

    data_dir = Path.home() / ".local" / "share" / "omarchy"
    bin_dir = data_dir / "bin"

    if args.uninstall:
        print(f"Uninstalling... removing {data_dir}")
        # Here you would add the logic to remove the directory
        # For now, we'll just print a message
        import shutil
        if data_dir.exists():
            shutil.rmtree(data_dir)
            print(f"Removed {data_dir}")
        else:
            print("Data directory not found.")
        return

    if not bin_dir.exists():
        print(f"Creating directory: {bin_dir}")
        bin_dir.mkdir(parents=True, exist_ok=True)

    app = LofiTUI()
    app.run()

if __name__ == "__main__":
    main()
