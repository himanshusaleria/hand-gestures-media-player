# Hand Gesture Media Controller

Control your macOS media playback and system volume using simple hand gestures! This application uses your webcam and computer vision (MediaPipe) to detect hand movements and translate them into system commands.

## Features

- **Hands-Free Control**: Great for when you're away from the keyboard or your hands are busy.
- **Visual Feedback**: See your camera feed with gesture detection overlay.
- **System Integration**: Works with standard macOS media keys (Spotify, Apple Music, System Volume).

## Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| **Swipe Left** | Previous Song | Move hand quickly from Right to Left |
| **Swipe Right** | Next Song | Move hand quickly from Left to Right |
| **Swipe Up** | Volume Up | Move hand quickly Upwards |
| **Swipe Down** | Volume Down | Move hand quickly Downwards |
| **Fist / Clench** | Play / Pause | Clench your fingers into a fist |

## Prerequisites

- **macOS** (This project currently uses AppleScript `osascript` for system control)
- **Python 3.11** (Recommended for best compatibility with MediaPipe)
- A Webcam

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/himanshusaleria/hand-gestures-media-player.git
    cd hand-gestures-media-player
    ```

2.  **Set up a Virtual Environment (Recommended):**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This will install `opencv-python`, `mediapipe`, and `numpy`.*

## Usage

1.  **Run the application:**
    ```bash
    source venv/bin/activate  # If not already active
    python main.py
    ```

2.  **Permissions:**
    - On first run, macOS may ask for permission to access the **Camera**. Click **OK**.
    - It may also ask for **Accessibility** or **Automation** permissions to control System Events (Volume/Media). You must grant this access in `System Settings > Privacy & Security > Automation` (or Accessibility) for your Terminal or IDE.

3.  **To Quit:**
    - Press `q` while the camera window is focused.

## Troubleshooting

-   **"osascript is not allowed to send keystrokes":**
    -   This means the terminal running the script does not have Accessibility/Automation permissions. Go to System Settings -> Privacy & Security -> Accessibility and ensure your Terminal app (e.g., iTerm, Terminal, or VS Code) is checked. You may need to remove and re-add it if it's not working.
-   **Import Errors:**
    -   Ensure you are using the correct Python environment and have installed the requirements. MediaPipe works best with Python 3.8 - 3.11.

## License
[MIT](LICENSE)
