from socket import *

#172.22.70.249

serverName = ''
serverHost = ''
serverPort = 12000

dnsHost = '127.0.0.1'
dnsPort = 15000

dnsSocket = socket(AF_INET, SOCK_DGRAM)
serverName = raw_input('Insira o nome do servidor que vc quer se conectar: ')
dnsSocket.sendto(serverName, (dnsHost, dnsPort))
query = dnsSocket.recvfrom(1024)[0]
print(query)
serverHost = query.split()[1]
dnsSocket.close()

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

def get_list():
	listinha = clientSocket.recv(1024)
	print(listinha)
	clientSocket.send('Received List')

# def get_file(message):	

def close_connection():
	clientSocket.close()


def main():
	sentence = 'Hello Server'
	clientSocket.send(sentence)
	print('From server: ' + clientSocket.recv(1024))

	while 1:
	
		op = input('1. Receber lista de arquivos\n2. Requisitar arquivo\n3. Encerrar conexao\nDigite a operacao desejada:')

		if op == 1:
			clientSocket.send(repr(op))
			get_list()
		elif op == 2:
			clientSocket.send(repr(op))
			message = clientSocket.recv(1024)
			file_name = raw_input(message)
			clientSocket.send(file_name)
			filesize = int(clientSocket.recv(1024))
			print(filesize)
			clientSocket.send('Size recieved. Client ready.')
			f = open('Downloads/' + file_name,'wb')
			bytes_recieved = 0
			while bytes_recieved < filesize:
				print('Receiving Data...')
				data = clientSocket.recv(min(filesize - bytes_recieved, 1024))
				# print(data)
				print(bytes_recieved)
				if not data:
					break
				f.write(data)
				bytes_recieved += len(data)
			f.close()
			print('File Received')
		elif op == 3:
			clientSocket.send(repr(op))
			close_connection()
			break
		else:
			print('Digite uma opcao valida.')
	

if __name__ == "__main__":
	main()