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
        
        '''
            HEAD
            id = head[0:2]
            nPackages = head[2:4]
            payload = head[4:6]
        '''
        
        payloadLen = int.from_bytes(head[4:6], byteorder='big')
        
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
        
        msg = ("ok").encode('utf-8') #handshake em bytes
        msgLen = len(msg)
        response = protocolo(msg, msgLen,0,1).datagrama
        print(f"Response: {response}")
        com2.sendData(response)
        
        print("Resposta enviada para o client!")
        #-----------------------------------------------------------------
       
        '''
            HEAD
            id = head[0:2]        --> id pacote atual
            nPackages = head[2:4] --> numero total de pacotes
            npayload = head[4:6]  --> tam payload em bytes
            
        '''
        
        print('A recepção irá começar... \n')
        
        '''
        fazer um while aq pra receber tds os pacotes
        enquanto nao receber todos os pacotes eu fico no loop
        
        
        
        se der erro --> reporto ao client
        se n der --> concateno o payload e prossigo pro prox pacote
        
        getAll so vai ser True quando eu chegar no eop do ultimo pacote
        '''
        # Recebimento dos pacotes ----------------------------------------
        getAll = False
        
        #while getAll==False:
        
        #Iniciando o recebimento do HEAD............................
        head, nHead = com2.getData(10)
        print('head: ', head)
        
        id = head[0:2]
        nPackages = head[2:4]
        nPayload = head[4:6]
        
        idInt = int.from_bytes(id, byteorder='big')
        packagesLen = int.from_bytes(nPackages, byteorder='big')
        payloadLen = int.from_bytes(nPayload, byteorder='big')
        
        print("--------------------------------------")
        print("Dados do head recebidos!")
        print(f'Id do pacote: {idInt}')
        print(f'Numero total de pacotes: {packagesLen}')
        print(f'Tamanho do payload: {payloadLen} bytes \n')
    
    
        #Iniciando recebimento do PAYLOAD...........................
        payload, nPayload = com2.getData(payloadLen)
        
        print("--------------------------------------")
        print("Dados do payload recebidos!")
        print(f'Recebeu: {nPayload} bytes do payload \n')
        
        
        #Iniciando acesso ao EOP....................................
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
        print(f"npayload = {nPayload}")
            
        # FIM do recebimento dos pacotes -------------------------------
        
        print('Todos pacotes salvos!')
        
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

