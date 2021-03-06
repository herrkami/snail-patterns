# snail_v1_r0.py
# 
# Sea shell algorithms in 1+1 dimensions 
# 
# This program is based on the book 
# "The Algorithmic Beauty of Sea Shells" by Hans Meinhardt, 1995 Springer-Verlag Berlin Heidelberg New York 
# and has been created with the help of the program 
# ising.py by Dan Schroeder, Weber State University, January 2013
#
# Autor: Korbinian Schreiber, University of Munich, June 2013
 

import Tkinter, numpy, random, math


# /////// WINDOW SETTINGS AND ELEMENTARY GRAPHIC FUNCTIONS ///////

size = 400#number of cells 
duration = 300 #number of time steps 
cell_width = 1
cell_duration = 1  
canvas_width = size * cell_width #full width of the canvas in pixels 
canvas_height = duration * cell_duration 

# Window 
snail_window = Tkinter.Tk() #create GUI
snail_window.title("snail_v1_r0.py") 
snail_window.geometry('+10+20') #get the window away from the corner
# snail_window.configure(background='white') 

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
def setCellColors(i, t, a, b): 
	print a
	a = 255 - int(round(a * 255)) 
	b = 255 - int(round(b * 255)) 
	r,g,b = b,a,a
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
c = numpy.ones((size,duration), float) 

# Init Parameters 
def initParameters(): 
	DaSlider.set(0.279) # Diffusion 
	DbSlider.set(0.588)
	DcSlider.set(0.485) # phase transition at 510
        RaSlider.set(0.618) # Decay 
        RbSlider.set(0.353)
	RcSlider.set(0.544)
        BaSlider.set(0.044) # Steady state production 
        BbSlider.set(0.044)
        SaSlider.set(0.2) # Saturation 
        SbSlider.set(0.9)
        CaSlider.set(0.412) # Coupling 
        GaSlider.set(0.250) # Initial concentration 
        GbSlider.set(0.5)
	GcSlider.set(0.5)
	PaSlider.set(0) # Initial concentration 
        PbSlider.set(0)
	PcSlider.set(0)
	AaSlider.set(0.000) # Initial concentration 
        AbSlider.set(0.000)
	AcSlider.set(0.000)
        InitialNoiseSlider.set(0.2) # Initial noise 

# Read sliders 
def readSliders(): 
	global Da, Db, Dc, Ra, Rb, Rc, Ba, Bb, Sa, Sb, Ca, Ga, Gb, Gc, Pa, Pb, Pc, Aa, Ab, Ac, InitialNoise 
	Da = DaSlider.get() # Diffusion 
	Db = DbSlider.get()
	Dc = DcSlider.get()
	Ra = RaSlider.get() # Decay 
	Rb = RbSlider.get()
	Rc = RcSlider.get()
	Ba = BaSlider.get() # Steady state production 
	Bb = BbSlider.get()
	Sa = SaSlider.get() # Saturation 
	Sb = SbSlider.get()
	Ca = CaSlider.get() # Coupling 
	Ga = GaSlider.get() # Initial concentration 
	Gb = GbSlider.get()
	Gc = GcSlider.get()
	Pa = PaSlider.get() # Initial period 
	Pb = PbSlider.get()
	Pc = PcSlider.get()
	Aa = AaSlider.get() # Initial period 
	Ab = AbSlider.get()
	Ac = AcSlider.get()
	InitialNoise = InitialNoiseSlider.get() # Initial noise  

Da, Db, Dc, Ra, Rb, Rc, Ba, Bb, Sa, Sb, Ca, Ga, Gb, Gc, Aa, Ab, Ac, InitialNoise = .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5
Pa, Pb, Pc = 1, 1, 1

