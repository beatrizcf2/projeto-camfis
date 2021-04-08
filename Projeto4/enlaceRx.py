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

# Threads
import threading

# Class
#Rx - quem recebe
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex == True):
                #comando que acessa o hw
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp  
                time.sleep(0.01)

    def threadStart(self):       
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        return(len(self.buffer))

    def getAllBuffer(self, len):
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    #metodo usado para receber os dados
    #recebe como argunmento o tamanho dos dados
    #enquanto o tam do buffer for menor do que o dos dados ele da um timesleep
    #retorna 
    def getNData(self, size):
        while(self.getBufferLen() < size):
            time.sleep(0.05)                 
        return(self.getBuffer(size))
        
    #funcao q faz o msm q getNdata mas dado um tempo max
    def getNDataTime(self,size,t):
        while self.getBufferLen() < size:
            if t <=0:
                return False
            mins, secs = divmod(t, 60) #calcula o n de min e seg
            timer = '{:02d}:{:02d}'.format(int(mins), int(secs))
            print(timer, end="\r") #print q sobrepoe o anterior
            time.sleep(0.05) #conta 0.05 seg
            t -= 0.05
          
        return self.getBuffer(size)
    


    def clearBuffer(self):
        self.buffer = b""


