from socket import *
from thread import *

#Inicia daemon TCP com socket
def startServerTCP(host, port):

	tcp = socket(AF_INET,SOCK_STREAM)

	origem = (host,port)

	tcp.bind(origem)
	tcp.listen(1)

	while True:
		conexao, cliente = tcp.accept()
		mensagem = conexao.recv(1024)
		conexao.send(mensagem)
		conexao.close()
			


def main():
	host = ''

	#Cria uma thread para cada porta
	try:
		start_new_thread(startServerTCP, (host,9001,))
		start_new_thread(startServerTCP, (host,9002,))
		start_new_thread(startServerTCP, (host,9003,))
	except:
		print("Nao foi possivel criar threads")
	
	while True:
		pass

main()
	
