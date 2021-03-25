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
    id = 0 #id do meu primeiro pacote
    lenPackages = ceil(txLen/114) #n de pacotes arredondando pra cima
    print(f"Tamanho da msg: {txLen}")
    print(f"Numero de pacotes: {lenPackages}")
    
    #preciso separar o txBuffer em n pacotes de tam 114
    for i in range(0, txLen, 114):
        if txLen - i >= 114: #se o tamanho da msg for maior ou igual a 114 preencho td o payload
            payload = txBuffer[0+i:114+i]
            payloadLen = len(payload)
            print(f'O tamanho do Payload do datagrama {id} é: {payloadLen}')
        else:
            payload = txBuffer[0+i:] # vai do inicio ate o final se o tam for menor que 114
            payloadLen = len(payload)
            print(f'O tamanho do Payload do último datagrama {id} é: {payloadLen}')
            
        datagrama = protocolo(payload,payloadLen,id,lenPackages)
        datagramas.append(datagrama)
        id+=1
        print(f'Foram criados {len(datagramas)}')
    
    return datagramas
