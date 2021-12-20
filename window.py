from tkinter import *
from time import gmtime, strftime
from tkinter import filedialog
from PIL import *
import os
from message_screen import MessageScreen
import re


class GUI():

    BACKGROUND_COLOR = '#c8a2c8'
    SUPPORTED_VIDEO_FORMATS = ['mp4']
    SUPPORTED_AUDIO_FORMATS = ['wav', 'mp3']

    def __init__(self):
        self.window = Tk()
        self.window.title('Asynchronous Chat')
        self.label_file_explorer = None
        self.createWidgets()

    def createWidgets(self):
        self.txt_area = MessageScreen(self.window, border=1, bg=self.BACKGROUND_COLOR, width=700, height=300)

        self.txt_field = Entry(self.window, bg='white')
        self.send_button = Button(self.window, text='Enviar',  command=self.send)
        self.file_button = Button(self.window, text='Arquivo', command=self.browseFiles)
        self.clear_button = Button(self.window, text='Limpar', command=self.clear)

        self.window.bind('<Return>', self.send)

        self.txt_area.grid(row=0, column=0, columnspan=5)
        self.txt_field.grid(row=1, column=0, columnspan=2, stick='ew', padx=(5, 0))
        self.send_button.grid( row=1, column=2, padx=0, pady=7)
        self.file_button.grid( row=1, column=3, padx=0)
        self.clear_button.grid(row=1, column=4, padx=0)

        self.window.columnconfigure(0, weight=4)
        self.window.columnconfigure(1, weight=1)


    def send(self, event=None):
        texto = '[' + strftime("%H:%M") + ']:' + " " + self.txt_field.get() + '\n'
        self.txt_area.display_text(texto)
        self.txt_field.delete(0, END)


    def clear(self, event=None):
        self.txt_area.clear()

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                            title = "Select a File",
                            filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))

        self.uploadFile(filename)

    def uploadFile(self, filename):
        self.txt_area.display_text('[' + strftime('%H:%M') + ']:')

        if re.match(r'.*\.(' + '|'.join(self.SUPPORTED_VIDEO_FORMATS) + ')', filename) is not None:
            self.txt_area.display_video(filename)
        elif re.match(r'.*\.(' + '|'.join(self.SUPPORTED_AUDIO_FORMATS) + ')', filename) is not None:
            self.txt_area.display_audio(filename)
        else:
            self.txt_area.display_image(filename)

    def start(self):
        self.window.mainloop()


interface = GUI().start()
