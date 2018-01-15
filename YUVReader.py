from tkinter import *
from tkinter import filedialog
import PIL
from PIL import ImageTk, Image
import math
import os


savename='null'
def donothing():
	print("donothing")
	
class Converter(object):
	"""Base class that should define interface for all conversions"""
	def __init__(self, filename, width, height, stride, frame,temp):
		self.filename = filename
		self.width = width
		self.height = height
		self.stride = stride
		self.frame = frame
		self.temp = temp
	#constructor#

	def Convert():
		raise NotImplementedError( "Should have implemented this!" )
	#convert#
#Converter#



class NV12Converter(Converter):
	"""This class converts NV12 files into RGB"""
	def __init__(self, filename, width, height, stride, frame, temp):
		super(NV12Converter, self).__init__(filename, width, height, stride, frame,temp)
	#constructor#

	
	def Convert(self):
		f_y = open(self.filename, "rb")
		f_uv= open(self.filename, "rb")
		

		converted_image_filename = self.filename.split('.')[0] + ".bmp"

		converted_image = Image.new("RGB", (self.width, self.height) )
		pixels = converted_image.load()

		size_of_file = os.path.getsize(self.filename)
		size_of_frame = ((3.0/2.0)*self.height*self.width)
		number_of_frames = size_of_file / size_of_frame
		frame_start = size_of_frame * self.frame
		uv_start = frame_start + (self.width*self.height)
        
 		#lets get our y cursor ready
		f_y.seek(int(frame_start));        
		for j in range(0, self.height):
			for i in range(0, self.width):
				#uv_index starts at the end of the yframe.  The UV is 1/2 height so we multiply it by j/2
				#We need to floor i/2 to get the start of the UV byte
				uv_index = uv_start + (self.width * math.floor(j/2)) + (math.floor(i/2))*2
				f_uv.seek(int(uv_index))
				
				y = ord(f_y.read(1))
				u = ord(f_uv.read(1))
				v = ord(f_uv.read(1))
				
				b = 1.164 * (y-16) + 2.018 * (u - 128)
				g = 1.164 * (y-16) - 0.813 * (v - 128) - 0.391 * (u - 128)
				r = 1.164 * (y-16) + 1.596*(v - 128)
	
				pixels[i,j] = int(r), int(g), int(b)	
		if self.temp==0 :			
			return converted_image
		elif self.temp ==1:
			converted_image.save(converted_image_filename)
		elif self.temp ==2:
			global savename
			savename2=savename+".bmp"
			converted_image.save(savename2)
		
def main():
	window=Tk();
	window.title('YUV Reader') # 타이틀
	#window.pack()
	window.config(width=800, height=500)
	#window.geometry('650x600') # 창 크기
	#window.geometry('650x490+500+10') # 창 크기와 창의 위치
	#window.resizable(0, 0) # 창의 x와 y 의 크기 조절 불가능

	
	mainframe=Frame(window);
	mainframe.config(width=800, height=500)
	menubar = Menu(mainframe);
	
	#secondframe=Frame(window);
	#secondframe.place(x=20,y=40)
	mainframe.pack()
	#secondframe.pack(side=LEFT, fill=X)
	
	
	
	d1=Label()
	filename='null'
	
	##statusbar##
	status = Label(window, text="Ready", bd=1, relief=SUNKEN, anchor=W)
	status.pack(side=BOTTOM, fill=X)
	
	def load():
		global filename
		filename =  filedialog.askopenfilename(initialdir = "C:/%USERPROFILE%/Desktop",title = "choose your file",filetypes = (("yuv files","*.yuv"),("all files","*.*")))
		converter = NV12Converter(filename, 640, 480, 640, 0,0)
		converter.Convert()
	
		#image = Image.open(filename)
		photo = ImageTk.PhotoImage(converter.Convert())
		d1.image=photo
		d1.destroy()
		Label.__init__(d1,mainframe,image=d1.image,bd=0) 
		d1.pack(side=TOP, fill=Y)
		
		os.path.split(filename)
		os.path.split(filename)[1]
		status.destroy()
		#status.__init__(window, text=os.path.split(filename)[1], bd=1, relief=SUNKEN, anchor=W)
		status.__init__(window, text=os.path.basename(filename), bd=1, relief=SUNKEN, anchor=W)
		status.pack(side=BOTTOM, fill=X)
		
		
	def save():
		global filename
		converter = NV12Converter(filename, 640, 480, 640, 0,1)
		converter.Convert()
		
		status.destroy()
		status.__init__(window, text="save complete", bd=1, relief=SUNKEN, anchor=W)
		status.pack(side=BOTTOM, fill=X)
		
	def saveas():
		global filename
		global savename
		savename =  filedialog.asksaveasfilename(initialdir = "/",title = "Save as",filetypes = (("BMP files","*.bmp"),("all files","*.*")))
		converter = NV12Converter(filename, 640, 480, 640, 0,2	)
		converter.Convert()
		
		status.destroy()
		status.__init__(window, text="SaveTo: "+savename+".bmp", bd=1, relief=SUNKEN, anchor=W)
		status.pack(side=BOTTOM, fill=X)		
		
	def infomation():
	   filewin = Toplevel(mainframe)
	   label = Label(filewin, text="Version : 1.0 \n  sehyeon.byeon@sony.com")
	   label.grid(row=0,column=1)
	   button = Button(filewin, text="close",command=filewin.destroy)
	   button.grid(row=1,column=1)
	
	def clear():
		d1.delete('0.0', END)
	
	def menubar1():
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open", command=load)
		filemenu.add_command(label="Save", command=save)
		filemenu.add_command(label="Save As...", command=saveas)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=mainframe.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		
		#editmenu = Menu(menubar, tearoff=0)
		#editmenu.add_command(label="Undo", command=donothing)
		#editmenu.add_separator()
		#editmenu.add_command(label="Cut", command=donothing)
		#editmenu.add_command(label="Copy", command=donothing)
		#editmenu.add_command(label="Paste", command=donothing)
		#editmenu.add_command(label="Delete", command=donothing)
		#editmenu.add_command(label="Select All", command=donothing)
		#menubar.add_cascade(label="Edit", menu=editmenu)
		
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About...", command=infomation)
		menubar.add_cascade(label="Help", menu=helpmenu)
		
	
		
	menubar1()
	#statusbar1()
	
	window.config
	window.config(menu=menubar)
	window.mainloop()

			
main()						

