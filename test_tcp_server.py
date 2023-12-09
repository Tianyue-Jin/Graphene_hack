import socket

def test_tcp_server():
    server_ip = '127.0.0.1'
    server_port = 12345

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to the server at {server_ip}:{server_port}")

        # Send a test message to the server
        message = "Hello, server! This is a test message."
        client_socket.send(message.encode('utf-8'))
        print(f"Sent message to the server: {message}")

        # Receive the response from the server
        response = client_socket.recv(1024)
        print(f"Received response from the server: {response.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        client_socket.close()
        print("Client socket closed.")

if __name__ == "__main__":
    test_tcp_server()
