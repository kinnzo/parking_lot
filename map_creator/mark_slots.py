from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw
import numpy as np

class Test():
    def __init__(self):
    #setting up a tkinter canvas with scrollbars
    	self.frame = Frame(root, bd=2, relief=SUNKEN)
    	self.frame.grid_rowconfigure(0, weight=1)
    	self.frame.grid_columnconfigure(0, weight=1)
    	self.xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
    	self.xscroll.grid(row=1, column=0, sticky=E+W)
    	self.yscroll = Scrollbar(self.frame)
    	self.yscroll.grid(row=0, column=1, sticky=N+S)
    	self.canvas = Canvas(self.frame, bd=0, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
    	self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
    	self.xscroll.config(command=self.canvas.xview)
    	self.yscroll.config(command=self.canvas.yview)
    	self.frame.pack(fill=BOTH,expand=1)

    	#adding the image
    	self.File = filedialog.askopenfilename(parent=root, initialdir="/home/kinnzo/Documents/rbc/data",title='Choose an image.')
    	self.source_img = Image.open(self.File)
    	self.source_img = self.source_img.resize((640,480), Image.ANTIALIAS)
    	#test_image = self.source_img
    	self.arr = np.zeros((40,30))

    	self.draw = ImageDraw.Draw(self.source_img)
    	windowsize_r = 16
    	windowsize_c = 16
    	for r in range(0,640, windowsize_r):
    	    for c in range(0,480, windowsize_c):
    	    	self.draw.rectangle(xy=[(r,c),(r+windowsize_r,c+windowsize_c)],outline="red")
    	self.out_file = "test1.jpg"
    	self.source_img.save(self.out_file, "JPEG")
    	self.img = ImageTk.PhotoImage(Image.open(self.out_file))
    	self.can_im = self.canvas.create_image(0,0,image=self.img,anchor="nw")
    	self.canvas.config(scrollregion=self.canvas.bbox(ALL))
    	self.canvas.bind("<Button 1>",self.printcoords)

    def changeImg(self):
        self.newimg = ImageTk.PhotoImage(Image.open(self.out_file))
        self.canvas.itemconfig(self.can_im,image=self.newimg)
    #function to be called when mouse is clicked
    def printcoords(self,event):
        #outputting x and y coords to console
        self.src_img = Image.open(self.out_file)
        self.src_img = self.src_img.resize((640,480), Image.ANTIALIAS)
        self.srcdraw = ImageDraw.Draw(self.src_img)
        self.netx, self.nety = event.x//16,event.y//16
        self.arr[self.netx][self.nety] = 1
        np.savetxt("map.csv",self.arr,delimiter=",")
        #print(self.netx,self.nety)
        self.srcdraw.rectangle(xy=[(16*self.netx,16*self.nety),(16*self.netx+16,16*self.nety+16)],fill="green")
        self.src_img.save(self.out_file, "JPEG")
        self.out_img = ImageTk.PhotoImage(Image.open(self.out_file))
        #print (event.x,event.y)
        self.changeImg()
    #mouseclick event
root = Tk()
root.geometry("800x600")
app = Test()   

root.mainloop()