# Set Parameters 
def loadParameters(): 
	enableAllSliders()
	mode = sim_parameters.get() 
	if mode == "3:caves":
		Da = 0.044
		Db = 0.838
		Dc = 0.515
		Ra = 0.618
		Rb = 0.353
		Rc = 0.529
		Ba = 0.044
		Bb = 0.000
		Sa = 0.000
		Sb = 0.000
		Ca = 0.412
		Ga = 0.250
		Gb = 0.500
		Gc = 0.500
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.200
	elif mode == "3:chaos1": 
		Da = 0.279
		Db = 0.588
		Dc = 0.485
		Ra = 0.618
		Rb = 0.353
		Rc = 0.544
		Ba = 0.044
		Bb = 0.000
		Sa = 0.000
		Sb = 0.000
		Ca = 0.412
		Ga = 0.250
		Gb = 0.500
		Gc = 0.500
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.200
	elif mode == "1:thin_lines": 
		Da = 0.088
		Db = 0.324
		Dc = 0.000
		Ra = 0.809
		Rb = 0.809
		Rc = 0.000
		Ba = 0.088
		Bb = 0.206
		Sa = 0.000
		Sb = 0.000
		Ca = 0.368
		Ga = 0.588
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.200
	elif mode == "1:waves_stripes": 
		Da = 0.103
		Db = 0.353
		Dc = 0.000
		Ra = 0.691
		Rb = 0.691
		Rc = 0.000
		Ba = 0.147
		Bb = 0.201
		Sa = 0.000
		Sb = 0.000
		Ca = 0.353
		Ga = 0.441
		Gb = 0.368
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.324
	elif mode == "1:dark_tri_waves":
		Da = 0.059
		Db = 0.279
		Dc = 0.000
		Ra = 0.529
		Rb = 0.529
		Rc = 0.000
		Ba = 0.074
		Bb = 0.110
		Sa = 0.000
		Sb = 0.000
		Ca = 0.496
		Ga = 0.647
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.426
	elif mode == "1:triangles1":
		Da = 0.056
		Db = 0.500
		Dc = 0.000
		Ra = 0.706
		Rb = 0.706
		Rc = 0.000
		Ba = 0.044
		Bb = 0.500
		Sa = 0.000
		Sb = 0.000
		Ca = 0.706
		Ga = 0.191
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.200
	elif mode == "1:stripes1":
		Da = 0.035
		Db = 0.353
		Dc = 0.000
		Ra = 0.368
		Rb = 0.368
		Rc = 0.000
		Ba = 0.022
		Bb = 0.633
		Sa = 0.000
		Sb = 0.000
		Ca = 0.430
		Ga = 0.640
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.074
	elif mode == "1:cepaea_nemoralis":
		Da = 0.118
		Db = 0.559
		Dc = 0.000
		Ra = 0.471
		Rb = 0.471
		Rc = 0.000
		Ba = 0.147
		Bb = 0.441
		Sa = 0.000
		Sb = 0.000
		Ca = 0.500
		Ga = 0.500
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.044
	elif mode == "1:waves1":
		Da = 0.029
		Db = 0.559
		Dc = 0.000
		Ra = 0.412
		Rb = 0.471
		Rc = 0.000
		Ba = 0.426
		Bb = 0.441
		Sa = 0.000
		Sb = 0.000
		Ca = 0.206
		Ga = 0.500
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.001
	elif mode == "1:conus_ebraeus":
		Da = 0.029
		Db = 0.544
		Dc = 0.000
		Ra = 0.412
		Rb = 0.471
		Rc = 0.000
		Ba = 0.456
		Bb = 0.412
		Sa = 0.000
		Sb = 0.000
		Ca = 0.206
		Ga = 0.500
		Gb = 0.500
		Gc = 0.000
		Pa = 30
		Pb = 30
		Pc = 0
		Aa = 0.162
		Ab = 0.147
		Ac = 0.000
		InitialNoise = 0.004
	elif mode == "1:bloody_tears":
		Da = 0.094
		Db = 0.809
		Dc = 0.000
		Ra = 0.676
		Rb = 0.676
		Rc = 0.000
		Ba = 0.118
		Bb = 0.647
		Sa = 0.000
		Sb = 0.000
		Ca = 0.657
		Ga = 0.646
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.044
	elif mode == "1:hearts":
		Da = 0.397
		Db = 0.824
		Dc = 0.000
		Ra = 0.676
		Rb = 0.676
		Rc = 0.000
		Ba = 0.118
		Bb = 0.615
		Sa = 0.000
		Sb = 0.000
		Ca = 0.657
		Ga = 0.646
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.044
	elif mode == "2:diagonals":
		Da = 0.010
		Db = 0.412
		Dc = 0.000
		Ra = 0.335
		Rb = 0.547
		Rc = 0.000
		Ba = 0.074
		Bb = 0.618
		Sa = 0.574
		Sb = 0.000
		Ca = 0.897
		Ga = 0.647
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.426
	elif mode == "2:amoria_ellioti":
		Da = 0.809
		Db = 0.309
		Dc = 0.000
		Ra = 0.250
		Rb = 0.265
		Rc = 0.000
		Ba = 0.441
		Bb = 0.588
		Sa = 0.647
		Sb = 0.000
		Ca = 0.897
		Ga = 0.284
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.132
	elif mode == "2:waves1":
		Da = 0.397
		Db = 0.397
		Dc = 0.000
		Ra = 0.426
		Rb = 0.000
		Rc = 0.000
		Ba = 0.088
		Bb = 0.265
		Sa = 0.000
		Sb = 0.000
		Ca = 0.824
		Ga = 0.176
		Gb = 0.500
		Gc = 0.191
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.132
	elif mode == "2:conus_abbas":
		Da = 0.662
		Db = 0.505
		Dc = 0.000
		Ra = 0.191
		Rb = 0.265
		Rc = 0.000
		Ba = 0.441
		Bb = 0.706
		Sa = 1.000
		Sb = 0.000
		Ca = 0.897
		Ga = 0.000
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.001
	elif mode == "2:oliva_porphyria":
		Da = 0.809
		Db = 0.400
		Dc = 0.000
		Ra = 0.250
		Rb = 0.265
		Rc = 0.000
		Ba = 0.382
		Bb = 0.814
		Sa = 0.971
		Sb = 0.000
		Ca = 0.897
		Ga = 0.294
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.132
	elif mode == "2:ghosts":
		Da = 0.824
		Db = 0.162
		Dc = 0.000
		Ra = 0.529
		Rb = 0.897
		Rc = 0.000
		Ba = 0.632
		Bb = 0.647
		Sa = 0.147
		Sb = 0.000
		Ca = 0.824
		Ga = 0.294
		Gb = 0.154
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.206
	elif mode == "2:dif_angle_lines":
		Da = 0.809
		Db = 0.368
		Dc = 0.000
		Ra = 0.250
		Rb = 0.338
		Rc = 0.000
		Ba = 0.382
		Bb = 0.382
		Sa = 0.971
		Sb = 0.000
		Ca = 0.897
		Ga = 1.000
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.235
	elif mode == "3:stripes_n_waves":
		Da = 0.004
		Db = 0.265
		Dc = 0.485
		Ra = 0.926
		Rb = 0.044
		Rc = 0.206
		Ba = 0.022
		Bb = 0.794
		Sa = 0.000
		Sb = 0.000
		Ca = 0.662
		Ga = 0.640
		Gb = 0.500
		Gc = 0.000
		Pa = 0
		Pb = 0
		Pc = 0
		Aa = 0.000
		Ab = 0.000
		Ac = 0.000
		InitialNoise = 0.074
		
	DaSlider.set(Da) # Diffusion 
	DbSlider.set(Db)
	DcSlider.set(Dc) # phase transition at 510
        RaSlider.set(Ra) # Decay 
        RbSlider.set(Rb)
	RcSlider.set(Rc)
        BaSlider.set(Ba) # Steady state production 
        BbSlider.set(Bb)
        SaSlider.set(Sa) # Saturation 
        SbSlider.set(Sb)
        CaSlider.set(Ca) # Coupling 
        GaSlider.set(Ga) # Initial concentration 
        GbSlider.set(Gb)
	GcSlider.set(Gc)
	PaSlider.set(Pa) # Initial concentration 
        PbSlider.set(Pb)
	PcSlider.set(Pc)
	AaSlider.set(Aa) # Initial concentration 
        AbSlider.set(Ab)
	AcSlider.set(Ac)
	InitialNoiseSlider.set(InitialNoise) # Initial noise 
	activateSliders()

