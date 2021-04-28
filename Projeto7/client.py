# -*- coding:utf-8 -*-
import struct
import numpy as np
from scipy import signal as sg
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt

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

number = input("Escolha um número entre 0 a 9: ")
amplitude = 1
time = 3
fs = 44100

freq1 = int(numbers[number][0])
print(f"freq1: {freq1}")
x1, s1 = signalMeu.generateSin(0,freq1, amplitude, time, fs)
freq2 = numbers[number][1]
x2, s2 = signalMeu.generateSin(0,freq2, amplitude, time, fs)

signal = s1+s2
print(signal)

with open("test.wav", "wb") as file:
    for i in signal:
        file.write(struct.pack('b',int(i)))

plt.figure()
plt.plot(x1, signal)
plt.title('Signal')
plt.show()



