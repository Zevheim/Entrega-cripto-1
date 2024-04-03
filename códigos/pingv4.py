import sys
import os
import time
import struct

from scapy.all import sr1, IP, ICMP,send, Ether
 
#a=IP()/ICMP()
#print(sys.argv[1])
id_paquete=os.getpid() & 0xFFFF #manera de generar un identificador unico utilizando el pid
tiempo=time.time()              #este valor se utiliza para el timestamp
for z in range(len(sys.argv[1])):
    timestamp_bytes=struct.pack('<Q', int(tiempo)) #pasa el timestamp a a bytes con en Little Endian
    a=IP()/ICMP(seq=(z+1))/bytes(timestamp_bytes)   #arma el paquete, con la condición de que la secuencia aumenta en uno durante el ciclo, también pasa el timestamp
    caracter=sys.argv[1][z]                         #toma el string pasado como argumento de la terminal
    a.ttl=64                                        #setea el time to live
    a.src="127.0.0.1"                               #ip de fuente
    a.dst="127.0.0.1"                               #ip de destino(se escoge esta para loopback)
    a['ICMP'].id=id_paquete                         #se carga la id generada con el pid al paquete
    a['Raw'].load=f"{caracter}\x0e\x0e\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17" \
        "\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27" \
        "\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37" #Info de payload sacada de wireshark, con el añadido del caracter en la primera posicion
    #a.show()                                                              #esta info se copio de un ping cualquiera enviado de forma normal
    send(a)
    time.sleep(1)





