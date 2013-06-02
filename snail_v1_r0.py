# snail_v1_r0.py
# 
# Sea shell algorithms in 1+1 dimensions 
# 
# This program is based on the book 
# "The Algorithmic Beauty of Sea Shells" by Hans Meinhardt, 1995 Springer-Verlag Berlin Heidelberg New York 
# and was created with the help of the program 
# ising.py by Dan Schroeder, Weber State University, January 2013
#
# Autor: Korbinian Schreiber, University of Munich, June 2013
 

import Tkinter, numpy, random, math


# /////// WINDOW SETTINGS AND ELEMENTARY GRAPHIC FUNCTIONS ///////

size = 100 #number of cells 
duration = 80 #number of time steps 
cell_width = 3 
cell_duration = 3  
canvas_width = size * cell_width #full width of the canvas in pixels 
canvas_height = duration * cell_duration 

# Window 
snail_window = Tkinter.Tk() #create GUI
snail_window.title("snail_v1_r0.py") 
snail_window.geometry('+600+50') #get the window away from the corner
snail_window.configure(background='white') 

# Canvas 
snail_canvas = Tkinter.Canvas(snail_window, width = canvas_width, height = canvas_height)
snail_canvas.pack() #put it at the top of the window
snail_image = Tkinter.PhotoImage(width = canvas_width, height = canvas_height)
snail_canvas.config(background='black') 
snail_canvas.create_image((1, 1), image = snail_image, anchor="nw", state="normal") 
#the coordinates (3, 3) are a kludge to eliminate a mysterious offset that occurs otherwise.

# Set cell color in grey scales [0,1] 
def setCell(i,t,value):
	color = 255 - int(round(value * 255)) 
	r,g,b = color,color,color
	snail_image.put("#%02x%02x%02x" %(r,g,b), to=(i*cell_width, t*cell_duration, (i+1)*cell_width, (t+1)*cell_duration))

# Set two cell colors in [0,1] 
def setCellColors(i, t, red, green): 
	red = 255 - int(round(red * 255)) 
	green = 255 - int(round(green * 255)) 
	r,g,b = red,green,green
	snail_image.put("#%02x%02x%02x" %(r,g,b), to=(i*cell_width, t*cell_duration, (i+1)*cell_width, (t+1)*cell_duration))

# Set cell color as difference between two values [0,1] 
def setCellDiff(i, t, subs1, subs2): 
	diff = subs1 - subs2 if subs1 > subs2 else 0 
	color = 255 - int(round(diff * 255)) 
	r,g,b = color,color,color
	snail_image.put("#%02x%02x%02x" %(r,g,b), to=(i*cell_width, t*cell_duration, (i+1)*cell_width, (t+1)*cell_duration))


# /////// PARAMETERS AND SETTINGS OF THE SIMULATION /////// 

# Arrays of activator, inhibitor, interactor,...
a = numpy.ones((size,duration), float)
b = numpy.ones((size,duration), float)
#c = numpy.ones((size,duration), float) 

# Diffusion 
Da = 0.005 #Dx > 0.4 leads to numerical instability (meinhardt) 
Db = 0.4 # 0.5 gave kind of chess pattern
#Dc = 

# Decay 
Ra = 0.1
Rb = 0.1
#Rc = 

# Steady state production 
Ba = 0.4
Bb = 0.1 # is x-dependent in some cases (chapter 4) 
#Bc = 

# Saturation, interactions, Michaelis-Menten constant  
Sa = 0.3
Sb = 0.9
#Sc = 

# Coupling or source density ('s' in the book) 
Ca = 0.08 # 0.055 was interesting

# Cell specific initial concentrations (arrays) 
#Aa = 
#AB = 
#Ac = 

# General initial concentrations 
Ga = 0.5 # TODO: 	For x-dependent concentrations they should become arrays, 
Gb = 0.5 # 		which would also affect initSubstance( , ).  
#Gc = 

# Initial Noise parameter 
InitialNoise = 0.2


# /////// USER INTERFACE ///////

# /////// FUNCTIONS AND METHODS OF THE SIMULATION ///////

# Init arrays 
def initSubstance(substance, concentration):
	for i in range(size):
		substance[i, 0] = concentration + InitialNoise - (InitialNoise * random.random())/2 # add fluctuations around concentration 

# Diffusion  
def diffusion(substance, i, t):
	# periodic constraints:
	low = size - 1 if i == 0 else i - 1
	high = 0 if i == size - 1 else i + 1
	# open ends:
#	low = i if i == 0 else i - 1
#	high = i if i == size - 1 else i + 1

	return (substance[low, t] - 2*substance[i, t] + substance[high, t]) 

# NOTE:	My first approach is to write down each of the different functions for varios problems explicitly. 
# 	Modular design would be great but I think it's better to first make sure, what's important and then see. 

# ******* Activator inhibitor mechanism (2.1)  
def daActivInhib(i, t):	
	return (Ca * ((a[i, t] * a[i, t] / b[i, t]) + Ba) - Ra*a[i, t] + Da*diffusion(a, i, t)) 

def dbActivInhib(i, t): 
	return (Ca * a[i, t] * a[i, t]  - Ra*b[i, t] + Bb + Db*diffusion(b, i, t))

# ******* Activator substrate reaction (2.4) 
def daActivSubs(i, t): 
	A , B = a[i, t], b[i, t] 
	return (Ca*B*((A*A / (1 + Sa*A*A)) + Ba) -Ra*A + Da*diffusion(a, i, t)) 
def dbActivSubs(i, t):
	A , B = a[i, t], b[i, t]
	return (Bb* - Ca*B*((A*A / (1 + Sa*A*A)) + Ba) - Rb + Db*diffusion(b, i, t))  


# /////// MAIN FUNCTION AND LOOP ///////

# Dummy functions
def dummyMain(): 
	setCell(int(random.random()*size),int(random.random()*duration),random.random())
	snail_window.after(1,dummyMain) 

def dummySnail(): 
	initSubstance(a, Ga) 
	initSubstance(b, Gb)
	for t in range(duration-1): 
		for i in range(size):
			a[i, t+1] = a[i, t] + daActivSubs(i, t) 
			if a[i, t+1] >= 1: 
				a[i, t+1] = 1
			if a[i, t+1] < 0: 
				a[i, t+1] = 0 
			b[i, t+1] = b[i, t] + dbActivSubs(i, t)
			if b[i, t+1] >= 1:
				b[i, t+1] = 1
			if b[i, t+1] < 0:
				b[i, t+1] = 0
#			setCellColors(i, t+1, a[i, t+1], b[i, t+1]) 
#			setCellDiff(i, t+1, a[i, t+1], b[i, t+1])
			setCell(i, t+1, a[i, t+1]) 
		print duration - t 	

#dummyMain()
dummySnail() 
snail_window.mainloop()





