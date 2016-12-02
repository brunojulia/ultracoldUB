# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 20:40:22 2016

@author: laura18

******************************************************************************

This program creates an animation to reproduce an analogy with the module of a 
bright soliton passing through a barrier. Given the energy and the height of 
the barrier, one can estimate an approximate transmision coefficient given the
probability of finding the soliton in each side. The probability obtained in 
the Interfaz_main.py (through gpe_bs_evolution.py) is read by this program and shown 
in the interface. To do so, moviepy is used.

The code is fully documented. The code has the option to save the animation in a
gif file, though the user may need the ffmpeg file to be able to save it.

This program also uses a particular naming for the variables:
xp, yp are the x and y coordinates for the particles before hitting the 'wall'
xf, yf are the x and y coordinates for the particles travelling to the right once
    it has arrived to 0, i.e. forward particles
xb, yb are the x and y coordinates for the particles travelling to the left once
    it has hit the 'wall', i.e. backward particles.
    
Velocity and dt are fixed in order to see the a clearer animation with a 
properly spacing between particles. 
"""

import matplotlib.pylab as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.image as mpimg
import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage
plt.rcParams['animation.ffmpeg_path'] = './ffmpegprog/bin/ffmpeg'


def update(t):
    global dt,ddt,v,prob,x0f,y0f,x0p,y0p,x0b,y0b,n
    prova = t/(8.0*dt) + ddt          #every 4 time steps, ddt is a small increment for the int to work properly
    Npart =  1 + int((prova))
    xf = np.empty([Npart])             #x-positions of the forward-particles
    yf = np.empty([Npart])             #y-positions of the forward-particles
    xb = np.empty([Npart])             #x-positions of the backward-particles
    yb = np.empty([Npart])             #y-positions of the backward-particles
    xp = np.empty([Npart])             #x-positions of the previous-particles
    yp = np.empty([Npart])             #y-positions of the previous-particles
    for j in range(0,Npart):      
        if n[j]==0:     #if it's the first time that changes
            xp[j] = x0p[j]
            yp[j] = y0p[j]
            xf[j] = -20
            yf[j] = -20
            xb[j] = -20
            yb[j] = -20   #stop moving (out of range)
            if xp[j]>=-1.1 and xp[j]<-0.5:    #if it's close to 0
                x0f[j] = x0f[j] + float(v*dt)  #keeps going to the right
                y0f[j] = y0f[j] - float(v*dt)  #keeps going onwards (y=0)
                x0b[j] = x0b[j] - float(v*dt)  #goes to the left
                y0b[j] = y0b[j] - float(v*dt)  #goes down
                x0p[j] = -20
                y0p[j] = -20  #stop moving
                n[j]=1            
            else:       #still not in the separating region
                x0f[j] = x0f[j] + float(v*dt)  #keeps going to the right
                y0f[j] = y0f[j] - float(v*dt)  #keeps going onwards (y=0)
                x0b[j] = x0b[j] + float(v*dt)  #keeps going to the right
                y0b[j] = y0b[j] - float(v*dt)  #keeps going onwards (y=0)
                x0p[j] = x0p[j] + float(v*dt)  #keeps going to the right
                y0p[j] = y0p[j] - float(v*dt)  #keeps going onwards (y=0)
        else:
            xf[j] = x0f[j]
            yf[j] = y0f[j]
            xb[j] = x0b[j]
            yb[j] = y0b[j]
            xp[j] = x0p[j]
            yp[j] = y0p[j]
            x0f[j] = x0f[j] + float(v*dt)
            y0f[j] = y0f[j] - float(v*dt)
            x0b[j] = x0b[j] - float(v*dt)  #goes to the left
            y0b[j] = y0b[j] - float(v*dt)  #goes  down
            x0p[j] = -20
            y0p[j] = -20  #stop moving
    line.set_xdata(xf)
    line.set_ydata(yf)
    line2.set_xdata(xf)
    line2.set_ydata(yf)
    line3.set_xdata(xb)
    line3.set_ydata(yb)
    line4.set_xdata(xb)
    line4.set_ydata(yb)
    line5.set_xdata(xp)
    line5.set_ydata(yp)
    line6.set_xdata(xp)
    line6.set_ydata(yp)
    return mplfig_to_npimage(fig_mpl)
    
    
global dt,ddt,v,prob,x0f,y0f,x0p,y0p,x0b,y0b,n

#some parameters
timef=12    #total time of simulation
v=10.0      #velocity of the partciles (FIXED)
t=0.0       #initial time
dt=0.05     #time step (FIXED)
##prob=0.8    #define probability == T trans. coeff.
ddt=1.0e-7  #defined for not having problems with int() and the number of particles

#reads the T coeff
datacoef=open('llum.dat','r')
coef=datacoef.readlines()
valueT=float((coef[0]).split('\t')[1])
valueR=float((coef[0]).split('\t')[0])
valueTot=valueT + valueR
coefT=valueT/valueTot
prob=coefT    #define probability == T trans. coeff.

fig_mpl, ax = plt.subplots(1,facecolor='black')
ax.set_axis_bgcolor('black')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

#plot particles
line, = ax.plot([],[], "*", ms=15*prob, color='white')  #onwards (already passed)
line2, = ax.plot([],[], "o", ms=15*prob, color='white',alpha=0.4)
line3, = ax.plot([],[], "*", ms=15*(1.0-prob), color='white') #backwards (already hit)
line4, = ax.plot([],[], "o", ms=15*(1.0-prob), color='white',alpha=0.4)
line5, = ax.plot([],[], "*", ms=15, color='white') #going to the wall
line6, = ax.plot([],[], "o", ms=15, color='white',alpha=0.4)

#we configure the plot (size)
ax.set_ylim(-18.0,18.0)
ax.set_xlim(-18.0,18.0)

Ninter=10000000         #we define some arrays to be used
x0f=np.empty([Ninter])
y0f=np.empty([Ninter])
x0b=np.empty([Ninter])
y0b=np.empty([Ninter])
x0p=np.empty([Ninter])
y0p=np.empty([Ninter])
n=np.empty([Ninter])    #counter for each particle

for j in range(0,Ninter):           #we define the initial position of the supposed particles
    x0f[j]=-13.75
    y0f[j]=13.75
    x0b[j]=-13.75
    y0b[j]=13.75
    x0p[j]=-13.75
    y0p[j]=13.75

# Set up formatting for the movie files
#FFwriter = animation.FFMpegWriter()

#let's plot like a barrier
barx=[]
bary=[]
for j in xrange(-200,200,1):
    barx.append(j/100.0)
    if j>=-100 and j<=100:
        bary.append(20.0)
    else:
        bary.append(-20.0)
abx=np.array(barx)
aby=np.array(bary)
ax.fill_between(abx,aby,-20,color='blue',alpha=(1-prob))

#and now the flashlight
light=mpimg.imread('linterna4.png')
ax.imshow(light,extent=(-18,-12,12,18),aspect='auto')

#let's do the animation
anim=mpy.VideoClip(update,duration=timef)
anim.write_gif('simulation_2.gif',program='ffmpeg',fps=15)
#plt.show()