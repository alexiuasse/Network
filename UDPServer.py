from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))          #associa porta com uma determinada interface de rede
print("The server is ready to receive!")

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.upper()
    print (clientAddress)
    print (modifiedMessage)
    serverSocket.sendto(modifiedMessage, clientAddress)