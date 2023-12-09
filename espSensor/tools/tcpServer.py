import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 2000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Server started on port " + str(UDP_PORT))

while True:
    data, addr = sock.recvfrom(16) # buffer size is 8 bytes


    # Unpack the float datagram 
    unpackedData = struct.unpack('ffii', data)




    # Print the data
    print("Unpacked data: " + str(unpackedData))

    # Send a response
    sock.sendto(data, addr)