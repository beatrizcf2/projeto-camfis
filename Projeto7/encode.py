
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

#definindo os parametros + dicionario
fs = 44100
amplitude = 100
time = 3
numbers = {"1":[1209,697],
"2": [1336,697],
"3": [1477,697],
"A": [1633,697],
"4": [1209,770],
"5": [1336,770],
"6": [1477,770],
"B": [1633,770],
"7": [1209,852],
"8": [1336,852],
"9": [1477,852],
"C": [1633,852],
"X": [1209,941],
"0": [1336,941],
"#": [1477,941],
"D": [1633,941],
}



def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder...\n")
    number = input("Escolha um número entre 0 a 9: ")
    
    print("Gerando Tons base...\n")
    freq1 = int(numbers[number][0])
    freq2 = int(numbers[number][1])
    x1, s1 = signalMeu.generateSin(0,freq1, amplitude, time, fs)
    x2, s2 = signalMeu.generateSin(0,freq2, amplitude, time, fs)
    
    signal = s1+s2
    
    print("Executando as senoides (emitindo o som)")
    print(f"Gerando Tom referente ao símbolo : {number}")
    sd.play(signal, fs)
    sd.wait() # aguarda fim do audio
    
    # Exibe gráficos
    x,y = signalMeu.calcFFT(0,signal, fs)
    plt.figure()
    plt.plot(x, np.abs(y))
    plt.title('Fourier')
    plt.show()
    
    
    

if __name__ == "__main__":
    main()
