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
        
        print('\nComunicação com SUCESSO\n')
        print('------------------------------------------')
        print('Carregando dados para a transmissão')
        print('------------------------------------------\n')

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
        
        # marca o tempo do inicio da transmissao
        inicio = time.time()
        
            
        #ENVIANDO HANDSHAKE--------------------------------
        print('------------------------------------------')
        print('Conectando ao servidor')
        print('------------------------------------------\n')
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
            if not isinstance(response, bool):
                type = int.from_bytes(response[0:1], byteorder='big')
                idPckg = int.from_bytes(response[4:5], byteorder='big')
                writeLog(client, 'recebimento', type, len(response), idPckg, numPckg)
            if response==False:
                user = input("Servidor inativo. Tentar novamente? S/N: \n")
                if user == 'N':
                    raise Exception("Falha ao comunicar com o servidor")
            elif type==2:
                print("Servidor Ativo!")
                print("Pronto para iniciar a transmissão\n")
                cont = 1
                inicia = True
        
        #cont precisa ser sempre igual ao numero de id do pacote
        
        print('------------------------------------------')
        print('Enviando Pacotes')
        print('------------------------------------------\n\n')
        
        while cont<=numPckg:
            datagrama = datagramas[cont-1]
            print("................................................................")
            print(f"PACOTE {cont}")
            print(f"Payload: {int.from_bytes(datagrama.h5, byteorder='big')}\nÚltimo pacote recebido com sucesso: {cont-1}\n")
            datagrama.h7 = cont-1 #ultimo pacote recebido com sucesso
            com1.sendData(datagrama.datagrama)
            #typeAction, typeMsg, lenMsg, idPckg, numberPckg
            type = int.from_bytes(datagrama.h0, byteorder='big')
            idPckg = int.from_bytes(datagrama.h4, byteorder='big')
            writeLog(client, 'envio', type, len(datagrama.datagrama), idPckg, numPckg)
            
            print(f"Enviando pacote {idPckg} para o servidor..\nEsperando resposta do servidor\n")
            
            timer1 = time.time()
            timer2 = time.time()
            head = com1.getDataTime(10, 1)
            if not isinstance(head, bool):
                type = int.from_bytes(head[0:1], byteorder='big')
                idPckg = int.from_bytes(head[4:5], byteorder='big')
                writeLog(client, 'recebimento head', type, len(head), idPckg, numPckg)
            getType4 = False
                
            while not getType4: #ainda nao recebeu msg tipo 4
                if not isinstance(head, bool) and int.from_bytes(head[0:1], byteorder='big')==4:
                    getType4 = True
                    print(f"Pacote {cont} enviado com SUCESSO!\n\n")
                else: #se nao recebeu a msg 4 ainda
                    if (time.time()-timer1)>5:
                        print(f"timer1 > 5\nReenviando o pacote {cont}\n")
                        com1.sendData(datagrama.datagrama)
                        type = int.from_bytes(datagrama.h0, byteorder='big')
                        idPckg = int.from_bytes(datagrama.h4, byteorder='big')
                        writeLog(client, 'envio', type, len(datagrama.datagrama), idPckg, numPckg)
                        timer1 = time.time()
                    if (time.time()-timer2)>20:
                        print("timer2 > 20\nTempo máximo de espera excedido\n")
                        error = protocolo(5, 0, 0, 0, 0, 0, 0)
                        com1.sendData(error.datagrama)
                        #typeAction, typeMsg, lenMsg, idPckg, numberPckg
                        type = int.from_bytes(error.h0, byteorder='big')
                        idPckg = int.from_bytes(error.h4, byteorder='big')
                        writeLog(client, 'envio', type, len(error.datagrama), idPckg, numPckg)
                        raise Exception("Falha ao comunicar com o servidor\n")
                    if not head:
                        print("Nada foi recebido\n")
                    elif not isinstance(head, bool):
                        #print(f"recebi uma msg q n era do tipo 4\nTipo:{int.from_bytes(head[0:1], byteorder='big')}\n")
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
                            print(f"Houve um erro no envio. Reenviando o pacote {cont} ao servidor")
                            timer1 = time.time()
                            timer2 = time.time()
                    head = com1.getDataTime(10, 1)
                    if not isinstance(head, bool):
                        type = int.from_bytes(head[0:1], byteorder='big')
                        idPckg = int.from_bytes(head[4:5], byteorder='big')
                        writeLog(client, 'recebimento head', type, len(head), idPckg, numPckg)
                    
            
        
            eop, nEop = com1.getData(4)
            cont+=1
            
        print("TODOS OS DADOS FORAM ENVIADOS COM SUCESSO\n")
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------\n")
        
        #marca o tempo do fim da comunicacao
        fim = time.time()
        
        #calcula a taxa de transmissao
        baudrate = calculate_baudrate(inicio, fim, txLen)
        print('Tempo de transmissao = {} segundos'.format(round(fim-inicio, 2)))
        print('BaudRate = {} bytes/segundo '.format(round(baudrate, 2)))
        
        com1.disable()
        
    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
