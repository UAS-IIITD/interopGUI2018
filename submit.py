#created by Ansh Kumar Sharma 2018130

import glob
import os
import sys
import time
from PIL import Image
from PIL import ImageTk
from tkinter import PhotoImage
from tkinter import END
import tkinter as tk
from PIL import Image
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2

def images():
	im = []
	if len(sys.argv) > 1:
		for path in sys.argv[1:]:
			im.extend(images_for(path))
	else:
		im.extend(images_for(os.getcwd()))
	return im

def images_for(path):
	if os.path.isfile(path+"/mycropped"):
		return [path+"/mycropped"]
	i = []
	for match in glob.glob("mycropped/*.jpg"):
		i.append(match)    
	return i

class Out():
	def __init__(self):

		self.root=tk.Tk()
		self.root.title('Upload to Interop')
		self.root.geometry('{}x{}'.format(1350,750))

		self.leftFrame=tk.Frame(self.root,width=600,height=740,padx=3,pady=3)
		self.rightFrame=tk.Frame(self.root,width=740,height=740,padx=3,pady=3)

		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(1, weight=1)

		self.leftFrame.grid(column=0,row=0,sticky="s")
		self.rightFrame.grid(column=1,row=0)

		self.lBtmFrame=tk.Frame(self.leftFrame,width=700,height=600,padx=3,pady=3)          # for details of target

		self.lBtmFrame.grid(row=1,column=0)

		###################################### target details ##########################################

		self.labelmission=tk.Label(self.lBtmFrame,text="Mission")
		self.label1=tk.Label(self.lBtmFrame,text="Type")
		self.label2=tk.Label(self.lBtmFrame,text="Latitude")
		self.label3=tk.Label(self.lBtmFrame,text="Longitude")
		self.label4=tk.Label(self.lBtmFrame,text="Orientation")
		self.label5=tk.Label(self.lBtmFrame,text="Shape")
		self.label6=tk.Label(self.lBtmFrame,text="Background Colour")
		self.label7=tk.Label(self.lBtmFrame,text="Alphanumeric Character")
		self.label8=tk.Label(self.lBtmFrame,text="Alphanumeric Colour")
		self.label9=tk.Label(self.lBtmFrame,text="Description")


		self.mission=tk.Entry(self.lBtmFrame)

		self.text1=tk.StringVar(self.lBtmFrame)
		self.text1.set("type")

		self.option1=tk.OptionMenu(self.lBtmFrame,self.text1,"standard","emergent","off_axis")
		self.option1.config(width=25)

		self.entry2=tk.Entry(self.lBtmFrame)
		self.entry3=tk.Entry(self.lBtmFrame)

		self.text4=tk.StringVar(self.lBtmFrame)
		self.text4.set("Orientation")

		self.option4=tk.OptionMenu(self.lBtmFrame,self.text4,"n","ne","e","se","s","sw","w","nw")
		self.option4.config(width=25)
		    
		self.text5=tk.StringVar(self.lBtmFrame)
		self.text5.set("Shape")

		self.option5=tk.OptionMenu(self.lBtmFrame,self.text5,"circle","semicircle","quarter_circle","triangle","square","rectangle","trapezoid","pentagon","hexagon","heptagon","octagon","star","cross")
		self.option5.config(width=25)

		self.text6=tk.StringVar(self.lBtmFrame)
		self.text6.set("Background Colour")

		self.option6=tk.OptionMenu(self.lBtmFrame,self.text6,"white","black","gray","red","blue","green","yellow","purple","brown","orange")
		self.option6.config(width=25)

		self.entry7=tk.Entry(self.lBtmFrame)

		self.text8=tk.StringVar(self.lBtmFrame)
		self.text8.set("Alphanumeric Colour")

		self.option8=tk.OptionMenu(self.lBtmFrame,self.text8,"white","black","gray","red","blue","green","yellow","purple","brown","orange")
		self.option8.config(width=25)

		self.entry9=tk.Entry(self.lBtmFrame)

		#################### positioning of labels ###################################

		self.labelmission.grid(row=0,padx=10,pady=15)
		self.labelmission.configure(width=25)
		self.labelmission.config(font=("Courier",13))

		self.label1.grid(row=1,padx=10,pady=15)
		self.label1.config(width=25)
		self.label1.config(font=("Courier",13))

		self.label2.grid(row=2,padx=10,pady=15)
		self.label2.config(width=25)
		self.label2.config(font=("Courier",13))

		self.label3.grid(row=3,padx=10,pady=15)
		self.label3.config(width=25)
		self.label3.config(font=("Courier",13))

		self.label4.grid(row=4,padx=10,pady=15)
		self.label4.config(width=25)
		self.label4.config(font=("Courier",13))

		self.label5.grid(row=5,padx=10,pady=15)
		self.label5.config(width=25)
		self.label5.config(font=("Courier",13))

		self.label6.grid(row=6,padx=10,pady=15)
		self.label6.config(width=25)
		self.label6.config(font=("Courier",13))

		self.label7.grid(row=7,padx=10,pady=15)
		self.label7.config(width=25)
		self.label7.config(font=("Courier",13))

		self.label8.grid(row=8,padx=10,pady=15)
		self.label8.config(width=25)
		self.label8.config(font=("Courier",13))

		self.label9.grid(row=9,padx=10,pady=15)
		self.label9.config(width=25)
		self.label9.config(font=("Courier",13))

		self.mission.grid(row=0,column=1,padx=10,pady=15)
		self.mission.config(width=25)
		self.mission.config(font=("Courier",13))
		self.option1.grid(row=1,column=1,padx=10,pady=15,sticky="ew")
		self.option1.config(width=25)
		self.option1.config(font=("Courier",13))
		self.entry2.grid(row=2,column=1,padx=10,pady=15)
		self.entry2.config(width=25)
		self.entry2.config(font=("Courier",13))
		self.entry3.grid(row=3,column=1,padx=10,pady=15)
		self.entry3.config(width=25)
		self.entry3.config(font=("Courier",13))
		self.option4.grid(row=4,column=1,padx=10,pady=15)
		self.option4.config(width=25)
		self.option4.config(font=("Courier",13))     
		self.option5.grid(row=5,column=1,padx=10,pady=15)
		self.option5.config(width=25)
		self.option5.config(font=("Courier",13))
		self.option6.grid(row=6,column=1,padx=10,pady=15)
		self.option6.config(width=25)
		self.option6.config(font=("Courier",13))
		self.entry7.grid(row=7,column=1,padx=10,pady=15)
		self.entry7.config(width=25)
		self.entry7.config(font=("Courier",13))
		self.option8.grid(row=8,column=1,padx=10,pady=15)
		self.option8.config(width=25)
		self.option8.config(font=("Courier",13))
		self.entry9.grid(row=9,column=1,padx=10,pady=15)
		self.entry9.config(width=25)
		self.entry9.config(font=("Courier",13))

		self.rightFrame.grid_rowconfigure(0, weight=1)
		self.rightFrame.grid_columnconfigure(1, weight=2)

		self.topRF=tk.Frame(self.rightFrame,width=740,height=600)
		self.midRF=tk.Frame(self.rightFrame,width=740,height=50)
		self.bottomRF=tk.Frame(self.rightFrame,width=740,height=110)

		self.topRF.grid(row=0,column=0)
		self.midRF.grid(row=1,column=0,sticky="nsew")
		self.bottomRF.grid(row=2,column=0)

		self._images = images()         
		self._image_pos = -1

		self.label = tk.Label(self.topRF, image=None)
		self.label.configure(borderwidth=0)

		self.prevButton=tk.Button(self.midRF,text="Previous",command=self.show_previous_image)
		self.nextButton=tk.Button(self.midRF,text="Next",command=self.show_next_image)

		self.prevButton.grid(row=0,column=0)
		self.prevButton.config(width=27,height=3)
		self.nextButton.grid(row=0,column=1)
		self.nextButton.config(width=27,height=3)

		self.uploadButton=tk.Button(self.bottomRF,text="Upload to Interop",bg="black",fg="white",command=self.upload2Interop)

		self.uploadButton.grid(row=0,column=1,padx=3,pady=3)
		self.uploadButton.config(width=28,height=2)
		self.uploadButton.config(font=("Courier",30))

		self.root.bind("<Escape>", self.esc_handler)
		self.root.bind("<Left>", self.show_previous_image)
		self.root.bind("<Right>", self.show_next_image)

		self.root.mainloop()

	image = None

	def esc_handler(self, e):
		self.root.destroy()

	def return_handler(self, e):
		self.show_next_image()

	def show_next_image(self, e=None):
		self._images = images()
		fname = self.next_image()
		if not fname:
			return
		self.show_image(fname,self.label)

		global splPath
		splPath=fname

	def show_previous_image(self, e=None):
		self._images = images()
		fname = self.previous_image()
		if not fname:
			return
		self.show_image(fname,self.label)

		global splPath
		splPath=fname

	def show_image(self, fname,label):
		self.original_image = Image.open(fname)
		self.image = None
		self.fit_to_box(label)
		self.last_view_time = time.time()

	def fit_to_box(self,label):
		if self.image:
			if self.image.size[0] == self.box_width: return
			if self.image.size[1] == self.box_height: return
		width, height = 600,300
		new_size = scaled_size(width, height, self.box_width, self.box_height)
		new_size=(width,height)
		self.image = self.original_image.resize(new_size, Image.ANTIALIAS)
		label.place(x=self.box_width/2, y=self.box_height/2, anchor=tk.E)
		tkimage = ImageTk.PhotoImage(self.image)
		label.configure(image=tkimage)
		label.image = tkimage

	def upload2Interop(self):
		s1=s2=s3=s4=s5=s6=s7=s8=s9=None
		s0=self.mission.get()
		s1=self.text1.get()
		s2=self.entry2.get()
		s3=self.entry3.get()
		s4=self.text4.get()
		s5=self.text5.get()
		s6=self.text6.get()
		s7=self.entry7.get()
		s8=self.text8.get()
		s9=self.entry9.get()

		if s1=="":
			s1=None
		if s2=="":
			s2=None
		if s3=="":
			s3=None
		if s4=="":
			s4=None
		if s5=="":
			s5=None
		if s6=="":
			s6=None
		if s7=="":
			s7=None
		if s8=="":
			s8=None
		if s9=="":
			s9=None

		myclient = client.Client(url='http://localhost:8000',
		        username='testuser',
		        password='testpass')

		odlc = interop_api_pb2.Odlc()  
		odlc.mission = 1 
		odlc.type = interop_api_pb2.Odlc.STANDARD
		#odlc.latitude = s2
		#odlc.longitude = s3
		odlc.orientation = 4   
		odlc.shape = 5
		odlc.shape_color = 6
		odlc.alphanumeric = s7
		odlc.alphanumeric_color = 8

		odlc = myclient.post_odlc(odlc)

		currPath = self._images[self._image_pos]

		with open(currPath, 'rb') as f:
			image_data = f.read()
			myclient.put_odlc_image(odlc.id, image_data)

	@property
	def box_width(self):
		return self.root.winfo_width()

	@property
	def box_height(self):   
		return self.root.winfo_height()

	def next_image(self):
		if not self._images: 
			return None
		self._image_pos += 1
		self._image_pos %= len(self._images)
		return self._images[self._image_pos]

	def previous_image(self):
		if not self._images: 
			return None
		self._image_pos -= 1
		return self._images[self._image_pos]

def scaled_size(width, height, box_width, box_height):
	source_ratio = width / float(height)
	box_ratio = box_width / float(box_height)
	if source_ratio < box_ratio:
		return int(box_height/float(height) * width), box_height
	else:
		return box_width, int(box_width/float(width) * height)

if __name__ == '__main__': 
	out=Out()