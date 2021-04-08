#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################



from enlace import *
import time
import numpy as np

from protocolo import *
from funcoes import *

import os

serialName = "/dev/cu.usbmodem14301" # Mac
imageW = "./img/copia.png"



    
    

def main():
    try:

        com2 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial
        com2.enable()

        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        print('Comunicação com SUCESSO \n')
        
        # RECEBENDO HANDSHAKE---------------------------------------------
        ocioso = True
        server = 111
        print("Recebendo handshake do client ...")
        while ocioso:
            handshake = com2.getDataTime(14, 1) #timesleep 1s
            if handshake==False:
                pass
            elif int.from_bytes(handshake[0:1], byteorder='big')==1:
                idServer = int.from_bytes(handshake[1:2], byteorder='big')
                print(f"opa recebi algo. idserver={idServer}")
                if idServer == server:
                    ocioso = False
                    numPckg = int.from_bytes(handshake[3:4], byteorder='big')
                    print("Handshake recebido!\n")
        response = protocolo(2, numPckg, 0, 0, 0, 0, 0).datagrama
        com2.sendData(response)
        cont = 1
        
        print("Msg tipo 2 enviada")
        
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
        
    except Exception as erro:
        print("\n ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

