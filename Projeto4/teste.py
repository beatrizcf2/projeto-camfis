# Fonte: https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/


# import the time module
import time
  
# define the countdown func.
def countdown(size, t):
    # fica dentro do loop ate t=0
    while t>0:
        mins, secs = divmod(t, 60) #calcula o n de min e seg
        timer = '{:02d}:{:02d}'.format(int(mins), int(secs))
        print(timer, end="\r") #print q sobrepoe o anterior
        time.sleep(0.1) #conta 1 seg
        t -= 0.1
      
    print('Fire in the hole!!')
  
  
# input time in seconds
#t = input("Enter the time in seconds: ")
  
# function call
#countdown(int(t))

def writeLog(client, typeAction, typeMsg, lenMsg, idPckg, numberPckg):
    tempo = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if client:
        file = open("Client1.txt", "a")
    else:
        file = open("Server1.txt", "a")
    
    log = tempo + '/ ' + typeAction + '/ ' + str(typeMsg) + '/ ' + str(lenMsg)
    if typeMsg == 3:
        log += '/ ' + str(idPckg) + '/ ' + str(numberPckg)
    file.write(log + '\n')
    file.close()

writeLog(True, 'envio', 3, 14, 0, 50)
