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
        
        #Iniciando o recebimento do head
        print("-------------------------------------------------")
        print("Iniciando recebimento do HANDSHAKE")
        print("-------------------------------------------------")
        
        head, nHead = com2.getData(10)
        print('head: ', head)
        if head[0:2]==0:
            print("Mensagem do tipo handshake!")
        
        '''
            HEAD
            type = head[0:2]
            id = head[2:4]
            nPackages = head[4:6]
            payload = head[6:8]
        '''
        type = int.from_bytes(head[0:2], byteorder='big')
        payloadLen = int.from_bytes(head[6:8], byteorder='big')
        
       
        print(f"Dados do head recebidos! Tipo de msg: {type} \n")
    
        #acesso ao payload recebido
        payload, nPayload = com2.getData(payloadLen)
        
        print("Dados do payload recebidos! ")
        print(f'Recebeu a seguinte msg: {payload.decode("utf-8")} \n')
        
        #acesso ao EOP recebido
        eop, nEop = com2.getData(4)
        
        #enviando resposta ao servidor
        print("Enviando resposta ao cliente... \n")
        

        response = acknowledge(0)
        com2.sendData(response)
        
        print("Resposta enviada para o client!")
        print("----------------------------------------------------- \n")
        #-----------------------------------------------------------------
       
        '''
            HEAD
            id = head[0:2]        --> id pacote atual
            nPackages = head[2:4] --> numero total de pacotes
            npayload = head[4:6]  --> tam payload em bytes
            
        '''
    
        
        print("-----------------------------------------------------")
        print("Iniciando recebimento dos pacotes")
        print("----------------------------------------------------- \n")
        
        # Recebimento dos pacotes ----------------------------------------
        getAll = False
        numberPackage = 0
        payloadImg = bytearray()
        
        while getAll==False:
            erro = False
            #Iniciando o recebimento do HEAD............................
            head, nHead = com2.getData(10)
            print('head: ', head)
            
            type = head[0:2]
            id = head[2:4]
            nPackages = head[4:6]
            nPayload = head[6:8]
            
            idInt = int.from_bytes(id, byteorder='big')
            packagesLen = int.from_bytes(nPackages, byteorder='big')
            payloadLen = int.from_bytes(nPayload, byteorder='big')
            
            print("--------------------------------------")
            print("Dados do head recebidos!")
            print(f'Id do pacote: {idInt}')
            print(f'Numero total de pacotes: {packagesLen}')
            print(f'Tamanho do payload: {payloadLen} bytes \n')
        
        
            #Iniciando recebimento do PAYLOAD...........................
            payload, payloadLenGet = com2.getData(payloadLen)
            
            print("--------------------------------------")
            print("Dados do payload recebidos!")
            print(f'Recebeu: {payloadLenGet} bytes do payload \n')
            
            
            #Iniciando acesso ao EOP....................................
            eop, nEop = com2.getData(4)
            
            print("--------------------------------------")
            print("Dados do EOP recebidos!")
            print("Verificando se eop esta correto...")
            
            #Verificando possíveis erros.................................
            if payloadLen != payloadLenGet:
                print('Tamanho do payload recebido é diferente do esperado')
                erro = True
            elif idInt != numberPackage:
                print('Id do pacote é diferente do esperado. Fora de ordem')
                erro = True
            elif eop != (0).to_bytes(4, byteorder='big'):
                print('ERRO: EOP não esta correto')
                erro = True
                
            # Enviando resposta ao client...............................
            '''
                TYPE:
                0 - handshake
                1 - envio dados
                2 - erro
                3 - td certo
                4 - mandar dnv
                5 - sucesso na transmissao
            '''
            if erro:
                print('Algo deu errado :( Enviando mensagem de erro ao client e aguardando reenvio do pacote...')
                #enviar msg de erro
                com2.sendData(acknowledge(2))
            else:
                print('Tudo certo :) Enviando ok ao client...')
                com2.sendData(acknowledge(3))
            
            
            
            # Aguardando resposta do client.............................
            time.sleep(5)
            asw, nAsw = com2.getData(15) #head=10+payload=1+eop=4
            type = asw[0:2] #type
        
            if type == 4:
                print("Ta reenviando os dados")
            elif type == 3:
                #sucesso --> continuo prox pacote                print("Deu tudo certo. Partiu proximo pacote")
                #se deu tudo certo segue o baile
                print('Tudo certo. Fim do pacote! \n')
                numberPackage +=1
                payloadImg += payload
            
            
            #se eu chegar no ultimo pacote saio do loop
            if idInt+1 == packagesLen:
                getAll = True
            
        
            #enviando resposta ao client com o tamanho dos dados recebidos
            #nPayload = nPayload.to_bytes(4, byteorder='big')
            #com2.sendData(nPayload)
            
            #print("--------------------------------------")
            #print("Enviando resposta ao client... \n")
            #print(f"npayload = {nPayload}")
            
        # FIM do recebimento dos pacotes -------------------------------
        
        print('Todos pacotes salvos!')
        
        #Salvando a cópia da img enviada
        print('Salvando os dados recebidos como cópia da img... \n')
        f = open(imageW, 'wb')
        f.write(payloadImg)
            
    
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

