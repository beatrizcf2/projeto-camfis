import tkinter as tk
from tkinter import filedialog
from math import *
from protocolo import *
import time

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


def writeLog(client, typeAction, typeMsg, lenMsg, idPckg, numberPckg):
    tempo = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    if client:
        file = open("logs/Client4.txt", "a")
    else:
        file = open("logs/Server4.txt", "a")
    
    log = tempo + '/ ' + typeAction + '/ ' + str(typeMsg) + '/ ' + str(lenMsg)
    if typeMsg == 3:
        log += '/ ' + str(idPckg) + '/ ' + str(numberPckg)
    file.write(log + '\n')
    file.close()
        
    

        
        
    
