from socket import*
import pickle

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
            print('temporizador estourou')
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

serverName = ''
serverHost = ''
serverPort = 12000

dnsPort = 15000
dnsHost = '127.0.0.1'

dnsSocket = socket(AF_INET, SOCK_DGRAM)
serverName = raw_input('Insira o nome do servidor que vc quer se conectar: ')
dnsSocket.sendto(serverName, (dnsHost, dnsPort))
query = dnsSocket.recvfrom(1024)[0]
serverHost = query.split()[1]
dnsSocket.close()

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = 'Hello Server!'
rdtSend(clientSocket, (serverHost, serverPort), message)
message = rdtRecv(clientSocket)[0]
print('From server: ' + message)

while True:
    op = input('1. Receber lista de arquivos\n2. Requisitar arquivo\n3. Encerrar conexao\nDigite a operacao desejada:')
    if op == 1:
        rdtSend(clientSocket, (serverHost, serverPort), repr(op))
        listinha = rdtRecv(clientSocket)[0]
        print(listinha)
        rdtSend(clientSocket, (serverHost, serverPort), 'Recieved List')
    elif op == 2:
        #le 2048 bytes, joga numa string
        #se a string for vazia, acabei de ler o arquivo
        #manda string vazia

        #ler enquanto o q leu n for uma string vazia


        rdtSend(clientSocket, (serverHost, serverPort), repr(op))
        message = rdtRecv(clientSocket)[0]
        filename = raw_input(message)
        rdtSend(clientSocket, (serverHost, serverPort), filename)
        f = open('Downloads/' + filename,'wb')
        while 1:
            print('Receiving Data...')
            data = rdtRecv(clientSocket)[0]
            if data == "":
                break
            f.write(data)
        f.close()
        print('File Received')
    elif op == 3:
        rdtSend(clientSocket, (serverHost, serverPort), repr(op))
        clientSocket.close()
        break