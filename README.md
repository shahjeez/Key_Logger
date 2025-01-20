# Key Logger

Welcome to the **Key Logger** project! This Python-based application is designed to monitor and log key presses, mouse movements, and file activities on a target device. Use this tool responsibly and only in environments where you have explicit permission to monitor activity.

## Features

- **Keystroke Monitoring**: Logs all keyboard activity.
- **Mouse Position Tracking**: Records mouse movement and clicks.
- **File Activity Logging**: Tracks file changes, additions, and deletions.

## Prerequisites

Before running the program, ensure you have the following:

- **Python**: Version 3.7 or later installed on your system.
- **Required Libraries**: Install dependencies with the following command:

  ```bash
  pip install -r requirements.txt
  ```

## How to Use

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shahjeez/Key_Logger.git
   cd keyLogger
   ```

2. **Set Configuration**

   Edit the `server.py` and `key1.py` file to define the monitoring path, IP, and port:

3. **Run the Program**

   Start the key logger by executing the following command:

   ```bash
   python key1.py
   ```
   Start the server by executing the following command:
   
   ```bash
   python server.py
   ```
   
5. **Access Logs**

   Logs will be stored in a file named `dat.txt` in the root directory and will be sent to the server with the name `received_data.txt` . If remote logging is enabled, ensure the receiver is set up to handle data from the specified `IP` and `PORT`.

## Interactive Demonstration

1. **Real-time Logs**: Visualize keystrokes and mouse activity in real time by enabling the console output in `key1.py`.
2. **Live File Monitoring**: Test the file activity logging by creating, editing, or deleting files in the monitored directory.

## Disclaimer

This tool is intended for educational purposes and ethical use only. Unauthorized use of this software to monitor devices without consent is illegal and strictly prohibited.

## Contributing

Feel free to fork the repository and submit pull requests for any enhancements or bug fixes.



