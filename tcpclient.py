import socket

# Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect(("127.0.0.1", 5000))

# Send data
client.send("Hello from client!".encode())

# Receive response
response = client.recv(1024).decode()
print("Server says:", response)

client.close()
