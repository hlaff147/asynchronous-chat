from tkinter import *
from PIL import *
from PIL import Image, ImageTk


class MessageScreen(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack_propagate(False)
        self.bg = kwargs['bg']

    def display_text(self, text):
        Label(self, text=text, bg=self.bg, justify=LEFT, anchor='w').pack(fill=X)

    def clear(self):
        for child in self.winfo_children():
            child.destroy()

    def display_image(self, filename):
        img = Image.open(filename)
        img = img.resize((100, 100))
        self.photo = ImageTk.PhotoImage(img)
        Label(self,
              image=self.photo,
              bg=self.bg,
              justify=LEFT,
              anchor='w'
          ).pack(fill=X)


