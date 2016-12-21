#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
from thread import *
import os
import subprocess

#Funcao que recebe um conjunto de bits como dados e retorna checksum de 16 bits a partir do calculo de crc
def crc16(data):
	num_bits_data = len(data)
	poli_crc16 = int('11000000000000101',2) #x16 + x15 + x2 + 1
	atual_data = data #atual_data guarda dados apos processamento de crc

	#executa algoritmo enquanto o numero de bits for diferente de 16
	while(len(atual_data)!=16):
		#se bit mais a esquerda e 1 faz xor com 17 mais significativos de data com polinomio e descarta bit mais significativo
		if(atual_data[0]=='1'):
			data_17 = int(atual_data[0:17],2)
			data_xor = data_17 ^ poli_crc16
			atual_data = "{:017b}".format(data_xor) + atual_data[17:]
			atual_data = atual_data[1:]
		else:
			#se bit mais a esquerda e 0, apenas descarta bit mais a esquerda
			atual_data = atual_data[1:]
		
	return atual_data

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
	dic['protocol'] = msg[72:80]
	dic['header_checksum'] = msg[80:96]
	dic['source_address'] = msg[96:128]
	dic['destination_address'] = msg[128:160]
	tamanho = len(msg)
	opcoes = msg[160:tamanho-8]
	dic['padding'] = msg[tamanho-8:tamanho]

	opcao = ''

	
	#tranforma bits de opcoes em string caracteres 
	if opcoes:
		j = 0
		k = 8
		nro_str = len(opcoes)/8
		l = []
		string = ''
		for i in range(nro_str):
			l = l + [opcoes[j:k]]
			j = k
			k = k + 8

		for st in l:
			string = string + chr(int(st,2))
		
		dic['options'] = string
	else:
		dic['options'] = ''
	
	return dic

#Funcao que cria pagina html com os resultados dos comandos a partir do dict de campos do cabeçalho
def criaPaginaResposta(dic,port):
	
	if(port == 9001):
		maq = "<h1 align = 'center' > MAQUINA 1 </h1>"
	if(port == 9002):
		maq = "<h1  align = 'center'> MAQUINA 2 </h1>"
	if(port == 9003):
		maq = "<h1  align = 'center'> MAQUINA 3 </h1>"
	
	#Comando PS
	if(int(dic['protocol'],2)==1):
		html = maq + "<h2> ### Comando PS : </h1>"
		if dic['options']:
			cmd = 'ps ' + dic['options']
		else:
			cmd = 'ps'

		f = os.popen(cmd) # roda comando PS
		out = f.read() # guarda em out saida de PS
		
		#separar strings de resultado de PS para fins de formatação
		# guarda indices de \n
		barra_n = []
		i = 0
		for c in out:
			if(c == '\n'):
				barra_n = barra_n + [i]
			i = i + 1
		
		#separa linhas de resultado
		i = 0
		linhas = [] #guarda linhas resultados
		for j in barra_n:
			linhas = linhas + [out[i:j]]
			i = j + 1

		#imprimi linhas em html
		for line in linhas:
			html = html + "<h3>" + line + "</h3>"
		
		html = html + "<h3>" + dic['options'] + "</h3>"


	#Comando DF
	elif(int(dic['protocol'],2)==2):
		html = maq + "<h2>### Comando DF : </h1>"
		if dic['options']:
			cmd = 'df ' + dic['options']
		else:
			cmd = 'df'

		f = os.popen(cmd) # roda comando PS
		out = f.read() # guarda em out saida de PS
		
		#separar strings de resultado de PS para fins de formatacao
		# guarda indices de \n
		barra_n = []
		i = 0
		for c in out:
			if(c == '\n'):
				barra_n = barra_n + [i]
			i = i + 1
		
		#separa linhas de resultado
		i = 0
		linhas = [] #guarda linhas resultados
		for j in barra_n:
			linhas = linhas + [out[i:j]]
			i = j + 1

		#imprimi linhas em html
		for line in linhas:
			html = html + "<h3>" + line + "</h3>"

	#Comando FINGER
	elif(int(dic['protocol'],2)==3):
		html = maq + "<h2>### Comando FINGER :</h1>"
		if dic['options']:
			cmd = 'finger ' + dic['options']
		else:
			cmd = 'finger'

		f = os.popen(cmd) # roda comando PS
		out = f.read() # guarda em out saida de PS
		
		#separar strings de resultado de PS para fins de formatacao
		# guarda indices de \n
		barra_n = []
		i = 0
		for c in out:
			if(c == '\n'):
				barra_n = barra_n + [i]
			i = i + 1
		
		#separa linhas de resultado
		i = 0
		linhas = [] #guarda linhas resultados
		for j in barra_n:
			linhas = linhas + [out[i:j]]
			i = j + 1

		#imprimi linhas em html
		for line in linhas:
			html = html + "<h3>" + line + "</h3>"


	#Comando UPTIME
	elif(int(dic['protocol'],2)==4):
		html = maq + "<h2>### Comando UPTIME :</h1>"
		if dic['options']:
			cmd = 'uptime ' + dic['options']
		else:
			cmd = 'uptime'

		f = os.popen(cmd) # roda comando PS
		out = f.read() # guarda em out saida de PS
		
		#separar strings de resultado de PS para fins de formatacao
		# guarda indices de \n
		barra_n = []
		i = 0
		for c in out:
			if(c == '\n'):
				barra_n = barra_n + [i]
			i = i + 1
		
		#separa linhas de resultado
		i = 0
		linhas = [] #guarda linhas resultados
		for j in barra_n:
			linhas = linhas + [out[i:j]]
			i = j + 1

		#imprimi linhas em html
		for line in linhas:
			html = html + "<h3>" + line + "</h3>"
	else:
	     html = "<h1>" +  "NOT COMMAND" + "</h1>"	
	     
	return html

