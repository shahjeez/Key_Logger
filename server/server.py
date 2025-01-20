import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   
    server_socket.bind(('IP', 'PORT')) # define your IP and PORT
    server_socket.listen(5) #5 devices can hear at a time
    print("Server listening on localhost")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection established from {addr}")

        with open('received_data.txt', 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)

        conn.close()
        print(f"File received successfully from {addr}")


if __name__ == "__main__":
    start_server()
