#created by Ansh Kumar Sharma 2018130

from geoloc import gp
import glob
import os
import sys
import time
from PIL import Image
from PIL import ImageTk
import json
from tkinter import PhotoImage
from tkinter import END
import tkinter as tk
from collections import OrderedDict
import pygame
import pickle

gpcrop = {}

pygame.init()

def images():
	im = []
	if len(sys.argv) > 1:
		for path in sys.argv[1:]:
			im.extend(images_for(path))
	else:
		im.extend(images_for(os.getcwd()))
	return sorted(im)

def images_for(path):
	if os.path.isfile(path+"/images"):
		return [path+"/images"]
	i = []
	for match in glob.glob("images/*.jpg"):
		i.append(match)    
	return i

class App():
	def __init__(self):

		self.index = 1

		self.root=tk.Tk()
		self.root.title('Crop Image')
		self.root.geometry('{}x{}'.format(1350,750))

		self.topRF=tk.Frame(self.root,width=740,height=600)
		self.midRF=tk.Frame(self.root,width=740,height=50)

		self.topRF.grid(row=0,column=0)
		self.midRF.grid(row=1,column=0,sticky="nsew")

		self._images = images()         
		self._image_pos = -1

		self.label = tk.Label(self.topRF, image=None)
		self.label.configure(borderwidth=0)

		self.prevButton=tk.Button(self.midRF,text="Previous",command=self.show_previous_image)
		self.nextButton=tk.Button(self.midRF,text="Next",command=self.show_next_image)
		self.cropButton=tk.Button(self.midRF,text="Crop",command=self.crop_image)

		self.prevButton.grid(row=0,column=0)
		self.prevButton.config(width=27,height=3)
		self.nextButton.grid(row=0,column=1)
		self.nextButton.config(width=27,height=3)
		self.cropButton.grid(row=0,column=2)
		self.cropButton.config(width=28,height=3)

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

	def crop_image(self):

		global splPath

		input_loc = splPath
		screen, px = self.setup(input_loc)
		left, upper, right, lower = self.mainLoop(screen, px)

		# ensure output rect always has positive width, height
		if right < left:
			left, right = right, left
		if lower < upper:
			lower, upper = upper, lower

		print(input_loc)
		im = Image.open(input_loc)
		im = im.resize((1280,720), Image.ANTIALIAS)
		im = im.crop(( left, upper, right, lower))
		pygame.display.quit()

		new_width  = 100
		new_height = 100
		im = im.resize((new_width, new_height), Image.ANTIALIAS)
		im.save("/home/anshks/interop/client/mycropped/"+str(self.index)+".jpg")
		self.index += 1
		try:
			gpcrop[str(self.index-1)+".jpg"] = gp[input_loc[7:]]
		except KeyError:
			print("OOPs")

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

	def displayImage(self,screen, px, topleft, prior):
		# ensure that the rect always has positive width, height
		x, y = topleft
		width =  pygame.mouse.get_pos()[0] - topleft[0]
		height = pygame.mouse.get_pos()[1] - topleft[1]
		if width < 0:
			x += width
			width = abs(width)
		if height < 0:
			y += height
			height = abs(height)

		# eliminate redundant drawing cycles (when mouse isn't moving)
		current = x, y, width, height
		if not (width and height):
			return current
		if current == prior:
			return current

		# draw transparent box and blit it onto canvas
		screen.blit(px, px.get_rect())
		im = pygame.Surface((width, height))
		im.fill((128, 128, 128))
		pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
		im.set_alpha(128)
		screen.blit(im, (x, y))
		pygame.display.flip()

		# return current box extents
		return (x, y, width, height)

	def setup(self,path):
		px = pygame.image.load(path)
		px = pygame.transform.scale(px, (1280, 720))
		screen = pygame.display.set_mode([1280,720])
		screen.blit(px, px.get_rect())
		pygame.display.flip()
		return screen, px

	def mainLoop(self,screen, px):
		topleft = bottomright = prior = None
		n=0
		while n!=1:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					if not topleft:
						topleft = event.pos
					else:
						bottomright = event.pos
						n=1
			if topleft:
				prior = self.displayImage(screen, px, topleft, prior)
		return ( topleft + bottomright )

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

def saveDict(dictionary):
	with open("gpcrop.txt", "wb") as myFile:
		pickle.dump(dictionary, myFile)

if __name__ == '__main__':
	app=App()
	saveDict(gpcrop)
