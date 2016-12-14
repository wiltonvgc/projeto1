#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb
import cgi
from ctypes import *
from socket import *
from thread import *


#Define funcao inicia conexao Socket Cliente TCP
def startClientSocket(host,port,msg):
	
	tcp = socket(AF_INET, SOCK_STREAM)
	destino = (host,port)

	tcp.connect(destino)

	tcp.send(msg)

	msg_recebida = tcp.recv(1024)

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
	check =  "{:016b}".format(header_checksum)
	source =  "{:032b}".format(source_address)
	dest = "{:032b}".format(destination_address)
	padd =  "{:08b}".format(padding)
	
	s = ''
	for c in options:
		s =  s + "{:08b}".format(ord(c))
	
	pacote = vers + ih + ts + tl + ide + fl + frag + time + prot + check + source + dest + s + padd
	return pacote


def main():
	#hablita cgi
	cgitb.enable() 

	host = '192.168.1.104' 


	#cabecalho obrigatorio de html
	print("Content-Type: text/html;charset=utf-8\r\n\r\n")

	form = cgi.FieldStorage()

	


	# Contrucao de pacote para MAQUINA 1 
	
	#COMANDO PS - MAQUINA 1	
	
	maq1_ps = form.getvalue("maq1_ps")
	maq1_ps_t = form.getvalue("maq1-ps")
	if(maq1_ps=='ps'):
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
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,msg)
			print(html)
			
		else:
			options = maq1_ps_t
			total_length = 21
			for caracter in maq1_ps_t:
				total_length = total_length + 1
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,msg)
			print(html)
			


	#COMANDO DF - MAQUINA 1	
	
	maq1_df = form.getvalue("maq1_df")
	maq1_df_t = form.getvalue("maq1-df")
	if(maq1_df=='df'):
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
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,msg)
			print(html)
		else:
			options = maq1_df_t
			total_length = 21
			for caracter in maq1_df_t:
				total_length = total_length + 1
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,msg)
			print(html)
	


	#COMANDO FINGER - MAQUINA 1	
	
	maq1_finger = form.getvalue("maq1_finger")
	maq1_finger_t = form.getvalue("maq1-finger")
	if(maq1_finger=='finger'):
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
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,msg)
			print(html)
		else:
			options = maq1_finger_t
			total_length = 21
			for caracter in maq1_finger_t:
				total_length = total_length + 1
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,html)
			print(html)


	#COMANDO UPTIME - MAQUINA 1	
	
	maq1_uptime = form.getvalue("maq1_uptime")
	maq1_uptime_t = form.getvalue("maq1-uptime")
	if(maq1_uptime=='uptime'):
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
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,msg)
			print(html)
		else:
			options = maq1_uptime_t
			total_length = 21
			for caracter in maq1_uptime_t:
				total_length = total_length + 1
			msg = criaPacote(version, ihl, type_of_service, total_length, identification,flags, fragment_offset,time_to_live, protocol, header_checksum, source_address, destination_address, options, padding)
			html = startClientSocket(host,9001,msg)
			print(html)




	
	
	
	

	
	

#chama funcao principal
main()