# Enable all Sliders
def enableAllSliders():
	on = 'active'
	DaSlider['state'] = on
	DbSlider['state'] = on
	DcSlider['state'] = on
	RaSlider['state'] = on
	RbSlider['state'] = on
	RcSlider['state'] = on
	BaSlider['state'] = on
	BbSlider['state'] = on
	SaSlider['state'] = on
	SbSlider['state'] = on
	CaSlider['state'] = on
	GaSlider['state'] = on
	GbSlider['state'] = on
	GcSlider['state'] = on
	InitialNoiseSlider['state'] = on

# Activate Sliders 
def activateSliders():
	on = 'active'
	off = 'disabled'
	sliders = mechanism.get()
	
	print sliders
	
	if sliders == "1:act-in":
		DaSlider['state'] = on
		DaSlider['fg'] = 'black'
		DbSlider['state'] = on
		DbSlider['fg'] = 'black'
		DcSlider['state'] = off
		DcSlider['fg'] = 'grey'
		RaSlider['state'] = on
		RaSlider['fg'] = 'black'
		RbSlider['state'] = on
		RbSlider['fg'] = 'black'
		RcSlider['state'] = off
		RcSlider['fg'] = 'grey'
		BaSlider['state'] = on
		BaSlider['fg'] = 'black'
		BbSlider['state'] = on
		BbSlider['fg'] = 'black'
		SaSlider['state'] = off
		SaSlider['fg'] = 'grey'
		SbSlider['state'] = off
		SbSlider['fg'] = 'grey'
		CaSlider['state'] = on
		CaSlider['fg'] = 'black'
		GaSlider['state'] = on
		GaSlider['fg'] = 'black'
		GbSlider['state'] = on
		GbSlider['fg'] = 'black'
		GcSlider['state'] = off
		GcSlider['fg'] = 'grey'
		PaSlider['state'] = on
		PaSlider['fg'] = 'black'
		PbSlider['state'] = on
		PbSlider['fg'] = 'black'
		PcSlider['state'] = off
		PcSlider['fg'] = 'grey'
		AaSlider['state'] = on
		AaSlider['fg'] = 'black'
		AbSlider['state'] = on
		AbSlider['fg'] = 'black'
		AcSlider['state'] = off
		AcSlider['fg'] = 'grey'
		InitialNoiseSlider['state'] = on
		InitialNoiseSlider['fg'] = 'black'
	elif sliders == "2:act-sub":
		DaSlider['state'] = on
		DaSlider['fg'] = 'black'
		DbSlider['state'] = on
		DbSlider['fg'] = 'black'
		DcSlider['state'] = off
		DcSlider['fg'] = 'grey'
		RaSlider['state'] = on
		RaSlider['fg'] = 'black'
		RbSlider['state'] = on
		RbSlider['fg'] = 'black'
		RcSlider['state'] = off
		RcSlider['fg'] = 'grey'
		BaSlider['state'] = on
		BaSlider['fg'] = 'black'
		BbSlider['state'] = on
		BbSlider['fg'] = 'black'
		SaSlider['state'] = on
		SaSlider['fg'] = 'black'
		SbSlider['state'] = off
		SbSlider['fg'] = 'grey'
		CaSlider['state'] = on
		CaSlider['fg'] = 'black'
		GaSlider['state'] = on
		GaSlider['fg'] = 'black'
		GbSlider['state'] = on
		GbSlider['fg'] = 'black'
		GcSlider['state'] = off
		GcSlider['fg'] = 'grey'
		PaSlider['state'] = on
		PaSlider['fg'] = 'black'
		PbSlider['state'] = on
		PbSlider['fg'] = 'black'
		PcSlider['state'] = off
		PcSlider['fg'] = 'grey'
		AaSlider['state'] = on
		AaSlider['fg'] = 'black'
		AbSlider['state'] = on
		AbSlider['fg'] = 'black'
		AcSlider['state'] = off
		AcSlider['fg'] = 'grey'
		InitialNoiseSlider['state'] = on
		InitialNoiseSlider['fg'] = 'black'
	elif sliders == "3:ext act-in":
		DaSlider['state'] = on
		DaSlider['fg'] = 'black'
		DbSlider['state'] = on
		DbSlider['fg'] = 'black'
		DcSlider['state'] = on
		DcSlider['fg'] = 'black'
		RaSlider['state'] = on
		RaSlider['fg'] = 'black'
		RbSlider['state'] = on
		RbSlider['fg'] = 'black'
		RcSlider['state'] = on
		RcSlider['fg'] = 'black'
		BaSlider['state'] = on
		BaSlider['fg'] = 'black'
		BbSlider['state'] = on
		BbSlider['fg'] = 'black'
		SaSlider['state'] = off
		SaSlider['fg'] = 'grey'
		SbSlider['state'] = off
		SbSlider['fg'] = 'grey'
		CaSlider['state'] = on
		CaSlider['fg'] = 'black'
		GaSlider['state'] = on
		GaSlider['fg'] = 'black'
		GbSlider['state'] = on
		GbSlider['fg'] = 'black'
		GcSlider['state'] = on
		GcSlider['fg'] = 'black'
		PaSlider['state'] = on
		PaSlider['fg'] = 'black'
		PbSlider['state'] = on
		PbSlider['fg'] = 'black'
		PcSlider['state'] = on
		PcSlider['fg'] = 'black'
		AaSlider['state'] = on
		AaSlider['fg'] = 'black'
		AbSlider['state'] = on
		AbSlider['fg'] = 'black'
		AcSlider['state'] = on
		AcSlider['fg'] = 'black'
		InitialNoiseSlider['state'] = on
		InitialNoiseSlider['fg'] = 'black'
		

