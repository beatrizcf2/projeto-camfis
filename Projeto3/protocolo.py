class protocolo(object):
    
    def __init__(self, txBuffer, txLen, idPackage, lenPackages, type):
        self.type = type.to_bytes(2, byteorder='big')
        self.id = idPackage.to_bytes(2, byteorder='big') #qual o meu pacote
        self.nPackage = lenPackages.to_bytes(2, byteorder='big') #total de pacotes
        self.nPayload = txLen.to_bytes(2, byteorder='big') #tamanho do payload
        self.head = self.type + self.id + self.nPackage + self.nPayload + (0).to_bytes(2, byteorder='big') #pra dar 10
        
        self.payload = txBuffer
        
        self.eop = (0).to_bytes(4, byteorder='big')
        
        self.datagrama = self.head + self.payload + self.eop
        
        '''
            TYPE:
            0 - handshake
            1 - envio dados
            2 - erro
            3 - td certo
            4 - mandar dnv
            5 - sucesso na transmissao
        '''
        
    



