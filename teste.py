from socket import *

serverName = ''
serverHost = '127.0.0.1'
serverPort = 12000

testSocket = socket(AF_INET, SOCK_DGRAM)
testSocket.settimeout(1.0)

while True:
    try:
        testSocket.recvfrom(1024)   
    except :
        print("timeout")
    