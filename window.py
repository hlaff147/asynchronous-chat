from tkinter import *
from time import gmtime, strftime
from tkinter import filedialog
from PIL import *
import os

from PIL import Image, ImageTk



class GUI():

    def __init__(self):
        self.window = Tk()
        self.window.title('Asynchronous Chat')
        self.label_file_explorer = None
        self.createWidgets()

    def createWidgets(self):
        self.txt_area = Frame(self.window, border=1, bg='#c8a2c8', width=700, height=300)

        self.txt_field = Entry(self.window, bg='white')
        self.send_button = Button(self.window, text='Enviar',  command=None)
        self.file_button = Button(self.window, text='Arquivo', command=None)
        self.clear_button = Button(self.window, text='Limpar', command=None)

        self.window.bind('<Return>', self.send)

        self.txt_area.grid(row=0, column=0, columnspan=5)
        self.txt_field.grid(row=1, column=0, columnspan=2, stick='ew', padx=(5, 0))
        self.send_button.grid( row=1, column=2, padx=0, pady=7)
        self.file_button.grid( row=1, column=3, padx=0)
        self.clear_button.grid(row=1, column=4, padx=0)

        self.window.columnconfigure(0, weight=4)
        self.window.columnconfigure(1, weight=1)

        #self.label_file_explorer = Label(self.canva,   text = "File Explorer using Tkinter", width = 100, height = 4,    fg = "blue")
        #button_explore = Button(self.canva, text = "Browse Files", command = self.browseFiles)
        #button_exit = Button(self.canva, text = "Exit", command = exit)
        #self.label_file_explorer.grid()
        #button_explore.grid()
        #button_exit.grid()


    def send(self, event=None):
        texto = '[' + strftime("%H:%M", gmtime()) + ']:' + " " + self.txt_field.get() + '\n'
        self.txt_area.insert(END, texto)
        self.txt_field.delete(0, END)


    def clear(self, event=None):
        self.txt_area.delete("1.0","end")

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                            title = "Select a File",
                            filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))

        self.uploadFile(filename)

    def uploadFile(self, filename):
        img = Image.open(filename)
        self.photo = ImageTk.PhotoImage(img)
        self.canva.create_image(20, 20, anchor = NW, image = self.photo)
        self.txt_area.insert(END, self.photo)



    def start(self):
        self.window.mainloop()


interface = GUI().start()
