import socket

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to IP and port
server.bind(("127.0.0.1", 5000))

# Listen for connections
server.listen(5)
print("Server is listening on port 5000...")

while True:
    client_socket, addr = server.accept()
    print(f"Connected to {addr}")

    data = client_socket.recv(1024).decode()
    print("Received:", data)

    client_socket.send("Hello from server!".encode())

    client_socket.close()
