import tkinter as tk
from tkinter import filedialog

# https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
def image_picker():
	root = tk.Tk()
	root.withdraw()

	return filedialog.askopenfilename(title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

def calculate_baudrate(start, end, nBytes):
    return nBytes/(end-start)

