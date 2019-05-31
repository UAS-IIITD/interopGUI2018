"""Updated last year's GUI"""

#!/usr/bin/env python

import glob
import os
import sys
import time
from PIL import Image
from PIL import ImageTk
import json
import interop
#import py3exiv2
from tkinter import PhotoImage
from tkinter import END
import tkinter as tk
from resizeimage import resizeimage
from collections import OrderedDict
# import pyexiv2
# import mypath
import pygame
from PIL import Image
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
#from google.protobuf import json_format
#from mavlink_proxy import MavlinkProxy
#from upload_odlcs import upload_odlcs
pygame.init()                       # initialise pygame

splPath=None

croppedPath=None

#class geo:
#    def ___init__(self):
#        self.value=0

def images():
    im = []
    print(sys.argv,1)
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            im.extend(images_for(path))
            print(path)
    else:
        im.extend(images_for(os.getcwd()))              #try changing os.getcwd() to your preferred directory
    print(im)
    return sorted(im)
    #return sorted(im, key=lambda s:s.lower())

def images_for(path):
    if os.path.isfile(path):
        return [path]
    i = []
    for match in glob.glob("*.jpg"):
        print (match)
        i.append(match)    
    return i


class App():
    def __init__(self):

        self.index1=1
        self.index2=1

        self.root=tk.Tk()
        self.root.title('Upload to Interop')
        self.root.geometry('{}x{}'.format(1350,750))

        self.leftFrame=tk.Frame(self.root,width=600,height=740,padx=3,pady=3)
        self.rightFrame=tk.Frame(self.root,width=740,height=740,padx=3,pady=3)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        

        self.leftFrame.grid(column=0,row=0,sticky="s")
        self.rightFrame.grid(column=1,row=0)


        self.lTopFrame=tk.Frame(self.leftFrame,image=None,width=100,height=50,padx=3,pady=10)       # for thumbnail
        self.lBtmFrame=tk.Frame(self.leftFrame,width=700,height=600,padx=3,pady=3)          # for details of target

        self.lTopFrame.grid(row=0,column=0)
        
        self.labelx = tk.Label(self.lTopFrame, image = None)                              # displaying thumbnail
 
        self.lBtmFrame.grid(row=1,column=0)

        ###################################### target details ##########################################

        self.label1=tk.Label(self.lBtmFrame,text="Type")
        self.label2=tk.Label(self.lBtmFrame,text="Latitude")
        self.label3=tk.Label(self.lBtmFrame,text="Longitude")
        self.label4=tk.Label(self.lBtmFrame,text="Orientation")
        self.label5=tk.Label(self.lBtmFrame,text="Shape")
        self.label6=tk.Label(self.lBtmFrame,text="Background Colour")
        self.label7=tk.Label(self.lBtmFrame,text="Alphanumeric Character")
        self.label8=tk.Label(self.lBtmFrame,text="Alphanumeric Colour")
        self.label9=tk.Label(self.lBtmFrame,text="Description")



        self.text1=tk.StringVar(self.lBtmFrame)
        self.text1.set("type")

        self.option1=tk.OptionMenu(self.lBtmFrame,self.text1,"standard","emergent","off_axis")
        self.option1.config(width=25)

        # self.entry1=tk.Entry(self.lBtmFrame)
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
 
        # self.entry4=tk.Entry(self.lBtmFrame)
        # self.entry5=tk.Entry(self.lBtmFrame)
        # self.entry6=tk.Entry(self.lBtmFrame)
        self.entry7=tk.Entry(self.lBtmFrame)

        self.text8=tk.StringVar(self.lBtmFrame)
        self.text8.set("Alphanumeric Colour")

        self.option8=tk.OptionMenu(self.lBtmFrame,self.text8,"white","black","gray","red","blue","green","yellow","purple","brown","orange")
        self.option8.config(width=25)
        # self.entry8=tk.Entry(self.lBtmFrame)
        self.entry9=tk.Entry(self.lBtmFrame)

        #################### positioning of labels ###################################

        self.label1.grid(row=0,padx=10,pady=15)
        self.label1.config(width=25)
        self.label1.config(font=("Courier",13))
    
        self.label2.grid(row=1,padx=10,pady=15)
        self.label2.config(width=25)
        self.label2.config(font=("Courier",13))
    
        self.label3.grid(row=2,padx=10,pady=15)
        self.label3.config(width=25)
        self.label3.config(font=("Courier",13))
    
        self.label4.grid(row=3,padx=10,pady=15)
        self.label4.config(width=25)
        self.label4.config(font=("Courier",13))
    
        self.label5.grid(row=4,padx=10,pady=15)
        self.label5.config(width=25)
        self.label5.config(font=("Courier",13))
    
        self.label6.grid(row=5,padx=10,pady=15)
        self.label6.config(width=25)
        self.label6.config(font=("Courier",13))
    
        self.label7.grid(row=6,padx=10,pady=15)
        self.label7.config(width=25)
        self.label7.config(font=("Courier",13))
    
        self.label8.grid(row=7,padx=10,pady=15)
        self.label8.config(width=25)
        self.label8.config(font=("Courier",13))
    
        self.label9.grid(row=8,padx=10,pady=15)
        self.label9.config(width=25)
        self.label9.config(font=("Courier",13))



        self.option1.grid(row=0,column=1,padx=10,pady=15,sticky="ew")
        self.option1.config(width=25)
        self.option1.config(font=("Courier",13))
        self.entry2.grid(row=1,column=1,padx=10,pady=15)
        self.entry2.config(width=25)
        self.entry2.config(font=("Courier",13))
        self.entry3.grid(row=2,column=1,padx=10,pady=15)
        self.entry3.config(width=25)
        self.entry3.config(font=("Courier",13))
        self.option4.grid(row=3,column=1,padx=10,pady=15)
        self.option4.config(width=25)
        self.option4.config(font=("Courier",13))     
        self.option5.grid(row=4,column=1,padx=10,pady=15)
        self.option5.config(width=25)
        self.option5.config(font=("Courier",13))
        self.option6.grid(row=5,column=1,padx=10,pady=15)
        self.option6.config(width=25)
        self.option6.config(font=("Courier",13))
        self.entry7.grid(row=6,column=1,padx=10,pady=15)
        self.entry7.config(width=25)
        self.entry7.config(font=("Courier",13))
        self.option8.grid(row=7,column=1,padx=10,pady=15)
        self.option8.config(width=25)
        self.option8.config(font=("Courier",13))
        self.entry9.grid(row=8,column=1,padx=10,pady=15)
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
        # self._fullscreen=true

        self.prevButton=tk.Button(self.midRF,text="Previous",command=self.show_previous_image)
        self.nextButton=tk.Button(self.midRF,text="Next",command=self.show_next_image)
        self.cropButton=tk.Button(self.midRF,text="Crop",command=self.crop_image)

        self.prevButton.grid(row=0,column=0)
        self.prevButton.config(width=27,height=3)
        self.nextButton.grid(row=0,column=1)
        self.nextButton.config(width=27,height=3)
        self.cropButton.grid(row=0,column=2)
        self.cropButton.config(width=28,height=3)

        # self.thumbnail=tk.Frame(self.bottomRF,bg="magenta",width=470,height=110)
        self.uploadButton=tk.Button(self.bottomRF,text="Upload to Interop",bg="black",fg="white",command=self.upload2Interop)

        # self.thumbnail.grid(row=0,column=0)
        self.uploadButton.grid(row=0,column=1,padx=3,pady=3)
        self.uploadButton.config(width=28,height=2)
        self.uploadButton.config(font=("Courier",30))

        # self.root.bind("<Return>", self.return_handler)
        # self.root.bind("<space>", self.space_handler)
        self.root.bind("<Escape>", self.esc_handler)
        self.root.bind("<Left>", self.show_previous_image)
        self.root.bind("<Right>", self.show_next_image)
        # self.root.bind("q", self.esc_handler)
        # self.root.bind("f", self.f_handler)
        # self.root.after(100, self.show_next_image)

       
        # self.set_timer()
        self.root.mainloop()
   
    # slide_show_time = 1
    # last_view_time = 0
    # paused = False
    image = None

    # def f_handler(self, e):
    #     self._fullscreen = not self._fullscreen
    #     if self._fullscreen:
    #         self.root.attributes('-fullscreen', True)
    #     else:
    #         self.root.attributes('-fullscreen', False)
    #         self.root.attributes("-zoomed", True)

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
        # self.v.set(fname)
        
        global splPath
        splPath=fname   

        x=self.gps()
        print ("Latitude and Longitude : ",x[0],x[1])
        self.entry2.delete(0,END)
        self.entry3.delete(0,END)
        self.entry2.insert(END,str(x[0]))
        self.entry3.insert(END,str(x[1]))
        # print (splPath)
        # print (mypath.splPath[46:])


    def show_previous_image(self, e=None):
        self._images = images()
        fname = self.previous_image()
        if not fname:
            return
        self.show_image(fname,self.label)
        # self.v.set(fname)
        
        global splPath
        splPath=fname

        x=self.gps()
        print ("Latitude and Longitude : ",x[0],x[1])
        self.entry2.delete(0,END)
        self.entry3.delete(0,END)
        self.entry2.insert(END,str(x[0]))
        self.entry3.insert(END,str(x[1]))

    # def sendSSH(self):
        # os.system("scp splPath iiitd@192.168.32.86:/home/iiitd/Desktop/target_images")
        # global splPath
        # cmd="scp "+splPath+" iiitd@192.168.32.86:/home/iiitd/Desktop/target_images" 
        # os.system(cmd)

    


    def show_image(self, fname,label):
        self.original_image = Image.open(fname)
        self.image = None
        self.fit_to_box(label)
        self.last_view_time = time.time()

    def crop_image(self):
        
        global splPath
        
        input_loc = splPath
        output_loc = splPath
        screen, px = self.setup(input_loc)
        left, upper, right, lower = self.mainLoop(screen, px)

        # ensure output rect always has positive width, height
        if right < left:
            left, right = right, left
        if lower < upper:
            lower, upper = upper, lower
        im = Image.open(input_loc)
        im = im.resize((1280,720), Image.ANTIALIAS)
        im = im.crop(( left, upper, right, lower))
        pygame.display.quit()

        im.save("cropped_"+output_loc)
        img = Image.open("cropped_"+output_loc) # image extension *.png,*.jpg
        new_width  = 100
        new_height = 100
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("cropped_"+output_loc)

        global mypath
        mypath="cropped_"+output_loc
        Im=ImageTk.PhotoImage(Image.open(mypath)) 
        self.labelx=tk.Label(self.lTopFrame,image=Im)

        a="cropped_"+output_loc
        x="cp "+a+" mydata/"+str(self.index1)+".jpg"
        os.system(x)
        xx="cp "+a+" "+str(self.index1)+".jpg"
        os.system(xx)
        self.index1+=1
        self._images = images()
        self.show_image("cropped_"+output_loc,self.labelx)

    def gps(self):
        # x=[]
        # global splPath
        # metadata=pyexiv2.ImageMetadata(splPath)
        # metadata.read()
        # print(metadata.exif_keys)
        # try:
        #     lat=metadata['Exif.GPSInfo.GPSLatitude']
        # except KeyError:
        #     lat=geo()
        #     lat.value='None'
        # x.append(lat.value)
        # try:
        #     lon=metadata['Exif.GPSInfo.GPSLongitude']
        # except KeyError:
        #     lon=geo()
        #     lon.value='None'
        # x.append(lon.value)
        return [38.1416667,76.4277778]



    def check_image_size(self):
        if not self.image:
            return
        self.fit_to_box()

    def fit_to_box(self,label):
        if self.image:
            if self.image.size[0] == self.box_width: return
            if self.image.size[1] == self.box_height: return
        # width, height = self.original_image.size
        width, height = 600,300
        print (width,height)
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
        # l = px.get_rect()
        # x = []
        # x.append(l[2])
        # x.append(l[3])
        screen = pygame.display.set_mode([1280,720])
        screen.blit(px, px.get_rect())
        pygame.display.flip()
        return screen, px


    def upload2Interop(self):
        s1=s2=s3=s4=s5=s6=s7=s8=s9=None
        s1=self.text1.get()
        s2=self.entry2.get()
        s3=self.entry3.get()
        s4=self.text4.get()
        s5=self.text5.get()
        s6=self.text6.get()
        s7=self.entry7.get()
        s8=self.text8.get()
        s9=self.entry9.get()
        if s9=="":
            s9=None
    
        target_response=OrderedDict([("id", 1),("mission", 1,),("type", s1),("latitude", s2),("longitude", s3),("orientation", s4),("shape",s5),("background_color",s6),("alphanumeric", s7),("alphanumeric_color", s8),("description", s9),("autonomous", False)])

        # print target_response
        json_str=json.dumps(target_response)
        print (json_str)

        
        x=self.gps()
        print ("Latitude and Longitude : ")
        with open(str(self.index2)+".json",'w') as outfile:
            json.dump(target_response,outfile)
        a=str(self.index2)+".json"
        b="cp "+a+" mydata/"+a 
        os.system(b)
       

        myclient = client.Client(url='http://localhost:8000',
                        username='testuser',
                        password='testpass')

        """target=interop.Odlc(id=None,
                                        user='indraprastha',
                                        type=s1,
                                        latitude=s2,
                                        longitude=s3,
                                        orientation=s4,
                                        shape=s5,
                                        background_color=s6,
                                        alphanumeric=s7,
                                        alphanumeric_color=s8,
                                        description=None, 
                                        autonomous=False)
                                target = client.post_odlc(target)"""


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

        print (str(self.index2)+".jpg")

        with open(str(self.index2)+".jpg", 'rb') as f:
            image_data = f.read()
            myclient.put_odlc_image(odlc.id, image_data)
        self.index2+=1



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

def test_scaled_size():
    x = scaled_size(width=1871, height=1223, box_width=1920, box_height=1080)
    assert x == (1652, 1080)
    x = scaled_size(width=100, height=100, blox_width=1920, box_height=1080)
    assert x ==(1080, 1080)






if __name__ == '__main__': 
    app=App()