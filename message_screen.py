from tkinter import *
from PIL import *
from PIL import Image, ImageTk
import imageio
from threading import Thread
from playsound import playsound

from tmp import VerticalScrolledFrame


class MessageScreen(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack_propagate(False)
        self.bg = kwargs['bg']

        self.frame = VerticalScrolledFrame(self, bg=self.bg)
        self.frame.pack(fill=BOTH)

    @property
    def viewport(self):
        return self.frame.interior

    def display_text(self, text):
        Label(self.viewport, text=text, bg=self.bg, justify=LEFT, anchor='w').pack(fill=X)

    def clear(self):
        for child in self.viewport.winfo_children():
            child.destroy()
        self.frame.canvas.yview_moveto(0)

    def display_image(self, filename):
        img = Image.open(filename)
        img = img.resize((100, 100))
        self.photo = ImageTk.PhotoImage(img)
        Label(self.viewport,
              image=self.photo,
              bg=self.bg,
              justify=LEFT,
              anchor='w'
          ).pack(fill=X)

    def stream(self):
        for image in self.video.iter_data():
            frame_image = Image.fromarray(image)
            frame_image = frame_image.resize((100, 100))
            frame_image = ImageTk.PhotoImage(frame_image)
            self.l.config(image=frame_image)
            self.l.image = frame_image

    def display_video(self, filename):
        self.video = imageio.get_reader(filename)
        delay = int(1000 / self.video.get_meta_data()['fps'])
        self.l = Label(self.viewport,
              bg=self.bg,
              justify=LEFT,
              anchor='w'
        )
        self.l.pack(fill=X)
        Thread(target=self.stream, daemon=True).start()

    def display_audio(self, filename):
        play_label = Label(self.viewport,
                           bg=self.bg,
                           justify=LEFT,
                           anchor='w'
        )
        play_label.pack(fill=X)
        Button(play_label,
               text='Play',
               command=lambda: playsound(filename)
        ).pack()

