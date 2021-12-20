from tkinter import *
from time import gmtime, strftime
from tkinter import filedialog
from PIL import *
import os
import re
import socket
from threading import Thread
from random import randint

from message_screen import MessageScreen


class GUI():

    BACKGROUND_COLOR = '#c8a2c8'
    SUPPORTED_VIDEO_FORMATS = ['mp4']
    SUPPORTED_AUDIO_FORMATS = ['wav', 'mp3']

    def __init__(self):
        self.window = Tk()
        self.window.title('Asynchronous Chat')
        self.label_file_explorer = None
        self.createWidgets()

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('localhost', 50000))
            self.s.listen(1)
            self.conn, addr = self.s.accept()
            self._socket = self.conn
        except:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(('localhost', 50000))
            self._socket = self.s
        finally:
            Thread(target=self.chat_recv, daemon=True).start()

    def chat_recv(self):
        while True:
            msg_type = self._socket.recv(5)
            msg_type = msg_type.decode('utf-8')

            if msg_type == 'TEXTX':
                msg = self._socket.recv(1024)
                msg = msg.decode('utf-8')
                self.txt_area.display_text(msg)
                return

            self.txt_area.display_text('[' + strftime('%H:%M') + ']:')

            if msg_type == 'IMAGE':
                with open('income.jpg', 'wb') as f:
                    while True:
                        data = self._socket.recv(512)
                        f.write(data)
                        if len(data) < 512:
                            break
                self.txt_area.display_image('income.jpg')

            elif msg_type == 'AUDIO':
                with open('income.wav', 'wb') as f:
                    while True:
                        data = self._socket.recv(512)
                        f.write(data)
                        if len(data) < 512:
                            break
                self.txt_area.display_audio('income.wav')

            elif msg_type == 'VIDEO':
                with open('income.mp4', 'wb') as f:
                    while True:
                        data = self._socket.recv(512)
                        f.write(data)
                        if len(data) < 512:
                            break
                self.txt_area.display_video('income.mp4')

    def createWidgets(self):
        self.txt_area = MessageScreen(self.window, border=1, bg=self.BACKGROUND_COLOR, width=700, height=300)

        self.txt_field = Entry(self.window, bg='white')
        self.send_button = Button(self.window, text='Enviar',  command=self.chat_send)
        self.file_button = Button(self.window, text='Arquivo', command=self.browseFiles)
        self.clear_button = Button(self.window, text='Limpar', command=self.clear)

        self.window.bind('<Return>', self.chat_send)

        self.txt_area.grid(row=0, column=0, columnspan=5)
        self.txt_field.grid(row=1, column=0, columnspan=2, stick='ew', padx=(5, 0))
        self.send_button.grid( row=1, column=2, padx=0, pady=7)
        self.file_button.grid( row=1, column=3, padx=0)
        self.clear_button.grid(row=1, column=4, padx=0)

        self.window.columnconfigure(0, weight=4)
        self.window.columnconfigure(1, weight=1)


    def chat_send(self, event=None):
        texto = '[' + strftime("%H:%M") + ']:' + " " + self.txt_field.get() + '\n'
        self._socket.send('TEXTX'.encode())
        self._socket.send(texto.encode())
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
            self._socket.send('VIDEO'.encode())
        elif re.match(r'.*\.(' + '|'.join(self.SUPPORTED_AUDIO_FORMATS) + ')', filename) is not None:
            self.txt_area.display_audio(filename)
            self._socket.send('AUDIO'.encode())
        else:
            self.txt_area.display_image(filename)
            self._socket.send('IMAGE'.encode())

        with open(filename, 'rb') as f:
            while True:
                l = f.read(512)
                if not l:
                    break
                self._socket.send(l)


    def start(self):
        self.window.mainloop()


interface = GUI().start()
