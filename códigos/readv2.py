import enchant   #para utilizar esta libreria con el idioma español hace falta correr(en linux): sudo apt-get install myspell-es
import sys
import string
import codecs
from scapy.all import *
from colorama import Fore, Style
scapy_captura=rdpcap('real_3.pcapng')   #se carga la captura de paquetes
cadena_sin_decodificar=""
lista_de_listas=[]
max=0                                   
for packet in scapy_captura:            #se itera por paquete presente en la captura
    if(packet.haslayer(ICMP)):          #se revisa si se está en el layer ICMP
        data=bytes(packet[Raw].load)    #se captura la información en bytes
        if data:
            caracter=hex(data[0])       #se transforma en hex la data
            splitter=caracter.split("0x")   #se deja solo la parte númerica del hexadecimal
            cadena_sin_decodificar=cadena_sin_decodificar + codecs.decode(splitter[1],"hex").decode("utf-8")    #se decodifica el hexadecimal, y se arma la string enc

alfabeto=string.ascii_lowercase         #alfabeto a ser utilizado para desencriptar el cifrado Caesar
mas_probable=[]                         #lista encargada de mantener cuenta sobre la string desencriptada más probable a ser la real
diccionario=enchant.Dict("es_CL")       #se instancia enchant, que se utiliza como diccionario para comparar las palabras desencriptadas

mensaje_encriptado=(cadena_sin_decodificar).strip() #se eliminan los espacios en blanco de la string encriptada
mensaje_decriptado=""                               

for a in range(26):                                 #se itera por el rango del alfabeto
    for x in range(len(mensaje_encriptado)):        #se itera por el largo del mensaje encriptado
        if mensaje_encriptado[x] in alfabeto:       #se revisa si el char está dentro del alfabeto
            posicion=alfabeto.find(mensaje_encriptado[x])   
            nuevaposicion=(posicion-a)%26           #se usa de corrimiento el rango del alfabeto, a, en este caso
            nuevocaracter=alfabeto[nuevaposicion]
            mensaje_decriptado+=nuevocaracter
        else:
            mensaje_decriptado += mensaje_encriptado[x] #arriba se mueve por el alfabeto haciendo el algoritmo inverso.

    revisar=mensaje_decriptado.split()                  #se separa la string desencriptada, tomando como separador espacio en blanco
    for i in range(len(revisar)):                       #se itera por el largo de la string desencriptada
        if diccionario.check(revisar[i]):               #se revisa si cada una de las palabras desencriptadas matchea una del diccionario en español
            mas_probable.append(revisar[i])             #en caso de que resulta en un match, se suma la palabra a la lista.
    if len(mas_probable)>max:
        max=len(mas_probable)                           #se deja un max global, equivalente a la mayor cantidad de palabras reales post desencripción
    lista_de_listas.append([mensaje_decriptado, len(mas_probable)]) #lista de lista donde se agrega la string, y el número de matches en el diccionario
    mensaje_decriptado=""
    mas_probable.clear()                                #se limpia el contador de matches para el siguiente ciclo
for b in range(len(lista_de_listas)):
    if max == lista_de_listas[b][1]:
        print(Fore.GREEN + f"{b} " + lista_de_listas[b][0] + Style.RESET_ALL)   #se printea en verde la string deco con más matches en el diccionario
    else:
        print(f"{b} " + lista_de_listas[b][0])          #en otro caso se printea sin color.