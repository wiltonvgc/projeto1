#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
from thread import *
import os
import subprocess

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

	#Comando FINGER
	elif(int(dic['protocol'],2)==3):
		html = maq + "<h2>### Comando FINGER :</h1>"
		if dic['options']:
			cmd = 'finger ' + dic['options']
		else:
			cmd = 'finger'

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


	#Comando UPTIME
	elif(int(dic['protocol'],2)==4):
		html = maq + "<h2>### Comando UPTIME :</h1>"
		if dic['options']:
			cmd = 'uptime ' + dic['options']
		else:
			cmd = 'uptime'

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
	else:
	     html = "<h1>" +  "NOT COMMAND" + "</h1>"	
	     
	return html

#Funcao que cria pacote de resposta
def criaPacoteResposta(mensagem, port):
	#obtem dicionario dos campos associados ao pacote recebeido	
	if mensagem:
		d = decodificaMensagem(mensagem)
	
	#verifica parametros maliciosos em options
	if '|' in d['options'] or ';' in d['options'] or '>' in d['options']:
		html = '<h3> PARAMETROS MALICIOSOS </h3>'
		return html

	else:
		html = criaPaginaResposta(d,port)
	 	return html
	
	
			
#Inicia daemon TCP com socket
def startServerTCP(host, port):

	tcp = socket(AF_INET,SOCK_STREAM)

	origem = (host,port)

	tcp.bind(origem)
	tcp.listen(1)

	while True:
		conexao, cliente = tcp.accept()
		mensagem = conexao.recv(1024)
		html = criaPacoteResposta(mensagem, port)
		conexao.send(html)
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
	
