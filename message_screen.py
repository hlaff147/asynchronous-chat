from tkinter import *
from PIL import *
from PIL import Image, ImageTk
import imageio
from threading import Thread
import platform
from vertical_scrolled_frame import VerticalScrolledFrame

if platform.system() == 'Windows':
    import winsound
    def play_sound(filename):
        winsound.PlaySound(filename, winsound.SND_FILENAME)
else:
    from playsound import playsound
    def play_sound(filename):
        playsound(filename, False)


class MessageScreen(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack_propagate(False)
        self.bg = kwargs['bg']

        self.frame = VerticalScrolledFrame(self, bg=self.bg)
        self.frame.pack(fill=BOTH)
        self.photos = []

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
        self.photos.append(ImageTk.PhotoImage(img))
        Label(self.viewport,
              image=self.photos[-1],
              bg=self.bg,
              justify=LEFT,
              anchor='w'
          ).pack(fill=X)

    def stream(self, video, label):
        for image in video.iter_data():
            frame_image = Image.fromarray(image)
            frame_image = frame_image.resize((100, 100))
            frame_image = ImageTk.PhotoImage(frame_image)
            label.config(image=frame_image)
            label.image = frame_image

    def display_video(self, filename):
        video = imageio.get_reader(filename)
        delay = int(1000 / video.get_meta_data()['fps'])
        label = Label(self.viewport,
              bg=self.bg,
              justify=LEFT,
              anchor='w'
        )
        label.pack(fill=X)
        Thread(target=self.stream, args=(video, label), daemon=True).start()

    def display_audio(self, filename):
        play_label = Label(self.viewport,
                           bg=self.bg,
                           justify=LEFT,
                           anchor='w'
        )
        play_label.pack(fill=X)
        Button(play_label,
               text='Play',
               command=lambda: play_sound(filename)
        ).pack()

