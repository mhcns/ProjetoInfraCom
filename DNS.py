from socket import *

dnsHost = '127.0.0.1'
dnsPort = 15000

dnsSocket = socket(AF_INET, SOCK_DGRAM)
dnsSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
dnsSocket.bind((dnsHost, dnsPort))
print('DNS Server ready!')

dic = dict()
while True:
    data, address = dnsSocket.recvfrom(1024)
    data_list = data.split()
    if len(data_list) == 2:
        dic[data_list[0]] = data_list[1]
        print('Registered {} as {}',data_list[0], data_list[1])
    elif len(data_list) == 1:
        if data_list[0] in dic:
            data += ' ' + dic[data_list[0]]
        print('Get {}',data_list[0])
    dnsSocket.sendto(data, address)
    print(dic)
