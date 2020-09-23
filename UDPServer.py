from socket import *
import pickle 
import os

sendSeq = 0
sendACK = 0
expectedSeq = 0
expectedACK = 0

def rdtSend(serverSocket, clientAddress, message):
    global sendSeq
    global sendACK
    packet = (sendSeq, sendACK, message)   
    data = pickle.dumps(packet)
    serverSocket.sendto(data, clientAddress)
    while True:
        try:
            recvData = serverSocket.recvfrom(1024)
        except:
            print('temporizador estourou')
            serverSocket.sendto(data, clientAddress)
        else:
            recvSeq, recvACK, recvMessage = pickle.loads(recvData[0])
            if recvACK == sendACK:
                if sendACK == 0:
                    sendACK = 1
                    sendSeq = 1
                else:
                    sendACK = 0
                    sendSeq = 0
                return 

def rdtRecv(serverSocket):
    global expectedACK
    while True:
        try: 
            recvData = serverSocket.recvfrom(1024)
        except:
            print('still waiting')
        else:
            recvSeq, recvACK, recvMessage = pickle.loads(recvData[0])
            if recvSeq == expectedACK:
                packet = (expectedSeq, expectedACK, '')
                data = pickle.dumps(packet)
                serverSocket.sendto(data, recvData[1])
                if expectedACK == 0:
                    expectedACK = 1
                else:
                    expectedACK = 0
                return (recvMessage, recvData[1])
            else:
                if expectedACK == 0:
                    packet = (expectedSeq, 1, '')
                    data = pickle.dumps(packet)
                    serverSocket.sendto(data, recvData[1])
                else:
                    packet = (expectedSeq, 0, '')
                    data = pickle.dumps(packet)
                    serverSocket.sendto(data, recvData[1])

dnsPort = 15000
dnsHost = '127.0.0.1'

serverAlias = 'luneri.com'
serverPort = 12000
serverHost = '127.0.0.1'

dnsSocket = socket(AF_INET, SOCK_DGRAM)
message = serverAlias + ' ' + serverHost
dnsSocket.sendto(message, (dnsHost, dnsPort))
recvMessage = dnsSocket.recvfrom(1024)[0]
print(recvMessage)
dnsSocket.close()


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.settimeout(2.0)
serverSocket.bind((serverHost, serverPort))
print("The server is ready to recieve")

while True:
    message, clientAddress = rdtRecv(serverSocket)
    print('Got connection from ' + repr(clientAddress))
    print('Server recieved ' + message)
    rdtSend(serverSocket, clientAddress, 'Ready for requests')
    while True:
        op = rdtRecv(serverSocket)[0]
        if op == '1':
            dir_list = os.listdir('Arquivos')
            print(dir_list)
            files = ''
            for i in dir_list:
                files += './' + i + '\n'
            rdtSend(serverSocket, clientAddress, files)
            list_response = rdtRecv(serverSocket)[0]
            print(list_response)
        elif op == '2':
            rdtSend(serverSocket, clientAddress, 'Type file name: ')
            filename = rdtRecv(serverSocket)[0]
            f = open('Arquivos/' + filename, 'rb')
            l = f.read(1024)
            while(l):
                rdtSend(serverSocket, clientAddress, l)
                l = f.read(1024)
            f.close()
            rdtSend(serverSocket, clientAddress, "")
            print('Done Sending')
        elif op == '3':
            serverSocket.close()
            break