def criaCabecalho(version, ihl, type_of_service, total_length, identification, flags, fragment_offset, time_to_live, protocol, header_checksum, source_address, destination_address, options, padding):
	vers = "{:04b}".format(version)
	ih =  "{:04b}".format(ihl)
	ts =  "{:08b}".format(type_of_service)
	tl = "{:016b}".format(total_length)
	ide =  "{:016b}".format(identification)
	fl =  "{:03b}".format(flags)
	frag =  "{:013b}".format(fragment_offset)
	time =  "{:08b}".format(time_to_live)
	prot =  "{:08b}".format(protocol)
	check =  "{:016b}".format(header_checksum)
	source =  "{:032b}".format(source_address)
	dest = "{:032b}".format(destination_address)
	padd =  "{:08b}".format(padding)
	
	s = ''
	
	#se options esta vazio zera 32 bits
	if not options:
		s = "{:032b}".format(0)	
	else:
		for c in options:
			s =  s + "{:08b}".format(ord(c))
	
	cabecalho = vers + ih + ts + tl + ide + fl + frag + time + prot + check + source + dest + s + padd
	return cabecalho

#Funcao que cria pacote de resposta
def criaPacoteResposta(mensagem, port):
		
	if(port == 9001):
		maq = "<h1 align = 'center' > MAQUINA 1 </h1>"
	if(port == 9002):
		maq = "<h1  align = 'center'> MAQUINA 2 </h1>"
	if(port == 9003):
		maq = "<h1  align = 'center'> MAQUINA 3 </h1>"

	if mensagem:
		d = decodificaMensagem(mensagem)#obtem dicionario dos campos associados ao pacote recebeido
		# set campos do cabeçalho do pacote de resposta
		version = 2
		ihl = 15
		type_of_service = 0
		identification = int(d['identification']) + 1
		flags = 7
		fragment_offset = 0
		time_to_live = int(d['time_to_live']) - 1
		protocol = int(d['protocol'],2)
		header_checksum = 0
		source_address = 3232235879
		destination_address = 3232235881
		options = ''
		padding = 0
		
		if(protocol==1):
			comando_html = "<h2> ###Comando PS:</h2>"
		elif(protocol==2):
			comando_html = "<h2> ###Comando DF:</h2>"
		elif(protocol==3):
			comando_html = "<h2> ###Comando FINGER:</h2>"
		elif(protocol==4):
			comando_html = "<h2> ###Comando UPTIME:</h2>"
		
		#obtem cheksum de mensagem recebida para verificacao
		checksum_rec = crc16(mensagem[0:80]+mensagem[96:])
		
		#verifica parametros maliciosos em campo options
		if '|' in d['options'] or ';' in d['options'] or '>' in d['options']:
			html = maq + comando_html + '<h3> PARAMETROS MALICIOSOS </h3>'		
		#verifica se campo flags e de envio : 000
		elif d['flags'] != '000':
			html =maq +  comando_html + '<h3> FLAG NAO COMPATIVEL PARA ENVIO </h3>'
		#verifica se campo version e 2
		elif d['version'] != '0010':
			html = maq + comando_html + '<h3> ERRO DE VERSAO </h3>'
		#verifica campo de checksum
		elif d['header_checksum']!=checksum_rec:
			html = maq + comando_html + '<h3> ERRO DE CHECKSUM DE ENVIO </h3>'
		else:
			html = criaPaginaResposta(d,port)
		

		#transforma pagina html em bits para envio junto ao cabeçalho
		s = ''
		t = 0
		for c in html:
			if(c!=''):
				s =  s + "{:08b}".format(ord(c))
			t = t + 1
		
		total_length = 24 + t
		cabecalho = criaCabecalho(version,ihl,type_of_service,total_length, identification, flags,fragment_offset, time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
		pacote_resposta = cabecalho + s
		return pacote_resposta
	
			
#Inicia daemon TCP com socket
def startServerTCP(host, port):

	tcp = socket(AF_INET,SOCK_STREAM)

	origem = (host,port)

	tcp.bind(origem)
	tcp.listen(1)

	while True:
		conexao, cliente = tcp.accept()
		mensagem = conexao.recv(5000)
		pacote = criaPacoteResposta(mensagem, port)
		conexao.send(pacote)
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
	
