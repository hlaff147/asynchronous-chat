from tkinter import *


class GUI():

	def __init__(self, largura, altura):
		self.window = Tk()
		self.canva = Canvas(self.window, width=largura, height=altura)
		self.canva.grid(columnspan=3)
		self.createWidgets()


	def createWidgets(self):
		self.txt_area = Text(self.canva, border=1)
		self.txt_field = Entry(self.canva, width=85, border=1, bg='white')
		self.send_button = Button(self.canva, text='Enviar', padx=40, command=self.send)
		self.arquivar_button = Button(self.canva, text='Arquivar', padx=40, command=None)
		
		self.txt_area.config(background='#c8a2c8')

		self.txt_area.grid(column=0, row=0, columnspan=3)
		self.txt_field.grid(column=0, row=1, columnspan=2)
		self.send_button.grid(column=2, row=1)
		self.arquivar_button.grid(column=3, row=1)
	

	def send(self, event=None):
		texto = self.txt_field.get() + '\n'
		self.txt_area.insert(END, texto)
		self.txt_field.delete(0, END)
	
	
	def start(self):
		self.window.mainloop()


interface = GUI(600, 800).start()