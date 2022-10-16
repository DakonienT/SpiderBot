
import socket

 





serverAddressPort   = ("127.0.0.1", 20001)
# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
bufferSize          = 1024
while True:
    msgFromClient       = str(input("Message to send :"))
    bytesToSend         = str.encode(msgFromClient)

    # Send to server using created UDP socket

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    

    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)