# /////// FUNCTIONS AND METHODS OF THE SIMULATION ///////

# Init arrays 
def initSubstance(substance, concentration):
	for i in range(size):
		substance[i, 0] = concentration + InitialNoise - (InitialNoise * random.random())/2 # add fluctuations around concentration 
# Init a periodic structure 
def initPeriodicSubstance(substance, concentration, period, amplitude): 
	if period == 0:
		period = size
	i,j = 0,0
	while(i<size):
		for j in range(period):
			if i< size:
				substance[i, 0] = concentration + (amplitude/2) + InitialNoise - (InitialNoise * random.random())/2
			i = i + 1
		for j in range(period):
			if i< size:
				substance[i, 0] = concentration - (amplitude/2) + InitialNoise - (InitialNoise * random.random())/2
			i = i + 1

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
	A, B = a[i, t], b[i, t]
	return (Ca * ((A*A / B) + Ba) - Ra*A + Da*diffusion(a, i, t)) 

def dbActivInhib(i, t): 
	A, B = a[i, t], b[i, t]
	return (Ca*A*A  - Rb*B + Bb + Db*diffusion(b, i, t))

# ******* Activator substrate reaction (2.4) 
def daActivSubs(i, t): 
	A, B = a[i, t], b[i, t] 
	return (Ca*B*((A*A / (1 + Sa*A*A)) + Ba) - Ra*A + Da*diffusion(a, i, t)) 
