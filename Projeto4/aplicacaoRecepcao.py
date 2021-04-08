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
        
        while cont<=numPckg:
            timer1 = time.time()
            timer2 = time.time()
            head = com2.getDataTime(10, 1) #pegando so o head
            getType3 = False
                
            while not getType3:
                
                if not head:
                    pass
                elif int.from_bytes(head[0:1], byteorder='big')==3:
                    getType3 = True
                    print("recebi msg do tipo 3")
                else: #se nao recebeu a msg 3 ainda
                    print(f"recebi msg, mas nao era do tipo 3\nTipo:{int.from_bytes(head[0:1], byteorder='big')}")
                    eop, nEop = com2.getData(4)
                    if (time.time()-timer2)>20:
                        print("timer2>20")
                        error = protocolo(5, 0, 0, 0, 0, 0, 0).datagrama
                        com2.sendData(error)
                        raise Exception("Falha ao comunicar com o servidor")
                    elif (time.time()-timer1)>2:
                        print("timer1>2")
                        verify = protocolo(4, 0, 0, 0, 0, 0, 0).datagrama
                        com2.sendData(verify)
                        timer1 = time.time()
                        
                    response = com2.getDataTime(10, 1)
            print(f"msg do tipo 3 encontrada\nid={int.from_bytes(head[4:5], byteorder='big')}")
            h5 = int.from_bytes(head[5:6], byteorder='big')
            print(f"Tamanho do payload = {h5}")
            payload, lenPayload = com2.getData(h5)
            print("peguei payload")
            eop, nEop = com2.getData(4)
            print("peguei eop")
            
            #verifica erros
            
            erro = False
            if not erro:
                correct = protocolo(4, 0, 0, 0, 0, 0, 0).datagrama
                com2.sendData(correct)
                cont+=1
                print("tudo certo")
            
                
            
        
            
    
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

