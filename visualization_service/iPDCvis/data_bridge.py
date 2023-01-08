import background_task
import socket
from collections import deque

databuffer = deque(maxlen=10000)


def dataparser(bytebuffer):
    # parse the data from the buffer
    # return a list of data

    # read the first byte to determine the type of data
    datatype = bytebuffer[0]


@background_task.background(schedule=0)
def listenToPort():
    global databuffer
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind the socket to the port
    server_address = ('127.0.0.1', 4433)
    sock.bind(server_address)

    while True:
        # receive incoming packets
        data, address = sock.recvfrom(4096)

        # turn data into integer
        data = int.from_bytes(data, byteorder='little')
        
        # print the contents of the packet
        print(f"received bytes from {address}: {data}")
        databuffer.append(data)
