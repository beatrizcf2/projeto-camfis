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
        teste = 0
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
        payloadImg = bytearray()
        successPckg = 0
        
        while cont<=numPckg:
            print("-------------------------------------------------")
            timer1 = time.time()
            timer2 = time.time()
            head = com2.getDataTime(10, 1) #pegando so o head
            getType3 = False
                
            while not getType3:
                if not isinstance(head, bool) and int.from_bytes(head[0:1], byteorder='big')==3:
                    getType3 = True
                    print("recebi msg do tipo 3")
                else: #se nao recebeu a msg 3 ainda
                    if (time.time()-timer2)>20:
                        print("timer2>20")
                        timeOut = protocolo(5, 0, 0, 0, 0, 0, 0).datagrama
                        com2.sendData(timeOut)
                        raise Exception("Falha ao comunicar com o servidor")
                    elif (time.time()-timer1)>2:
                        print("timer1>2")
                        verify = protocolo(4, 0, 0, 0, 0, 0, 0).datagrama
                        com2.sendData(verify)
                        timer1 = time.time()
                        
                    if not head:
                        print("nao recebi nada")
                    elif not isinstance(head, bool):
                        print(f"recebi msg, mas nao era do tipo 3\nTipo:{int.from_bytes(head[0:1], byteorder='big')}")
                        eop, nEop = com1.getData(4)
                        print("peguei eop residual")
                        
                    response = com2.getDataTime(10, 1)
                    
            print(f"msg do tipo 3 encontrada\nid={int.from_bytes(head[4:5], byteorder='big')}")
            
            #verifica erros
            erro = False
            
            h0 = int.from_bytes(head[0:1], byteorder='big')
            h1 = int.from_bytes(head[1:2], byteorder='big')
            h2 = int.from_bytes(head[2:3], byteorder='big')
            h3 = int.from_bytes(head[3:4], byteorder='big')
            h4 = int.from_bytes(head[4:5], byteorder='big')
            h5 = int.from_bytes(head[5:6], byteorder='big')
            h6 = int.from_bytes(head[6:7], byteorder='big')
            h7 = int.from_bytes(head[7:8], byteorder='big')
            h8 = int.from_bytes(head[8:9], byteorder='big')
            h9 = int.from_bytes(head[9:10], byteorder='big')
            
            print(f"Tipo de mensagem: {h0}")
            print(f"Id do sensor: {h1}")
            print(f"Id do servidor: {h2}")
            print(f"Número total de pacotes do arquivo: {h3}")
            print(f"Pacote atual: {h4}")
            print(f"Tamanho do payload {h5}")
            print(f"Pacote solicitado para recomeço: {h6}")
            print(f"Último pacote recebido com sucesso: {h7}")
            print(f"CRC: {h8}")
            print(f"CRC: {h9}\n")
            
            payload, lenPayload = com2.getData(h5)
            print("Dados do payload recebidos!")
            print(f'Recebeu: {lenPayload} bytes do payload\n')
            
            eop, lenEop = com2.getData(4)
            print("Dados do EOP recebidos!\n")
            
            #verificando erros
            if cont == 7 and teste == 0:
                h4 = 27 #verificar se esta fora de ordem
                teste += 1
                
            
            if lenPayload != h5:
                print('Tamanho do payload recebido é diferente do esperado')
                erro = True
            elif cont != h4:
                print(f'Id do pacote é diferente do esperado. Fora de ordem. Esperava {cont}, mas recebi {h4}')
                erro = True
            elif eop != (0).to_bytes(4, byteorder='big'):
                print('ERRO: EOP não esta correto')
                erro = True
                
            # Enviando resposta ao client...............................
            if erro:
                print('Algo deu errado :( Enviando mensagem de erro ao client e aguardando reenvio do pacote...\n')
                error = protocolo(6, 0, 0, 0, restartPckg, successPckg, 0).datagrama
                com2.sendData(error)
            else:
                print('Tudo certo :) Enviando ok ao client...\n')
                restartPckg = cont+1
                successPckg = cont
                correct = protocolo(4, 0, 0, 0, 0, 0, 0).datagrama
                com2.sendData(correct)
                cont+=1
                payloadImg += payload
                print("tudo certo")
                
                
            
        
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

