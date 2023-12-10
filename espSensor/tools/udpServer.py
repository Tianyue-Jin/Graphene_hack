import socket


UDP_IP = "192.168.4.2"
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Server started on port " + str(UDP_PORT))

while True:
    data, addr = sock.recvfrom(16) # buffer size is 8 bytes
    # Unpack the float datagram 
    # Print the data
    print("Unpacked data: " + str(data))

    # Send a response
    sock.sendto(data, addr)