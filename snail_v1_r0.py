# snail_v1_r0.py
# 
# Sea shell algorithms in 1+1 dimensions 
# 
# This program is based on the book 
# "The Algorithmic Beauty of Sea Shells" by Hans Meinhardt, ©1995 Springer-Verlag Berlin Heidelberg New York 
# and was created with the help of the program 
# ising.py by Dan Schroeder, Weber State University, January 2013
#
# Autor: Korbinian Schreiber, University of Munich, June 2013
 

import Tkinter, numpy, random, math


# /////// WINDOW SETTINGS AND ELEMENTARY GRAPHIC FUNCTIONS ///////

size = 100 #number of cells 
duration = 120 #number of time steps 
cell_width = 5 
cell_duration = 5  
canvas_width = size * cell_width #full width of the canvas in pixels 
canvas_height = duration * cell_duration 

# Window 
snail_window = Tkinter.Tk() #create GUI
snail_window.title("snail_v1_r0.py") 
snail_window.geometry('+50+50') #get the window away from the corner 

# Canvas 
snail_canvas = Tkinter.Canvas(snail_window, width = canvas_width, height = canvas_height)
snail_canvas.pack() #put it at the top of the window
snail_image = Tkinter.PhotoImage(width = canvas_width, height = canvas_height) 
snail_canvas.create_image((3, 3), image = snail_image, anchor="nw", state="normal") 
#the coordinates (3, 3) are a kludge to eliminate a mysterious offset that occurs otherwise.

# Set cell color in grey scales [0,1] 
def setCell(i,t,value):
	color = int(round(value * 255)) 
	r,g,b = color,color,color
	snail_image.put("#%02x%02x%02x" %(r,g,b), to=(i*cell_width, t*cell_duration, (i+1)*cell_width, (t+1)*cell_duration))



# /////// COMPUTATION AND SETTINGS OF THE SIMULATION /////// 

# Arrays of activator, inhibitor, interactor,...
a = numpy.ones((size,duration), float)
b = numpy.ones((size,duration), float)
#c = numpy.ones((size,duration), float) 

# Diffusion 
Da = 0.2 #Dx > 0.4 leads to numerical instability (meinhardt) 
Db = 0.35 
#Dc = 

# Decay 
Ra = 0.1
Rb = 0.1
#Rc = 

# Steady state production 
Ba = 0.2 
Bb = 0.2 
#Bc = 

# Saturation, interactions, Michaelis-Menten constant  
Sa = 0.9
Sb = 0.9
#Sc = 

# Coupling ('s' in the book) 
Ca = 0.5 

# Cell specific initial concentrations (arrays) 
#Aa = 
#AB = 
#Ac = 

# General initial concentrations 
Ga = 0.2
Gb = 0.2 
#Gc = 



# calculation of activator
def getActivator():
	

# Dummy main() 
def dummyMain(): 
	setCell(int(random.random()*size),int(random.random()*duration),random.random()) 
	snail_window.after(1,dummyMain) 

dummyMain()
snail_window.mainloop()





