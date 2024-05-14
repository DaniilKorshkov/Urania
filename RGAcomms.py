import socket
import sys

def SendPacketToRGA(package):
    HOST, PORT = "169.254.198.174", 10014
    data = str(package)+"       "

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data

        try:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(data + "\n", "utf-8"))
            received = str(sock.recv(1024), "utf-8")
        except:
            print(f"Connection to RGA refused")
            received = None

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))

    return(received)





#https://stackoverflow.com/questions/34653875/python-how-to-send-data-over-tcp
