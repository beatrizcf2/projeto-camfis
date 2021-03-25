class protocolo(object):
    
    def __init__(self, txBuffer, txLen):
        self.head = txLen.to_bytes(10, byteorder='big')
        self.payload = txBuffer
        self.eop = (0).to_bytes(4, byteorder='big')
        self.datagrama = self.head + self.payload + self.eop
        
    



