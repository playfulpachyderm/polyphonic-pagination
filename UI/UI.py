from tkinter import *
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from tkinter.filedialog import askopenfilename

# from PdfToInternalRep import pdfToInternalRep


class AppMenu(Menu):
    def __init__(self, master, *args, **kwargs):
        print(type(master))

        super().__init__(master.root, *args, **kwargs)


        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open", command=master.open_pdf)

        self.add_cascade(label="File", menu=self.file_menu)


class UI(object):
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=596, height=842)
        self.canvas.pack()

        self.root.bind("<Right>", self.next_page)
        self.root.bind("<Left>", self.prev_page)

        self.menu = AppMenu(self)
        self.root.config(menu=self.menu)

        # self.open_pdf()

        self.root.mainloop()

    def open_pdf(self):
        filename = askopenfilename()
        pages = convert_from_path(filename, size=(596, 842))
        self.pages = [ImageTk.PhotoImage(x) for x in pages]

        # self.data = pdfToInternalRep(filename)

        self.CURRENT_PAGE = 0
        self.redraw()

        # For some reason this is the only effective way to re-focus keyboard input
        self.root.deiconify()

    def redraw(self):
        self.canvas.create_image(0, 0, anchor=NW, image=self.pages[self.CURRENT_PAGE])
        line = self.canvas.create_rectangle(56, 210, 197, 332, fill="red", stipple="gray50")

    def next_page(self, e):
        print("Next page")
        if self.CURRENT_PAGE >= len(self.pages) - 1:
            return
        self.CURRENT_PAGE += 1
        self.redraw()

    def prev_page(self, e):
        print("Prev page")
        if self.CURRENT_PAGE <= 0:
            return
        self.CURRENT_PAGE -= 1
        self.redraw()


#frame = Frame(tk, width=100, height=100)
# root.bind("<KeyPress>", keydown)
# root.bind("<KeyRelease>", keyup)



app = UI()