def dbActivSubs(i, t):
	A, B = a[i, t], b[i, t]
	return (Bb - Ca*B*((A*A / (1 + Sa*A*A)) + Ba) - Rb*B + Db*diffusion(b, i, t))  

# ******* Extended activator inhibitor mechanism (5.3)
def daExActivInhib(i, t): 
	A, B, C = a[i, t], b[i, t], c[i, t] 
	return((Ca/C) * (A*A/B + Ba) - Ra*A +Da*diffusion(a, i, t)) 
def dbExActivInhib(i, t):
	A, B, C = a[i, t], b[i, t], c[i, t] 
	return((Rb*A*A/C) - Rb*B + Bb + Db*diffusion(b, i, t)) 
def dcExActivInhib(i, t):
	A, B, C = a[i, t], b[i, t], c[i, t]
	return(Rc*(A - C) + Dc*diffusion(c, i, t)) 


# Dummy functions
def dummyMain(): 
	setCell(int(random.random()*size),int(random.random()*duration),random.random())
	snail_window.after(1,dummyMain) 


# /////// DUMMY FUNCTIONS ///////

def dummySnail(): 
	initSubstance(a, Ga) 
	initSubstance(b, Gb) 
	initSubstance(c, Gc) 
	readSliders()
	print_case = print_mode.get() 
	for t in range(duration-1): 
		for i in range(size):
			# calculate a 
