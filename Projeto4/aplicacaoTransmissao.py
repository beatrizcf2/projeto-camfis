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
        numPckg = len(datagramas)
        
            
        #ENVIANDO HANDSHAKE---------------------------------------
        handshake = protocolo(1, numPckg, 0, 0, 0, 0, 0)
        
        inicia = False
        client = True
        
        while not inicia:
            com1.sendData(handshake.datagrama)
            #typeAction, typeMsg, lenMsg, idPckg, numberPckg
            type = int.from_bytes(handshake.h0, byteorder='big')
            idPckg = int.from_bytes(handshake.h4, byteorder='big')
            writeLog(client, 'envio', type, len(handshake.datagrama), idPckg, numPckg)
            response = com1.getDataTime(14, 5) #retorna falso se passar de 5s
            if response==False:
                user = input("Servidor inativo. Tentar novamente? S/N: \n")
                if user == 'N':
                    raise Exception("Falha ao comunicar com o servidor")
            elif int.from_bytes(response[0:1], byteorder='big')==2:
                print("Resposta do server recebida")
                cont = 1
                inicia = True
        
        #cont precisa ser sempre igual ao numero de id do pacote
        
        while cont<=numPckg:
            print("-------------------------------------------------")
            print(f"Numero de datagramas: {len(datagramas)}\nnumPckg: {numPckg}\ncont: {cont}\n")
            datagrama = datagramas[cont-1]
            datagrama.h7 = cont-1 #ultimo pacote recebido com sucesso
            com1.sendData(datagrama.datagrama)
            #typeAction, typeMsg, lenMsg, idPckg, numberPckg
            type = int.from_bytes(datagrama.h0, byteorder='big')
            idPckg = int.from_bytes(datagrama.h4, byteorder='big')
            writeLog(client, 'envio', type, len(datagrama.datagrama), idPckg, numPckg)
            
            print(f"Enviando pacote {idPckg} para o servidor...\nCont={cont}\nTipo:{type}\nTamanho do datagrama: {len(datagrama.datagrama)}\nUltimo recebido com sucesso: {cont-1}\n")
            
            timer1 = time.time()
            timer2 = time.time()
            head = com1.getDataTime(10, 1)
            getType4 = False
                
            while not getType4: #ainda nao recebeu msg tipo 4
                #if not head:
                #    head = com1.getDataTime(10, 1)
                #    print("nao recebi nadica")
                if not isinstance(head, bool) and int.from_bytes(head[0:1], byteorder='big')==4:
                    getType4 = True
                else: #se nao recebeu a msg 4 ainda
                    if (time.time()-timer1)>5:
                        print("timer1>5")
                        com1.sendData(datagrama.datagrama)
                        #typeAction, typeMsg, lenMsg, idPckg, numberPckg
                        type = int.from_bytes(datagrama.h0, byteorder='big')
                        idPckg = int.from_bytes(datagrama.h4, byteorder='big')
                        writeLog(client, 'envio', type, len(datagrama.datagrama), idPckg, numPckg)
                        timer1 = time.time()
                    if (time.time()-timer2)>20:
                        print("timer2>20")
                        error = protocolo(5, 0, 0, 0, 0, 0, 0)
                        com1.sendData(error.datagrama)
                        #typeAction, typeMsg, lenMsg, idPckg, numberPckg
                        type = int.from_bytes(error.h0, byteorder='big')
                        idPckg = int.from_bytes(error.h4, byteorder='big')
                        writeLog(client, 'envio', type, len(error.datagrama), idPckg, numPckg)
                        raise Exception("Falha ao comunicar com o servidor\n")
                    if not head:
                        print("nao recebi nada\n")
                    elif not isinstance(head, bool):
                        print(f"recebi uma msg q n era do tipo 4\nTipo:{int.from_bytes(head[0:1], byteorder='big')}\n")
                        eop, nEop = com1.getData(4)
                        if int.from_bytes(head[0:1], byteorder='big') == 6:
                            cont = int.from_bytes(head[6:7], byteorder='big') #pega o pacote que devo reiniciar
                            datagrama = datagramas[cont-1]
                            datagrama.h7 = cont #last sent successfully
                            com1.sendData(datagrama.datagrama)
                            #typeAction, typeMsg, lenMsg, idPckg, numberPckg
                            type = int.from_bytes(datagrama.h0, byteorder='big')
                            idPckg = int.from_bytes(datagrama.h4, byteorder='big')
                            writeLog(client, 'envio', type, len(datagrama.datagrama), idPckg, numPckg)
                            print(f"Pacote que deu erro reenviado ao servidor!/nPacote de recomeço: {cont}")
                            timer1 = time.time()
                            timer2 = time.time()
                    head = com1.getDataTime(10, 1)
            
        
            print(f"msg do tipo 4 encontrada\nid={int.from_bytes(head[4:5], byteorder='big')}\n")
            eop, nEop = com1.getData(4)
            cont+=1
            
            
        
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
