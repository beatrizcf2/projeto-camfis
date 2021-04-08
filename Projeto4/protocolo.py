class protocolo(object):
    
    def __init__(self, type, lenPackages, idPackage, txLen, restartPackage, successPackage, txBuffer):
        
        idSensor = 111
        idServer = 222
        idFile = 1
    
        #head
        self.h0 = type.to_bytes(1, byteorder='big')            #tipo
        self.h1 = idSensor.to_bytes(1, byteorder='big')        #id
        self.h2 = idServer.to_bytes(1, byteorder='big')        #id
        self.h3 = lenPackages.to_bytes(1, byteorder='big')     #total de pacotes
        self.h4 = idPackage.to_bytes(1, byteorder='big')       #id pacote atual
        if type == 1 or type == 2:
            self.h5 = idFile.to_bytes(1, byteorder='big')      #id arquivo --> se for h0=handshake
        elif type == 3:
            self.h5 = txLen.to_bytes(1, byteorder='big')       #len payload --> se for h0=3
        else:
            self.h5 = (0).to_bytes(1, byteorder='big')
        self.h6 = restartPackage.to_bytes(1, byteorder='big')  #restartpackage
        self.h7 = successPackage.to_bytes(1, byteorder='big')  #ultimo pacote com sucesso = idPackage-1
        self.h8 = (0).to_bytes(1, byteorder='big')             #CRC
        self.h9 = (0).to_bytes(1, byteorder='big')             #CRC
        
        self.head = self.h0 + self.h1 + self.h2 + self.h3 + self.h4 + self.h5 + self.h6 + self.h7 + self.h8 + self.h9
        
        #payload
        if txBuffer==0:
            self.payload = bytearray()
        else:
            self.payload = txBuffer
        
        #eop
        self.eop = (0).to_bytes(4, byteorder='big')
        
        self.datagrama = self.head + self.payload + self.eop
        
        '''
        ESQUELETO
            h0 [0:1] – tipo de mensagem
            h1 [1:2] – id do sensor
            h2 [2:3] – id do servidor
            h3 [3:4] – número total de pacotes do arquivo
            h4 [4:5] – número do pacote sendo enviado
            h5 [5:6] – se tipo for handshake:id do arquivo
                     – se tipo for dados: tamanho do payload
            h6 [6:7] – pacote solicitado para recomeço quando ha erro no envio.
            h7 [7:8] – último pacote recebido com sucesso.
            h8 [8:9] – CRC
            h9 [9:10] – CRC
            PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
            EOP – 4 bytes: 0xFF 0xAA 0xFF 0xAA
        
        TIPOS
            tipo 1 - handshake client-server
            tipo 2 - hanshake server-client
            tipo 3 - dados
            tipo 4 - verificacao server-client para msg tipo 3
            tipo 5 - timeout, quando o limite de espera excede
            tipo 6 - erro, server-client quando recebe uma msg do tipo 3 invalida
            
            
        '''
        

        
    