#			a[i, t+1] = a[i, t] + daActivSubs(i, t) 
#			a[i, t+1] = a[i, t] + daActivInhib(i, t)
#			a[i, t+1] = a[i, t] + daActivSubs(i, t)
			a[i, t+1] = a[i, t] + daExActivInhib(i, t)
			if a[i, t+1] >= 1: 
				a[i, t+1] = 1
			if a[i, t+1] < 0: 
				a[i, t+1] = 0 
			# calculate b 
#			b[i, t+1] = b[i, t] + dbActivSubs(i, t)
#			b[i, t+1] = b[i, t] + dbActivInhib(i, t)
#			b[i, t+1] = b[i, t] + dbActivSubs(i, t)
			b[i, t+1] = b[i, t] + dbExActivInhib(i, t)
			if b[i, t+1] >= 1:
				b[i, t+1] = 1
			if b[i, t+1] < 0:
				b[i, t+1] = 0
			# calculate c 
			c[i, t+1] = c[i, t] + dcExActivInhib(i, t)
			if c[i, t+1] >= 1:
				c[i, t+1] = 1
			if c[i, t+1] < 0:
				c[i, t+1] = 0
			# print line 
			# maybe this can be done in a loop that runs after each line:
			if print_case == "color":
				setCellColors(i, t+1, a[i, t+1], b[i, t+1]) 
			elif print_case == "diff": 
				setCellDiff(i, t+1, a[i, t+1], b[i, t+1]) 
			elif print_case == "b/w": 
				setCell(i, t+1, a[i, t+1])
		snail_window.update() 	

def executeSim():
	activateSliders()
	readSliders() 
