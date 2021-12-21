from tkinter import *


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, bg, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                    yscrollcommand=vscrollbar.set,bg=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas,bg=bg)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                       anchor=NW)


        #This would create a frame that had actually the size of the whole window height
        #I have tested so much with options and haven't found a way to make it work correctly without this
        a = Frame(self.interior,height=10,bg=bg)
        a.pack()

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                    # update the canvas's width to fit the inner frame
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            #With this piece of code, the "a" frame adapts its height to the elements inside. 
            a.configure(height=10)
            a.update()
            mylist = interior.winfo_children()
            for i in mylist:
                lasty=i.winfo_height()+i.winfo_y()
            a.configure(height=lasty)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)


if __name__ == '__main__':
    root = Tk()
    frame = VerticalScrolledFrame(root, bg='red')
    frame.pack()

    for i in range(50):
        Label(frame.interior,
              text=str(i)
        ).pack()

    root.mainloop()

