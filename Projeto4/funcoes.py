import tkinter as tk
from tkinter import filedialog
from math import *
from protocolo import *

# https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
def image_picker():
	root = tk.Tk()
	root.withdraw()

	return filedialog.askopenfilename(title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

def calculate_baudrate(start, end, nBytes):
    return nBytes/(end-start)

def createDatagrams(txBuffer,txLen):
    #preciso add o id do meu pacote no head e o n total no head
    datagramas = [] #vou salvar todos meus pacotes aq
    id = 1 #id do meu primeiro pacote
    lenPackages = ceil(txLen/114) #n de pacotes arredondando pra cima
    print(f"Tamanho da msg: {txLen}")
    print(f"Numero de pacotes: {lenPackages}")
    print(f"Tamanho do payload do ultimo datagrama: {txLen-(114*(lenPackages-1))}\n")
    
    #preciso separar o txBuffer em n pacotes de tam 114
    for i in range(0, txLen, 114):
        if txLen - i >= 114: #se o tamanho da msg for maior ou igual a 114 preencho td o payload
            payload = txBuffer[0+i:114+i]
            payloadLen = len(payload) 
            
        else:
            payload = txBuffer[0+i:] # vai do inicio ate o final se o tam for menor que 114
            payloadLen = len(payload)
            
        datagrama = protocolo(3, lenPackages, id, payloadLen, 0, 0, payload)
        #PROTOCOLO: protocolo(type, lenPackages, idPackage, txLen, restartPackage, successPackage, txBuffer)
        datagramas.append(datagrama)
        id+=1
    print(f'Foram criados {len(datagramas)}\n')
    
    return datagramas
    
    
def createMsg(type, lenPackages):
    '''
        PROTOCOLO: protocolo(type, lenPackages, idPackage, txLen, restartPackage, successPackage, txBuffer)
        TYPE:
        tipo 1 - handshake client-server
        tipo 2 - hanshake server-client
        tipo 3 - dados
        tipo 4 - verificacao server-client para msg tipo 3
        tipo 5 - timeout, quando o limite de espera excede
        tipo 6 - erro, server-client quando recebe uma msg do tipo 3 invalida
    '''
    txBuffer = 0
    txLen = 0
    
    
    datagrama = protocolo(type, lenPackages, 0, 0, 0, 0, 0).datagrama
    #total de bytes = 14
    return datagrama
'''
def verifyError(head):
    
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
    if lenPayload != h5:
        print('Tamanho do payload recebido é diferente do esperado')
        erro = True
    elif cont != h4:
        print('Id do pacote é diferente do esperado. Fora de ordem')
        erro = True
    elif eop != (0).to_bytes(4, byteorder='big'):
        print('ERRO: EOP não esta correto')
        erro = True
        
    # Enviando resposta ao client...............................
    if erro:
        print('Algo deu errado :( Enviando mensagem de erro ao client e aguardando reenvio do pacote...\n')
        #enviar msg de erro
        com2.sendData()
    else:
        print('Tudo certo :) Enviando ok ao client...\n')
        com2.sendData()
        
''' 
        
        
    
