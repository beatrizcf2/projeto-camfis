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
        
        # RECEBENDO HANDSHAKE--------------------------------------------------
        
        #Iniciando o recebimento do head
        head, nHead = com2.getData(10)
        print('head: ', head)
        
        payloadLen = int.from_bytes(head, byteorder='big')
        
        print("--------------------------------------")
        print("Dados do head recebidos! Tipo de msg: Handshake")
        print(f'Tamanho do payload: {payloadLen} bytes \n')
    
    
        #acesso ao payload recebido
        payload, nPayload = com2.getData(payloadLen)
        
        print("--------------------------------------")
        print("Dados do payload recebidos!")
        print(f'Recebeu: {nPayload} bytes do payload \n')
        
        #acesso ao EOP recebido
        eop, nEop = com2.getData(4)
        
        #enviando resposta ao servidor
        
        msg = ("ok?").encode('utf-8') #handshake em bytes
        msgLen = len(msg)
        response = protocolo(msg, msgLen).datagrama
        print(f"Response: {response}")
        com2.sendData(response)
        
        print("Resposta enviada para o client!")
        #----------------------------------------------------------------------
        
        print('A recepção irá começar... \n')
        
        
        #Iniciando o recebimento do head
        head, nHead = com2.getData(10)
        print('head: ', head)
        #transformando head em int para passar como arg do getdata - sei o tamanho do meu payload
        payloadLen = int.from_bytes(head, byteorder='big')
        
        print("--------------------------------------")
        print("Dados do head recebidos!")
        print(f'Tamanho do payload: {payloadLen} bytes \n')
    
    
        #acesso ao payload recebido
        payload, nPayload = com2.getData(payloadLen)
        
        print("--------------------------------------")
        print("Dados do payload recebidos!")
        print(f'Recebeu: {nPayload} bytes do payload \n')
        
        
        #acesso ao EOP recebido
        eop, nEop = com2.getData(4)
        
        print("--------------------------------------")
        print("Dados do EOP recebidos!")
        print("Verificando se eop esta correto...")
        
        if eop == (0).to_bytes(4, byteorder='big'):
            print('EOP esta correto. Fim do pacote! \n')
        
        
        #enviando resposta ao client com o tamanho dos dados recebidos
        nPayload = nPayload.to_bytes(4, byteorder='big')
        com2.sendData(nPayload)
        
        print("--------------------------------------")
        print("Enviando resposta ao client... \n")
        
        
        #Salvando a cópia da img enviada
        print('Salvando os dados recebidos como cópia da img... \n')
        f = open(imageW, 'wb')
        f.write(payload)
            
    
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

