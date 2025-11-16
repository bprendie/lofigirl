from textual.app import App, ComposeResult
from textual.containers import Container, Grid
from textual.widgets import Header, Footer, Button, Static, Input
from textual.screen import Screen
from textual import events
import subprocess
import yt_dlp
import json
from pathlib import Path
from typing import List, Dict

DEFAULT_PRESETS: List[Dict[str, str]] = [
    {"name": "Lofi Girl", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"},
    {"name": "Synthwave Lofi", "url": "https://www.youtube.com/watch?v=4xDzrJKXOOY"},
    {"name": "Christmas Lofi", "url": "https://www.youtube.com/watch?v=C4qJeIjNd2U"},
    {"name": "Jazz Lofi", "url": "https://www.youtube.com/watch?v=HuFYqnbVbzY"},
]

PRESET_FILE = Path(__file__).with_name("presets.json")


def load_presets() -> List[Dict[str, str]]:
    """Load presets from presets.json with a graceful fallback."""
    try:
        with PRESET_FILE.open("r", encoding="utf-8") as f:
            presets = json.load(f)

        if not isinstance(presets, list):
            raise ValueError("Preset data must be a list")

        cleaned = []
        for preset in presets:
            if (
                isinstance(preset, dict)
                and isinstance(preset.get("name"), str)
                and isinstance(preset.get("url"), str)
                and preset["name"].strip()
                and preset["url"].strip()
            ):
                cleaned.append({"name": preset["name"].strip(), "url": preset["url"].strip()})
        if cleaned:
            return cleaned
        raise ValueError("No valid presets found")
    except Exception as error:
        print(f"Falling back to default presets: {error}")
        return DEFAULT_PRESETS.copy()


PRESETS = load_presets()

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

    CSS_PATH = "lofigirl.css"
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
                # If something goes wrong, print the error
                print(e)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_request_quit(self) -> None:
        """Push the quit screen."""
        self.push_screen(QuitScreen())


if __name__ == "__main__":
    app = LofiTUI()
    app.run()
