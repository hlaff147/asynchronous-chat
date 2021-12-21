from tkinter import *
from time import strftime
from tkinter import filedialog
from PIL import *
import re
import socket
from threading import Thread

from message_screen import MessageScreen


class GUI():
    BACKGROUND_COLOR = '#c8a2c8'
    SUPPORTED_VIDEO_FORMATS = ['mp4']
    SUPPORTED_AUDIO_FORMATS = ['wav', 'mp3']
    SUPPORTED_IMAGE_FORMATS = ['jpg', 'png']
    RECEIVED_FILE_COUNTER = 0

    def __init__(self):
        self.window = Tk()
        self.window.title('Asynchronous Chat')
        self.label_file_explorer = None
        self.createWidgets()

        self.video_regex = re.compile(r'.*\.(' + '|'.join(self.SUPPORTED_VIDEO_FORMATS) + ')')
        self.audio_regex = re.compile(r'.*\.(' + '|'.join(self.SUPPORTED_AUDIO_FORMATS) + ')')
        self.image_regex = re.compile(r'.*\.(' + '|'.join(self.SUPPORTED_IMAGE_FORMATS) + ')')

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

    def get_infilename(self, extension):
        self.RECEIVED_FILE_COUNTER += 1
        return f'TRANSFER_FILE{self.RECEIVED_FILE_COUNTER}.{extension}'

    def chat_recv(self):
        while True:
            msg_type = self._socket.recv(5)
            msg_type = msg_type.decode('utf-8')

            if msg_type == '':
                break

            if msg_type == 'TEXTX':
                msg = self._socket.recv(1024)
                msg = msg.decode('utf-8')
                self.txt_area.display_text(msg)
                continue

            self.txt_area.display_text(strftime('[%x %X]:'))

            extension = self._socket.recv(10).decode('utf-8')
            extension = re.match(r'([^-]+).*', extension).group(1)
            filename = self.get_infilename(extension)

            with open(filename, 'wb') as f:
                while True:
                    data = self._socket.recv(512)
                    f.write(data)
                    if len(data) < 512:
                        break

            if msg_type == 'IMAGE':
                self.txt_area.display_image(filename)
            elif msg_type == 'AUDIO':
                self.txt_area.display_audio(filename)
            elif msg_type == 'VIDEO':
                self.txt_area.display_video(filename)
            else:
                self.txt_area.display_text('Transferiu arquivo ' + extension)

    def createWidgets(self):
        self.txt_area = MessageScreen(self.window, border=1, bg=self.BACKGROUND_COLOR, width=700, height=300)
        self.txt_area.grid(row=0, column=0, columnspan=5, sticky='nswe')
        self.txt_area.columnconfigure(0,weight=1)
        self.txt_area.rowconfigure(0, weight=1)

        self.txt_field = Entry(self.window, bg='white')
        self.txt_field.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)
        self.txt_field.columnconfigure(0, weight=2)
        self.send_button = Button(self.window, text='Enviar', command=self.chat_send)
        self.send_button.grid(row=1, column=1, pady=5)
        self.send_button.columnconfigure(0, weight=1)
        self.file_button = Button(self.window, text='Arquivo', command=self.browseFiles)
        self.file_button.grid(row=1, column=2, pady=5)
        self.file_button.columnconfigure(0, weight=1)
        self.clear_button = Button(self.window, text='Limpar', command=self.clear)
        self.clear_button.grid(row=1, column=3, padx=(0,5), pady=5)
        self.clear_button.columnconfigure(0, weight=1)

        self.window.bind('<Return>', self.chat_send)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

    def chat_send(self, event=None):
        texto = self.txt_field.get()

        if texto.isspace() or texto == '':
            return

        texto = strftime('[%x %X]:') + " " + self.txt_field.get()

        self._socket.send('TEXTX'.encode())
        self._socket.send(texto.encode())
        self.txt_area.display_text(texto)
        self.txt_field.delete(0, END)

    def clear(self, event=None):
        self.txt_area.clear()

    def browseFiles(self):
        filename = filedialog.askopenfilename(title="Select a File")
        if filename:
            self.uploadFile(filename)

    def uploadFile(self, filename):
        self.txt_area.display_text(strftime('[%x %X]:'))
        extension = re.match(r'.*\.(.+)', filename).group(1)

        if self.video_regex.match(filename) is not None:
            self.txt_area.display_video(filename)
            self._socket.send('VIDEO'.encode())

        elif self.audio_regex.match(filename) is not None:
            self.txt_area.display_audio(filename)
            self._socket.send('AUDIO'.encode())

        elif self.image_regex.match(filename) is not None:
            self.txt_area.display_image(filename)
            self._socket.send('IMAGE'.encode())

        else:
            self.txt_area.display_text('Transferiu arquivo ' + extension)
            self._socket.send('FILEX'.encode())

        extension_code = extension + '-' * (10 - len(extension))
        self._socket.send(extension_code.encode())

        with open(filename, 'rb') as f:
            while True:
                l = f.read(512)
                if not l:
                    break
                self._socket.send(l)

    def start(self):
        self.window.mainloop()
        self._socket.close()


interface = GUI().start()
