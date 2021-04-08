#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    
    def __init__(self, name):
        self.fisica      = fisica(name) # é o serialName - nome da porta do computador
        self.rx          = RX(self.fisica) #inicializa o RX
        self.tx          = TX(self.fisica) #inicializa o TX
        self.connected   = False

    def enable(self):
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    # Método que recebe os dados em bytes (array) e envia os dados
    #usa a funcao sendBuffer do tx(pino de envio)
    def sendData(self, data):
        self.tx.sendBuffer(data)
    
    #Método que recebe o tamanho dos dados e retorna os dados e o len dos dados
    def getData(self, size):
        data = self.rx.getNData(size)
        return(data, len(data))
        
    #Método que recebe o tamanho dos dados e retorna os dados e o len dos dados apos um determinado tempo
    
    def getDataTime(self,size,t):
        while self.rx.getBufferLen() < size:
            if t <=0:
                return False #, (0).to_bytes(size), byteorder='big')
            mins, secs = divmod(t, 60) #calcula o n de min e seg
            timer = '{:02d}:{:02d}'.format(int(mins), int(secs))
            print(timer, end="\r") #print q sobrepoe o anterior
            time.sleep(0.05) #conta 0.05 seg
            t -= 0.05
          
        return self.rx.getBuffer(size)
