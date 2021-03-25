class protocolo(object):
    
    def __init__(self, txBuffer, txLen, idPackage, lenPackages):
        self.id = idPackage.to_bytes(2, byteorder='big') #qual o meu pacote
        self.nPackage = lenPackages.to_bytes(2, byteorder='big') #total de pacotes
        self.nPayload = txLen.to_bytes(2, byteorder='big') #tamanho do payload
        
        self.head = self.id + self.nPackage + self.nPayload + (0).to_bytes(4, byteorder='big') #pra dar 10
        self.payload = txBuffer
        self.eop = (0).to_bytes(4, byteorder='big')
        self.datagrama = self.head + self.payload + self.eop
        
    



