#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb
import cgi
from ctypes import *
from socket import *
from thread import *

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

#Funcao que reecebe mensagem de bits enviados e retorna html para ser impresso 
def decodificaMensagem(pacote_obtido,pacote_envio,port):
	dic = {}
	dic['version'] = pacote_obtido[0:4]
	dic['ihl'] = pacote_obtido[4:8]
	dic['type_of_service'] = pacote_obtido[8:16]
	dic['total_length'] = pacote_obtido[16:32]
	dic['identification'] = pacote_obtido[32:48]
	dic['flags'] = pacote_obtido[48:51]
	dic['fragment_offset'] = pacote_obtido[51:64]
	dic['time_to_live'] = pacote_obtido[64:72]
	dic['protocol'] = pacote_obtido[72:80]
	dic['header_checksum'] = pacote_obtido[80:96]
	dic['source_address'] = pacote_obtido[96:128]
	dic['destination_address'] = pacote_obtido[128:160]
	dic['opcoes'] = pacote_obtido[160:160]
	dic['padding'] = pacote_obtido[160:168]
	tamanho = len(pacote_obtido)
	html_bin = pacote_obtido[168:tamanho]#guarda versao binaria de html
	protocol = int(dic['protocol'],2)#guarda versao numerica de protocol
	
	if(port==9001):
		comando_html = "<h1 align='center'> MAQUINA 1 </h1>"
	elif(port==9002):
		comando_html = "<h1 align='center'> MAQUINA 2 </h1>"
	elif(port==9003):
		comando_html = "<h1 align='center'> MAQUINA 3 </h1>"

	if(protocol==1):
		comando_html = comando_html + "<h2> ###Comando PS:</h2>"
	elif(protocol==2):
		comando_html = comando_html + "<h2> ###Comando DF:</h2>"
	elif(protocol==3):
		comando_html = comando_html + "<h2> ###Comando FINGER:</h2>"
	elif(protocol==4):
		comando_html = comando_html + "<h2> ###Comando UPTIME:</h2>"
		
	
	html = ''#guarda html obtido para ser impresso
	
	#tranforma bits de campo de dados html em string caracteres 
	if html_bin:
		j = 0
		k = 8
		nro_str = len(html_bin)/8
		l = []
		string = ''
		for i in range(nro_str):
			l = l + [html_bin[j:k]]
			j = k
			k = k + 8

		for st in l:
			string = string + chr(int(st,2))
			
		html = string
	
	#verificacoes de campo time_to_live e identification
	dic_envio = {}
	dic_envio['time_to_live'] = pacote_envio[64:72]
	dic_envio['identification'] = pacote_envio[32:48]

	if (int(dic_envio['time_to_live'],2)!=(int(dic['time_to_live'],2)+1)):
		html = comando_html + "<h3> ERRO DE TIME LIVE </h3>"
	elif(int(dic_envio['identification'],2)!=(int(dic['identification'],2)-1)):
		html = comando_html + "<h3> ERRO DE IDENTIFICATION </h3>"
	elif(dic['flags']!='111'):
		html = comando_html + "<h3> ERRO DE FLAG </h3>"

	#verificacao de checksum de mensagem recebida
	checksum_rec = dic['header_checksum'] #checksum recebido no campo da mensagem recebida
	
	#mensagem recebida sem campo de checksum
	m = dic['version'] + dic['ihl'] + dic['type_of_service'] + dic['total_length'] + dic['identification'] + dic['flags'] + dic['fragment_offset'] + dic['time_to_live'] + dic['protocol'] + dic['source_address']  + dic['destination_address'] + dic['padding'] + html_bin		
	
	checksum = crc16(m) #calcula checksum da mensagem recebida

	#compara checksum recebido com o calculado 
	if(checksum!=checksum_rec):
		html = comando_html + "<h3> ERRO DE CHECKSUM NA RESPOSTA  </h3>"
		
	
	
	return html

#Define funcao inicia conexao Socket Cliente TCP
def startClientSocket(host,port,msg):
	
	tcp = socket(AF_INET, SOCK_STREAM)
	destino = (host,port)

	tcp.connect(destino)

	tcp.send(msg)

	msg_recebida = tcp.recv(8096)

	tcp.close()
	
	return msg_recebida


