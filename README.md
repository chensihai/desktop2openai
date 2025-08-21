# Desktop2OpenAI

A Windows desktop application that provides quick screenshot analysis using OpenAI's Vision API. Simply capture any part of your screen and get AI-powered insights instantly through a convenient system tray interface.

## Features

- **System Tray Integration**: Runs quietly in the background with easy access from the system tray
- **Quick Screenshot Capture**: Uses Windows' built-in Snipping Tool (Win + Shift + S) for seamless screenshot capture
- **Keyboard Shortcut**: Press `Ctrl + M` to quickly capture and analyze screenshots
- **OpenAI Vision API**: Leverages GPT-4 Vision to analyze and describe screenshot contents
- **User-Friendly Interface**: Clean popup windows display AI analysis results
- **Settings Management**: Easy API key configuration through a settings dialog
- **Single Instance**: Prevents multiple instances from running simultaneously

## Prerequisites

- Windows operating system
- Python 3.7 or higher
- OpenAI API key

## Installation

1. **Clone or download this repository**

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key**:
   - Run the application and click on "Settings" in the system tray menu
   - Enter your OpenAI API key and save

## Usage

### Running the Application

```bash
python main.py
```

The application will start and appear as an icon in your system tray.

### Capturing and Analyzing Screenshots

1. **Using the System Tray**: Right-click the tray icon and select "Capture & Send"
2. **Using Keyboard Shortcut**: Press `Ctrl + M` anywhere on your system
3. **Screenshot Process**: 
   - The Windows Snipping Tool will open automatically
   - Select the area you want to analyze
   - The screenshot will be sent to OpenAI's Vision API
   - Results will appear in a popup window

### Settings

Access settings by right-clicking the system tray icon and selecting "Settings". Here you can:
- Configure your OpenAI API key
- The API key is stored locally in [`api_key.txt`](api_key.txt)

## Building an Executable

To create a standalone executable file:

```bash
pyinstaller main.py --onefile --add-data="./icon.png;."
```

This will create a single executable file in the `dist` folder that can be run without Python installed.

## Project Structure

- [`main.py`](main.py) - Main application code
- [`requirements.txt`](requirements.txt) - Python dependencies
- [`icon.png`](icon.png) - System tray icon image
- `api_key.txt` - Your OpenAI API key (created after first setup)

## Dependencies

Key dependencies include:
- `openai` - OpenAI API client
- `pystray` - System tray functionality
- `pyautogui` - Screenshot automation
- `pillow` - Image processing
- `tkinter` - GUI components
- `keyboard` - Global hotkey support
- `pywin32` - Windows-specific functionality

See [`requirements.txt`](requirements.txt) for the complete list of dependencies.

## Troubleshooting

- **"Instance Already Running" message**: The application prevents multiple instances. Close the existing instance before starting a new one.
- **API key issues**: Make sure your OpenAI API key is valid and has sufficient credits.
- **Screenshot not captured**: Ensure you complete the screenshot selection in the Snipping Tool before the timeout period.

## License

This project is open source. Feel free to modify and distribute as needed.