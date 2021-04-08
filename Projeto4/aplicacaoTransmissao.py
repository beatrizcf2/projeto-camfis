#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from enlace import *
import time
import numpy as np
from funcoes import *
from protocolo import *
import sys

import os


#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem141101" # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)


def main():
    try:
        
        com1 = enlace(serialName)
        

        # Ativa comunicacao. Inicia os threads e a comunicação serial
        com1.enable()
        
        print('\nComunicação com SUCESSO')
        
        #carregando img para transmissao
        imageR = image_picker()
        
        #bytes da img
        txBuffer = open(imageR, 'rb').read()
        
        #len dos bytes da imagem
        txLen = len(txBuffer)
        
        #criando os datagramas
        datagramas = createDatagrams(txBuffer, txLen)
        
        #numero total de pacotes a serem enviados
        numPckg = len(datagramas) + 1
        
            
        #ENVIANDO HANDSHAKE---------------------------------------
        handshake = protocolo(1, numPckg, 0, 0, 0, 0, 0).datagrama
        
        inicia = False
        
        while not inicia:
            com1.sendData(handshake)
            response = com1.getDataTime(14, 5) #retorna falso se passar de 5s
            if response==False:
                user = input("Servidor inativo. Tentar novamente? S/N: \n")
                if user == 'N':
                    raise Exception("Falha ao comunicar com o servidor")
            elif int.from_bytes(response[0:1], byteorder='big')==2:
                print("Resposta do server recebida")
                cont = 1
                inicia = True
            
        
                    
                    
        
        print("Servidor está ativo!\n")
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        
        com1.disable()
        
    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
