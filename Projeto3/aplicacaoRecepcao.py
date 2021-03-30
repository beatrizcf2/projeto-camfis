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
        print("-----------------------------------------")
        print("HANDSHAKE")
        print("------------------------------------------")
        
        print("Recebendo handshake do client ...")
        handshake, nHandshake = com2.getData(15)
        print("Handshake recebido!\n")
        
        type = int.from_bytes(handshake[0:2], byteorder='big')
       
        
        
        #enviando resposta ao servidor
        print("Enviando resposta ao cliente...")

        response = acknowledge(0)
        com2.sendData(response)
        
        print("Resposta enviada para o client!\n")
        #-------------------------------------------------

    
        
        print("--------------------------------------------")
        print("Recebendo os pacotes")
        print("-------------------------------------------- \n")
        
        # Recebimento dos pacotes ----------------------------------------
        getAll = False
        numberPackage = 0
        payloadImg = bytearray()
        
        while not getAll:
            erro = False
            
            #Iniciando o recebimento do HEAD............................
            head, nHead = com2.getData(10)
            print('head: ', head)
            
            type = head[0:2]
            id = head[2:4]
            nPackages = head[4:6]
            nPayload = head[6:8]
            
            idInt = int.from_bytes(id, byteorder='big')
            typeInt = int.from_bytes(type, byteorder='big')
            packagesLen = int.from_bytes(nPackages, byteorder='big')
            payloadLen = int.from_bytes(nPayload, byteorder='big')
            
            
            print("Dados do head recebidos!")
            print(f'Id do pacote: {idInt}')
            print(f'Tipo de msg: {typeInt}')
            print(f'Numero total de pacotes: {packagesLen}')
            print(f'Tamanho do payload: {payloadLen} bytes \n')
        
        
            #Iniciando recebimento do PAYLOAD...........................
            payload, payloadLenGet = com2.getData(payloadLen)
            
           
            print("Dados do payload recebidos!")
            print(f'Recebeu: {payloadLenGet} bytes do payload \n')
            
            
            #Iniciando acesso ao EOP....................................
            eop, nEop = com2.getData(4)
            
            print("Dados do EOP recebidos!\n")
            
            
            
            #Verificando possíveis erros.................................
            print("Verificando possíveis erros ...\n")
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
            if erro:
                print('Algo deu errado :( Enviando mensagem de erro ao client e aguardando reenvio do pacote...\n')
                #enviar msg de erro
                com2.sendData(acknowledge(2))
            else:
                print('Tudo certo :) Enviando ok ao client...\n')
                com2.sendData(acknowledge(3))
            
            
            
            # Aguardando resposta do client.............................
            time.sleep(0.01)
            asw, nAsw = com2.getData(15) #head=10+payload=1+eop=4
            type = int.from_bytes(asw[0:2], byteorder='big') #type
            print(f"type: {type}")
        
            if type == 4:
                print("Ta reenviando os dados")
            elif type == 6:
                raise Exception("Comunicaçao FALHOU")
            elif type == 3:
                #sucesso --> continuo prox pacote                print("Deu tudo certo. Partiu proximo pacote")
                #se deu tudo certo segue o baile
                print('Tudo certo. Fim do pacote!\n')
                numberPackage +=1
                payloadImg += payload
            print("..........................")
            
            #se eu chegar no ultimo pacote saio do loop
            if idInt+1 == packagesLen:
                getAll = True
            
            
        # FIM do recebimento dos pacotes -------------------------------
        
        print('Todos pacotes salvos!\n')
        print('Enviando informações da transmissao ao client ...\n')
        
        com2.sendData(acknowledge(5))
        
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

