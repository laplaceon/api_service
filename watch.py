import os
import time
import requests
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define event handler
class MyHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer = []

    def send_buffer(self):
        if self.buffer:
            # Combine lines in buffer into one string
            try:
                # Send POST request with log data to server
                response = requests.post("http://localhost:8080/log-analysis/", json={"logs": self.buffer})
                print(f"Sent batch of logs to server, got response {response.status_code}")
            except Exception as e:
                print(f"Failed to send batch of logs to server: {e}")
            # Clear buffer
            self.buffer = []

    def on_modified(self, event):
        print(f'Event type: {event.event_type} path : {event.src_path}')
        if event.src_path.endswith('app.log'):
            print("app.log has been modified. Processing logs:")
            with open(event.src_path, 'r') as file:
                logs = file.readlines()  # Read log lines into a list
                # For every line in the log file
                for log in logs:
                    # Add the line to the buffer
                    self.buffer.append(log.strip())  # strip() to remove newline characters
                    # If the buffer has 50 lines, send it to the server
                    if len(self.buffer) >= 50:
                        self.send_buffer()

# Set observer to the path
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_handler.send_buffer()  # Send remaining logs if any
        observer.stop()
    observer.join()
