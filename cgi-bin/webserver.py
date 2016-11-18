#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb
import cgi
from ctypes import *
from socket import *


#Define funcao inicia conexao Socket Cliente TCP
def startClientSocket(host,port,msg):
	
	tcp = socket(AF_INET, SOCK_STREAM)
	destino = (host,port)

	tcp.connect(destino)
	
	

	tcp.send(msg)

	msg_recebida = tcp.recv(1024)

	tcp.close()
	
	return msg_recebida


#Define estrutura para cabeçalho do pacote de dados
class Header(Structure):
	_fields_ = [("version",c_uint,4), ("ihl",c_uint,4), ("type-of-service",c_uint,8), ("total-lenght",c_uint,16), ("identification",c_uint,16), ("flags",c_uint, 3), ("fragment-offset",c_uint,13), ("time-to-live",c_uint,16), ("protocol",c_uint,8),
("header-checksum",c_uint,16), ("source-address",c_uint,32), ("destination-address",c_uint,32), ("options",c_wchar_p), ("padding",c_uint,8)]

#Define lista de campos do cabeçalho
fields_header = ['version','ihl','type-of-service', 'total-length', 'identification', 'flags', 'fragment-offset', 'time-to-live', 'protocol', 'header-checksum', 'source-address', 'destination-address', 'options', 'padding']




#Define funcao que constroi cabeçalho para envio. values: dict => {campo : valor }
def buildPackageRequest(values):

	#Set valores de campos do cabeçalho	
	version = values['version']
	ihl = values['ihl']
	type_of_service = values['type-of-service']
	total_lenght = values['total-length']
	identification = values['identification']
	flags = values['flags']
	fragment_offset = values['fragment-offset']
	time_to_live = values['time-to-live']
	protocol = values['protocol']
	header_checksum = values['header-checksum']
	source_address = values['source-address']
	destination_address = values['destination-address']
	options = values['options']
	padding = values['padding']
	
	#Controi estrutura de campos de bits Header para cabeçalho
	package = Header(version, ihl, type_of_service, total_lenght, identification, flags, fragment_offset, time_to_live, protocol, header_checksum, source_address, destination_address,options, padding)
	return package

#Define funcao que constroi dict com campos de um form cgi para posterior contrucao do cabecalho
def buildDictFields(version, ihl, type_of_service, total_lenght, identification, flags, fragment_offset, time_to_live, protocol, header_checksum, source_address, destination_address, options, padding):
	
	values = {}.fromkeys(fields_header)
	values['version'] = version
	values['ihl'] = ihl
	values['type-of-service'] = type_service
	values['total-length'] = total_lenght
	values['identification'] = identification
	values['flags'] = flags
	values['fragment-offset'] = fragment_offset
	values['time-to-live'] = time_to_live
	values['protocol'] = protocol
	values['header-checksum'] = header_checksum
	values['source-address'] = source_address
	values['destination-address'] = destination_address
        values['options'] = options
	values['padding'] = padding
	return values
	

def main():
	#hablita cgi
	cgitb.enable()    


	#cabecalho obrigatorio de html
	print("Content-Type: text/html;charset=utf-8\r\n\r\n")

	form = cgi.FieldStorage()

	#Maquina 1 
	#maq1_ps = form.getvalue("maq1_ps")
	#maq1_ps_t = form.getvalue("maq1-ps")

	#print(maq1_ps_t)
	
	#maq1_df = form["maq1_df"].value
	#maq1_df_t = form["maq1-df"].value

	#maq1_finger = form["maq1_finger"].value
	#maq1_finger_t = form["maq1-finger"].value

	#maq1_uptime = form["maq1_uptime"].value
	#maq1_uptime_t = form["maq1-uptime"].value

	msg = startClientSocket('192.168.1.102',9001,"msg1")
	print(msg)
	msg = startClientSocket('192.168.1.102',9001,"msg2")
	print(msg)
	
	msg = startClientSocket('192.168.1.102',9002,"msg3")
	print(msg)
	msg = startClientSocket('192.168.1.102',9002,"msg4")
	print(msg)


	
	
	
	

	
	

#chama funcao principal
main()