#Define funcao que cria pacote para envio 
#Entrada: recebe campos do cabecalho
#Retorno: string de bits relativos aos campos respeitando o cabeçalho padrao
def criaPacote(version, ihl, type_of_service, total_length, identification, flags, fragment_offset, time_to_live, protocol, header_checksum, source_address, destination_address, options, padding):
	vers = "{:04b}".format(version)
	ih =  "{:04b}".format(ihl)
	ts =  "{:08b}".format(type_of_service)
	tl = "{:016b}".format(total_length)
	ide =  "{:016b}".format(identification)
	fl =  "{:03b}".format(flags)
	frag =  "{:013b}".format(fragment_offset)
	time =  "{:08b}".format(time_to_live)
	prot =  "{:08b}".format(protocol)
	source =  "{:032b}".format(source_address)
	dest = "{:032b}".format(destination_address)
	padd =  "{:08b}".format(padding)
	

	s = ''
	for c in options:
		s =  s + "{:08b}".format(ord(c))
	
	#calculo de crc para dados a serem enviados
	m =  vers + ih + ts + tl + ide + fl + frag + time + prot + source + dest + s + padd
	check =  crc16(m)
		
	#pacote final de envio
	pacote = vers + ih + ts + tl + ide + fl + frag + time + prot + check + source + dest + s + padd
	return pacote

def threadMaq1(form,host,port):
		
	tem_comando = False
	# Contrucao de pacote para MAQUINA 1 
	
	#COMANDO PS - MAQUINA 1	
	
	maq1_ps = form.getvalue("maq1_ps")
	maq1_ps_t = form.getvalue("maq1-ps")
	if(maq1_ps=='ps'):
		tem_comando = True
		protocol = 1
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq1_ps_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
			
		else:
			options = maq1_ps_t
			total_length = 21
			for caracter in maq1_ps_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
			
			


	#COMANDO DF - MAQUINA 1	
	
	maq1_df = form.getvalue("maq1_df")
	maq1_df_t = form.getvalue("maq1-df")
	if(maq1_df=='df'):
		tem_comando = True
		protocol = 2
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq1_df_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq1_df_t
			total_length = 21
			for caracter in maq1_df_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
	


	#COMANDO FINGER - MAQUINA 1	
	
	maq1_finger = form.getvalue("maq1_finger")
	maq1_finger_t = form.getvalue("maq1-finger")
	if(maq1_finger=='finger'):
		tem_comando = True
		protocol = 3
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq1_finger_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq1_finger_t
			total_length = 21
			for caracter in maq1_finger_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)

	#COMANDO UPTIME - MAQUINA 1	
	
	maq1_uptime = form.getvalue("maq1_uptime")
	maq1_uptime_t = form.getvalue("maq1-uptime")
	if(maq1_uptime=='uptime'):
		tem_comando = True
		protocol = 4
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq1_uptime_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq1_uptime_t
			total_length = 21
			for caracter in maq1_uptime_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)

	
	#Verifica se nenhum opcao de comando foi selecionada
	if not tem_comando:
		protocol = 0
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		total_length = 24 #bytes
		pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
		pacote_obtido = startClientSocket(host,port,pacote_envio)
		html = decodificaMensagem(pacote_obtido,pacote_envio,port)
		print(html)

