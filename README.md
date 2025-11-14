# LofiTUI


A Textual TUI (Terminal User Interface) for playing YouTube lofi streams directly in your terminal using `mpv`. Enjoy your favorite lofi beats with ASCII art video, all from the comfort of your command line.

## Features

* **Curated Presets:** Easily switch between popular lofi streams like Lofi Girl, Synthwave, Christmas, and Jazz.
* **Custom URL Playback:** Paste any YouTube URL to play your own chosen stream.
* **Terminal-based Video:** Renders video as colored ASCII art using `mpv`'s `--vo=tct` output.
* **Audio Playback:** Streams audio in the background via `mpv`.
* **Interactive TUI:** Built with the `textual` library for a responsive and user-friendly experience.
* **Dark Mode:** Toggle dark mode for comfortable viewing.
* **Quit Confirmation:** Prevents accidental exits with a confirmation dialog.

## Screenshots

![LofiTUI main screen](lofi_tui1.png)
![LofiTUI playing a stream with ASCII art](lofi_tui2.png)

## Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3:** The application is written in Python.
* **`mpv`:** A free, open-source, and cross-platform media player. Install it using your system's package manager (e.g., `sudo apt install mpv` on Debian/Ubuntu, `sudo pacman -S mpv` on Arch Linux).

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bprendie/lofigirl.git
    cd lofitui
    ```

2.  **Install Python dependencies:**
    The project uses a virtual environment for managing dependencies.
    ```bash
    ./run.sh
    ```
    The `run.sh` script will automatically create a virtual environment, install the necessary Python packages (listed in `requirements.txt`), and then launch the application.

## Usage

To run the LofiTUI, simply execute the `run.sh` script:

```bash
./run.sh
