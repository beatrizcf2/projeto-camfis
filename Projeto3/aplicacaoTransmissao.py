#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from funcoes import image_picker, calculate_baudrate
from protocolo import *

import os


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem141101" # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial
        com1.enable()
        
        print('Comunicação com SUCESSO')
        
            
        #ENVIANDO HANDSHAKE-----------------------------
        
        print("Verificando se servidor está ativo...")
        
        msg = ("ok?").encode('utf-8') #handshake em bytes
        msgLen = len(msg)
        handshake = protocolo(msg, msgLen).datagrama
        
        print(f"Mensagem: {msg}")
        print(f"Handshake: {handshake}")
        
        getHandshake = False
        
        #com1.sendData(hanshake.encode('utf-8'))
        
        #print("Mensagem de verificacao enviada")
        #print("Esperando resposta do servidor...")
        
        #getHandshake = com1.getDataTime(msgLen)
        
        while getHandshake == False: #se passar de 5s
            print("cheguei até acá")
            com1.sendData(handshake)
        
            print("Mensagem de verificacao enviada")
            print("Esperando resposta do servidor...")
            
            getHandshake = com1.getDataTime(msgLen, 5)
            
            print("Cheguei ate o getdatatime")
            
            if getHandshake==False:
                user = input("Servidor inativo. Tentar novamente? S/N: ")
                if user == 'N':
                    # Encerra comunicação
                    print("-------------------------")
                    print("Comunicação encerrada")
                    print("-------------------------")
                    
                    com1.disable()
                    sys.exit()
                    
        
            
        
        print("Handshake efetuado com sucesso!")
        print("Preparando transmissão do arquivo...")
            
        
        
        
        #-------------------------------------------------
        #iniciando transmissao dos dados
        
        imageR = image_picker()

        print("Carregando imagem para transmissão... \n")
        
        #sao os bytes da img
        txBuffer = open(imageR, 'rb').read()
        
        #len dos bytes da imagem
        txLen = len(txBuffer)
        
        datagrama = protocolo(txBuffer,txLen).datagrama
        
        # marca o tempo do inicio da transmissao
        inicio = time.time()
    
        print('A transmissão irá começar... \n ')
        
        # Enviando o datagrama
        com1.sendData(datagrama)
        print("--------------------------------------")
        print("Enviando datagrama para o servidor...")
        print("--------------------------------------")
        
        time.sleep(0.5)
        
       
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        txSize = com1.tx.getStatus()
        print(f'Status TX: {txSize}')
        
        
        #recebendo os dados da resposta (asw) do servidor com o n de bytes recebidos
        asw, nAsw = com1.getData(4)
        lenAsw = int.from_bytes(asw, byteorder='big')
        print("Resposta do servidor recebida!")
        print("Servidor recebeu {} bytes" .format(lenAsw))
        print("--------------------------------------")
        
        if lenAsw == txLen:
            print('\n Imagem enviada com sucesso ao servidor \n')
        else:
            print('\n ERRO no envio')
        
        
        #marca o tempo do fim da comunicacao
        fim = time.time()
        
        #calcula a taxa de transmissao
        baudrate = calculate_baudrate(inicio, fim, lenAsw)
        print('Tempo de transmissao = {} segundos'.format(round(fim-inicio, 2)))
        print('BaudRate = {} bytes/segundo '.format(round(baudrate, 2)))
        
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
