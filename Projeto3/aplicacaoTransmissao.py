#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código!

'''
    TYPE OF MESSAGE:
    0 - handshake
    1 - envio dados
    2 - erro
    3 - td certo
    4 - mandar dnv
    5 - sucesso na transmissao
'''


from enlace import *
import time
import numpy as np
from funcoes import image_picker, calculate_baudrate, createDatagrams, acknowledge
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
        print("--------------------------------------")
        print("Verificando se servidor está ativo...")
        print("-------------------------------------- \n")
        
        handshake = acknowledge(0)
        print(f"Handshake: {handshake} \n")
        print(f"len handshake: {len(handshake)}")
        
        getHandshake = False
        
        
        while getHandshake == False: #se passar de 5s
            com1.sendData(handshake)
        
            print("Mensagem de verificacao enviada \n")
            print("Esperando resposta do servidor... \n")
            
            getHandshake = com1.getDataTime(15, 5)
            
            
            if getHandshake==False:
                user = input("Servidor inativo. Tentar novamente? S/N: \n")
                if user == 'N':
                    # Encerra comunicação
                    print("-------------------------")
                    print("Comunicação encerrada")
                    print("-------------------------")
                    
                    com1.disable()
                    sys.exit()
                    
        
        print("Handshake efetuado com sucesso!")
        print("Preparando transmissão do arquivo... \n")
        print("------------------------------- \n")
            
        
        
        
        #-------------------------------------------------
        #iniciando transmissao dos dados
        
        imageR = image_picker()

        print("Carregando imagem para transmissão... \n")
        
        #sao os bytes da img
        txBuffer = open(imageR, 'rb').read()
        
        #len dos bytes da imagem
        txLen = len(txBuffer)
        
        
        #fazendo o teste dos datagramas----------
        print('--------------------------------------')
        print('Criando os Datagramas... \n')
        datagramas = createDatagrams(txBuffer, txLen)
        print('-------------------------------------- \n')
        
        # marca o tempo do inicio da transmissao
        inicio = time.time()
        
        print('Datagramas criados! \n')
        print('A transmissão irá começar... \n ')
        
        '''
        
            Preciso receber resposta do server a cada datagrama enviado
            Enviar uma resposta informando como que o server deve proceder
        
        '''
        
        for datagrama in datagramas:
            erro = True
            #enquanto erro nao der false eu continuo tentando enviar o pacote
            while erro:
                # Enviando o datagrama
                com1.sendData(datagrama.datagrama) #serve vai dar get head,payload e eop, e dps enviar msg
                print("--------------------------------------")
                print(f"Enviando datagrama {int.from_bytes(datagrama.id, byteorder='big')} para o servidor...")
                print(f"Payload: {int.from_bytes(datagrama.nPayload, byteorder='big')}")
                print("--------------------------------------")
                time.sleep(0.01)
                #recebendo os dados da resposta (asw) do servidor com o n de bytes recebidos
                asw, nAsw = com1.getData(15) #head=10+payload=1+eop=4
                type = int.from_bytes(asw[0:2], byteorder='big') #type
                print(f"type: {type}")
                if type == 2:
                    #erro --> reenvio do pacote
                    com1.sendData(acknowledge(4))
                elif type == 3:
                    erro = False
                    #sucesso --> continuo o processo
                    com1.sendData(acknowledge(3))
                time.sleep(0.01)
                
            
            print("Resposta do servidor recebida!")
            print("--------------------------------------")
        
        #FIM DA TRANSMISSAO
    
        
        #marca o tempo do fim da comunicacao
        fim = time.time()
        
        #calcula a taxa de transmissao
        baudrate = calculate_baudrate(inicio, fim, txLen)
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