#	initSubstance(a, Ga)
#	initSubstance(b, Gb)
#	initSubstance(c, Gc)
	initPeriodicSubstance(a, Ga, Pa, Aa) 
	initPeriodicSubstance(b, Gb, Pb, Ab) 
	initPeriodicSubstance(c, Gc, Pc, Ac) 
	mech = mechanism.get()
	print_case = print_mode.get() 
	if mech == "1:act-in": 
		for t in range(duration-1): 
			for i in range(size):
				a[i, t+1] = a[i, t] + daActivInhib(i, t)
				if a[i, t+1] >= 1: 
					a[i, t+1] = 1
				if a[i, t+1] < 0: 
					a[i, t+1] = 0
				b[i, t+1] = b[i, t] + dbActivInhib(i, t)
				if b[i, t+1] >= 1:
					b[i, t+1] = 1
				if b[i, t+1] < 0:
					b[i, t+1] = 0
				if print_case == "color":
					setCellColors(i, t+1, a[i, t+1], b[i, t+1]) 
				elif print_case == "diff": 
					setCellDiff(i, t+1, a[i, t+1], b[i, t+1]) 
				elif print_case == "b/w": 
					setCell(i, t+1, a[i, t+1])
			snail_window.update()
	elif mech == "2:act-sub": 
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
				if print_case == "color":
					setCellColors(i, t+1, a[i, t+1], b[i, t+1]) 
				elif print_case == "diff": 
					setCellDiff(i, t+1, a[i, t+1], b[i, t+1]) 
				elif print_case == "b/w": 
					setCell(i, t+1, a[i, t+1])
			snail_window.update()
	elif mech == "3:ext act-in": 
		for t in range(duration-1): 
			for i in range(size):
				a[i, t+1] = a[i, t] + daExActivInhib(i, t)
				if a[i, t+1] >= 1: 
					a[i, t+1] = 1
				if a[i, t+1] < 0: 
					a[i, t+1] = 0
				b[i, t+1] = b[i, t] + dbExActivInhib(i, t)
				if b[i, t+1] >= 1:
					b[i, t+1] = 1
				if b[i, t+1] < 0:
					b[i, t+1] = 0
				c[i, t+1] = c[i, t] + dcExActivInhib(i, t)
				if c[i, t+1] >= 1:
					c[i, t+1] = 1
				if c[i, t+1] < 0:
					c[i, t+1] = 0
				if print_case == "color":
					setCellColors(i, t+1, a[i, t+1], b[i, t+1]) 
				elif print_case == "diff": 
					setCellDiff(i, t+1, a[i, t+1], b[i, t+1]) 
				elif print_case == "b/w": 
					setCell(i, t+1, a[i, t+1])
			snail_window.update()

# /////// USER INTERFACE ///////

