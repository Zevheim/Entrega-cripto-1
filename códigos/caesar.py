import sys
resultado=""

for i in range(len(sys.argv[1])):           #Toma el largo de la cadena introducida por terminal, para iterar sobre este.
    if sys.argv[1][i] == ' ':               #En caso de que haya espacio en blanco no es necesario desplazar caracteres.
        resultado +=" "
    elif(sys.argv[1][i].isupper()):
        resultado += chr((ord(sys.argv[1][i]) + int(sys.argv[2])-65) % 26 + 65)         #Se desplaza en el rango de caracteres mayuscula
    else:
        resultado += chr((ord(sys.argv[1][i]) + int(sys.argv[2])-97) % 26 + 97)         #se desplaza en el rango de caracteres minuscula
print(resultado)