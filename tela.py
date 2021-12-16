from tkinter import *
from time import gmtime, strftime


class GUI():

	def __init__(self, width, height):
		self.window = Tk()
		self.window.title('Asynchronous Chat')
		self.canva = Canvas(self.window, width=width, height=height)
		self.canva.grid(columnspan=3)
		self.createWidgets()


	def createWidgets(self):
		self.txt_area = Text(self.canva, border=1)
		self.txt_field = Entry(self.canva, width=85, border=1, bg='white')
		self.send_button = Button(self.canva, text='Send', padx=40, command=self.send)
		self.archive_button = Button(self.canva, text='Archive', padx=40, command=None)
		self.clean_button = Button(self.canva, text='Clean', padx=40, command=self.clear)
		
		self.window.bind('<Return>', self.send)
		self.txt_area.config(background='#c8a2c8')

		self.txt_area.grid(column=0, row=0, columnspan=3)
		self.txt_field.grid(column=0, row=1, columnspan=2)
		self.send_button.grid(column=2, row=1)
		self.archive_button.grid(column=3, row=1)
		self.clean_button.grid(column=4, row=1)
	

	def send(self, event=None):
		texto = '[' + strftime("%H:%M", gmtime()) + ']:' + " " + self.txt_field.get() + '\n'
		self.txt_area.insert(END, texto)
		self.txt_field.delete(0, END)


	def clear(self, event=None):
		self.txt_area.delete("1.0","end")


	def start(self):
		self.window.mainloop()


interface = GUI(600, 800).start()