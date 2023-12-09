import socket

# Define the server's IP address and port
server_ip = '127.0.0.1'  # Loopback address for localhost
server_port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections (max 5 connections in the queue)
server_socket.listen(5)
print(f"Server listening on {server_ip}:{server_port}")

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Receive data from the client
    data = client_socket.recv(1024)
    if not data:
        break  # Exit the loop if no data is received

    # Process the received data (you can replace this with your own logic)
    print(f"Received data: {data.decode('utf-8')}")

    # Send a response back to the client
    response = "Hello, client! Your message was received."
    client_socket.send(response.encode('utf-8'))

    # Close the connection with the client
    client_socket.close()

# Close the server socket
server_socket.close()
