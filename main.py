import io, os, sys
import base64
import requests
import pyautogui
import threading
from PIL import Image, ImageGrab
from pystray import Icon, MenuItem as item, Menu
import tkinter as tk
from tkinter import scrolledtext, Toplevel

import win32event
import win32api
from winerror import ERROR_ALREADY_EXISTS
from tkinter import messagebox

# Create a named mutex that's unique to your application
mutex = win32event.CreateMutex(None, False, 'Global\\YourAppUniqueMutexName')

# Check if the mutex is already exists which indicates another instance is running
last_error = win32api.GetLastError()
if last_error == ERROR_ALREADY_EXISTS:
  messagebox.showinfo("Instance Already Running", "Another instance of the app is already running.")
  sys.exit(0)  # Exit the program if instance is already running


# Use a global variable for the root window
root = tk.Tk()
root.withdraw()  # Hide the root window as it is not needed



# Determine if we're running in a bundle or a live Python environment
if getattr(sys, 'frozen', False):
    # If the application is running in a bundle, set the base directory
    # to the sys._MEIPASS directory (PyInstaller sets this attribute)
    basedir = sys._MEIPASS
else:
    # If it's not bundled, use the current directory
    basedir = os.path.dirname(__file__)


# Function to create a loading window
def create_loading_window():
    loading_window = Toplevel(root)
    loading_window.title("Processing...")
    loading_label = tk.Label(loading_window, text="Processing the screenshot, please wait...")
    loading_label.pack(padx=20, pady=20)
    # Keep the loading window always on top
    loading_window.attributes("-topmost", True)
    return loading_window


# Function to simulate 'Win + Shift + S' key press
def invoke_snipping_tool():
    pyautogui.hotkey('win', 'shift', 's')

# Function to check and get image from clipboard
def get_image_from_clipboard():
    threading.Event().wait(5)
    image = ImageGrab.grabclipboard()
    if isinstance(image, Image.Image):
        return image
    return None

# Function to encode the image
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to send image to OpenAI Vision API
def send_to_openai_vision_api(base64_image):
    # api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual OpenAI API key
    api_key = "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"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Function to display the response in a pop-up window
def display_response(response, loading_window):
    # Destroy the loading window
    loading_window.destroy()
    
    # Create a new Tkinter window
    response_window = Toplevel(root)
    response_window.title("OpenAI Vision API Response")
    
    # Create a ScrolledText widget
    text_area = scrolledtext.ScrolledText(response_window, wrap=tk.WORD)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    # Insert the response text into the widget
    text_area.insert(tk.INSERT, response)
    
    # Make the text widget read-only (to allow text selection and copying)
    text_area.config(state=tk.DISABLED)

# Function triggered by system tray icon click
def on_clicked(icon):
    # Show loading window
    loading_window = create_loading_window()
    invoke_snipping_tool()
    thread = threading.Thread(target=process_screenshot, args=(loading_window,))
    thread.start()

# Function to process the screenshot
def process_screenshot(loading_window):
    image = get_image_from_clipboard()
    if image:
        base64_image = encode_image(image)
        response = send_to_openai_vision_api(base64_image)
        # Switch from the loading window to the response window
        text = response.get("choices")[0].get("message").get("content")
        display_response(str(text), loading_window)

# Function to safely exit the application
def exit_action(icon):
  messagebox.showinfo("Exit", "Exit the application")
  root.quit()  # Ensure the Tkinter root is destroyed to clean up
  icon.stop()
  sys.exit(0)  # Exit the application


# Setup the menu for the system tray icon
menu = Menu(
  item('Capture & Send', on_clicked),
  item('Exit', exit_action)
)

def setup(icon):
    icon.visible = True

# System tray icon setup
icon_path = os.path.join(basedir, 'icon.png')
    
icon = Icon("test_icon", Image.open(icon_path), "Screenshot Tool", menu=menu)

# Run the icon in a thread to prevent blocking
icon_thread = threading.Thread(target=icon.run, args=(setup,))
icon_thread.start()

# Start the main Tkinter loop in a way that it doesn't block
root.mainloop()
