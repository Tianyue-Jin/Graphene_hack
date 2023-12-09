import socket
import struct
import random
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 2000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Generate random float and integer values
    float1 = random.uniform(1.0, 10.0)
    float2 = random.uniform(1.0, 10.0)
    int1 = random.randint(1, 100)
    int2 = random.randint(1, 100)

    # Pack the random values into a binary format
    packed_data = struct.pack('ffii', float1, float2, int1, int2)

    # Send the packed data to the server
    sock.sendto(packed_data, (UDP_IP, UDP_PORT))

    # Print the values sent to the server
    print("Sent data: float1={}, float2={}, int1={}, int2={}".format(float1, float2, int1, int2))

    # Receive the response from the server
    response, addr = sock.recvfrom(16)

    # Print the response
    print("Server response: " + str(response))

    # Add a delay before sending the next set of random values
    time.sleep(1)