# Diffusion 
diff_control = Tkinter.Frame(snail_window)
diff_control.pack() 
diff_label = Tkinter.Label(diff_control, text="Diffusion:   ")
diff_label.pack(side="left")
DaSlider = Tkinter.Scale(diff_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
DaSlider.pack(side="left")
DbSlider = Tkinter.Scale(diff_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
DbSlider.pack(side="left")
DcSlider = Tkinter.Scale(diff_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
DcSlider.pack(side="left")
# Decay 
decay_control = Tkinter.Frame(snail_window)
decay_control.pack()
decay_label = Tkinter.Label(decay_control, text="Decay:       ")
decay_label.pack(side="left")
RaSlider = Tkinter.Scale(decay_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
RaSlider.pack(side="left")
RbSlider = Tkinter.Scale(decay_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
RbSlider.pack(side="left")
RcSlider = Tkinter.Scale(decay_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
RcSlider.pack(side="left")
# Steady state production
steady_control = Tkinter.Frame(snail_window)
steady_control.pack() 
steady_label = Tkinter.Label(steady_control, text="Basal prod.: ")
steady_label.pack(side="left")
BaSlider = Tkinter.Scale(steady_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
BaSlider.pack(side="left")
BbSlider = Tkinter.Scale(steady_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
BbSlider.pack(side="left")
steady_spacer = Tkinter.Frame(steady_control, width=100)
steady_spacer.pack(side="left")
# Saturation 
sat_control = Tkinter.Frame(snail_window)
sat_control.pack()
sat_label = Tkinter.Label(sat_control, text="Saturation:  ")
sat_label.pack(side="left")
SaSlider = Tkinter.Scale(sat_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
SaSlider.pack(side="left")
SbSlider = Tkinter.Scale(sat_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
SbSlider.pack(side="left")
sat_spacer = Tkinter.Frame(sat_control, width=100)
sat_spacer.pack(side="left")
# Coupling
coupling_control = Tkinter.Frame(snail_window)
coupling_control.pack()
coupling_label = Tkinter.Label(coupling_control, text="Coupling:    ")
coupling_label.pack(side="left")
CaSlider = Tkinter.Scale(coupling_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
CaSlider.pack(side="left")
coupling_spacer = Tkinter.Frame(coupling_control, width=200) 
coupling_spacer.pack(side="left")
# Initial concentration 
concen_control = Tkinter.Frame(snail_window)
concen_control.pack()
concen_label = Tkinter.Label(concen_control, text="Init. conc.: ")
concen_label.pack(side="left")
GaSlider = Tkinter.Scale(concen_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
GaSlider.pack(side="left")
GbSlider = Tkinter.Scale(concen_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
GbSlider.pack(side="left")
GcSlider = Tkinter.Scale(concen_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
GcSlider.pack(side="left")
# Initial period 
period_control = Tkinter.Frame(snail_window)
period_control.pack()
period_label = Tkinter.Label(period_control, text="Init. period: ")
period_label.pack(side="left")
PaSlider = Tkinter.Scale(period_control, from_=0, to=size, resolution = 1, length=100, orient="horizontal")
PaSlider.pack(side="left")
PbSlider = Tkinter.Scale(period_control, from_=0, to=size, resolution = 1, length=100, orient="horizontal")
PbSlider.pack(side="left")
PcSlider = Tkinter.Scale(period_control, from_=0, to=size, resolution = 1, length=100, orient="horizontal")
PcSlider.pack(side="left")
# Initial amplitude 
amp_control = Tkinter.Frame(snail_window)
amp_control.pack()
amp_label = Tkinter.Label(amp_control, text="Init. amp.: ")
amp_label.pack(side="left")
AaSlider = Tkinter.Scale(amp_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
AaSlider.pack(side="left")
AbSlider = Tkinter.Scale(amp_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
AbSlider.pack(side="left")
AcSlider = Tkinter.Scale(amp_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
AcSlider.pack(side="left")
# Initial noise
noise_control = Tkinter.Frame(snail_window)
noise_control.pack()
noise_label = Tkinter.Label(noise_control, text="Init. noise: ")
noise_label.pack(side="left")
InitialNoiseSlider = Tkinter.Scale(noise_control, from_=0, to=1, resolution = 0.001, length=100, orient="horizontal")
InitialNoiseSlider.pack(side="left")
noise_spacer = Tkinter.Frame(noise_control, width=200) 
noise_spacer.pack(side="left")
# Start button
start_control = Tkinter.Frame(snail_window) 
start_control.pack(side="left") 
StartButton = Tkinter.Button(start_control, text = "SIM", width = 3, command = executeSim) 
StartButton.pack(side="left") 
# Print mode menu 
print_mode = Tkinter.StringVar(start_control) 
print_mode.set("b/w") 
print_menu = Tkinter.OptionMenu(start_control, print_mode, "b/w", "diff", "color") 
print_menu.pack(side="left")
# Simulation parameter menu
sim_parameters = Tkinter.StringVar(start_control) 
sim_parameters.set("2:oliva_porphyria") 
SimMenu = Tkinter.OptionMenu(start_control, sim_parameters, "1:thin_lines", "1:stripes1", "1:cepaea_nemoralis", "1:waves1", "1:conus_ebraeus", "1:waves_stripes", "1:dark_tri_waves", "1:triangles1", "1:bloody_tears", "1:hearts", "2:diagonals", "2:waves1", "2:amoria_ellioti", "2:conus_abbas", "2:ghosts", "2:oliva_porphyria", "2:dif_angle_lines", "3:caves", "3:chaos1", "3:stripes_n_waves") 
SimMenu.pack(side="left")
# Load simulation button
load_sim = Tkinter.Frame(snail_window) 
load_sim.pack(side="left") 
LoadSimButton = Tkinter.Button(start_control, text = "LOAD", width = 3, command = loadParameters) 
LoadSimButton.pack(side="left") 
# Mechanism menu
mechanism = Tkinter.StringVar(start_control) 
mechanism.set("2:act-sub") 
MechMenu = Tkinter.OptionMenu(start_control, mechanism, "1:act-in", "2:act-sub", "3:ext act-in") 
MechMenu.pack(side="left")


# /////// MAIN FUNCTION AND LOOP ///////

#dummyMain() 
loadParameters() 
executeSim() 
#snail_window.after(1, dummySnail())  
snail_window.mainloop()



