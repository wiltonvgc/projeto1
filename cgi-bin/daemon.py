from socket import *
from thread import *

#Funcao que reecebe mensagem de bits enviados e retorna dict com valores inteiros para cada campos do cabecalho
def decodificaMensagem(msg):
	dic = {}
	dic['version'] = msg[0:4]
	dic['ihl'] = msg[4:8]
	dic['type_of_service'] = msg[8:16]
	dic['total_length'] = msg[16:32]
	dic['identification'] = msg[32:48]
	dic['flags'] = msg[48:51]
	dic['fragment_offset'] = msg[51:64]
	dic['time_to_live'] = msg[64:72]
	dic['protocol'] = msg[73:81]
	dic['header_checksum'] = msg[81:97]
	dic['source_address'] = msg[97:129]
	dic['destination_address'] = msg[129:161]
	tamanho = len(msg)
	dic['options'] = msg[161:tamanho-8]
	dic['padding'] = msg[tamanho-8:tamanho]
	return dic

#Inicia daemon TCP com socket
def startServerTCP(host, port):

	tcp = socket(AF_INET,SOCK_STREAM)

	origem = (host,port)

	tcp.bind(origem)
	tcp.listen(1)

	while True:
		conexao, cliente = tcp.accept()
		mensagem = conexao.recv(1024)
		d = decodificaMensagem(mensagem)
		conexao.send("PROTOCOL : " + d['version'])
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
	