def threadMaq2(form,host,port):

	tem_comando = False		

	# Contrucao de pacote para MAQUINA 2
	
	#COMANDO PS - MAQUINA 2
	
	maq2_ps = form.getvalue("maq2_ps")
	maq2_ps_t = form.getvalue("maq2-ps")
	if(maq2_ps=='ps'):
		tem_comando = True
		protocol = 1
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq2_ps_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
			
		else:
			options = maq2_ps_t
			total_length = 21
			for caracter in maq2_ps_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
			
			


	#COMANDO DF - MAQUINA 2
	
	maq2_df = form.getvalue("maq2_df")
	maq2_df_t = form.getvalue("maq2-df")
	if(maq2_df=='df'):
		tem_comando = True
		protocol = 2
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq2_df_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq2_df_t
			total_length = 21
			for caracter in maq2_df_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
	


	#COMANDO FINGER - MAQUINA 2	
	
	maq2_finger = form.getvalue("maq2_finger")
	maq2_finger_t = form.getvalue("maq2-finger")
	if(maq2_finger=='finger'):
		tem_comando = True
		protocol = 3
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq2_finger_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq2_finger_t
			total_length = 21
			for caracter in maq2_finger_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)

	#COMANDO UPTIME - MAQUINA 2	
	
	maq2_uptime = form.getvalue("maq2_uptime")
	maq2_uptime_t = form.getvalue("maq2-uptime")
	if(maq2_uptime=='uptime'):
		tem_comando = True
		protocol = 4
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq2_uptime_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq2_uptime_t
			total_length = 21
			for caracter in maq2_uptime_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)


	#Verifica se nenhum opcao de comando foi selecionada
	if not tem_comando:
		protocol = 0
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		total_length = 24 #bytes
		pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
		pacote_obtido = startClientSocket(host,port,pacote_envio)
		html = decodificaMensagem(pacote_obtido,pacote_envio,port)
		print(html)

	
def threadMaq3(form,host,port):
		
	tem_comando = False
	# Contrucao de pacote para MAQUINA 1 
	
	#COMANDO PS - MAQUINA 3
	
	maq3_ps = form.getvalue("maq3_ps")
	maq3_ps_t = form.getvalue("maq3-ps")
	if(maq3_ps=='ps'):
		tem_comando = True
		protocol = 1
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq3_ps_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
			
		else:
			options = maq3_ps_t
			total_length = 21
			for caracter in maq3_ps_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
			
			


	#COMANDO DF - MAQUINA 3	
	
	maq3_df = form.getvalue("maq3_df")
	maq3_df_t = form.getvalue("maq3-df")
	if(maq3_df=='df'):
		tem_comando = True
		protocol = 2
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq3_df_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq3_df_t
			total_length = 21
			for caracter in maq3_df_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
	


	#COMANDO FINGER - MAQUINA 3	
	
	maq3_finger = form.getvalue("maq3_finger")
	maq3_finger_t = form.getvalue("maq3-finger")
	if(maq3_finger=='finger'):
		tem_comando = True
		protocol = 3
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq3_finger_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq3_finger_t
			total_length = 21
			for caracter in maq3_finger_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)

	#COMANDO UPTIME - MAQUINA 3
	maq3_uptime = form.getvalue("maq3_uptime")
	maq3_uptime_t = form.getvalue("maq3-uptime")
	if(maq3_uptime=='uptime'):
		tem_comando = True
		protocol = 4
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		# se parametros estao vazios
		if not maq3_uptime_t:
			total_length = 24 #bytes
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)
		else:
			options = maq3_uptime_t
			total_length = 21
			for caracter in maq3_uptime_t:
				total_length = total_length + 1
			pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			pacote_obtido = startClientSocket(host,port,pacote_envio)
			html = decodificaMensagem(pacote_obtido,pacote_envio,port)
			print(html)

	#Verifica se nenhum opcao de comando foi selecionada
	if not tem_comando:
		protocol = 0
		version = 2
		ihl = 15
		type_of_service = 0
		identification = 1
		flags = 0
		fragment_offset = 0
		time_to_live = 1
		source_address = 3232235881
		destination_address = 3232235879
		header_checksum = 0
		options = ""
		padding = 0
		total_length = 24 #bytes
		pacote_envio = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
		pacote_obtido = startClientSocket(host,port,pacote_envio)
		html = decodificaMensagem(pacote_obtido,pacote_envio,port)
		print(html)


def main():
	#hablita cgi
	cgitb.enable() 

	host = '192.168.1.101' 


	#cabecalho obrigatorio de html
	print("Content-Type: text/html;charset=utf-8\r\n\r\n")

	form = cgi.FieldStorage()
	
	threadMaq1(form,host,9001)
	threadMaq2(form,host,9002)
	threadMaq3(form,host,9003)
	
	
	
#chama funcao principal
main()
