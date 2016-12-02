# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 13:28:56 2016

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
    global dt,ddt,v,prob,x0,y0,n
    prova = t/(8.0*dt) + ddt          #every 4 time steps, ddt is a small increment for the int to work properly
    Npart =  1 + int((prova))
    x = np.empty([Npart])             #x-positions of the particles
    y = np.empty([Npart])             #y-positions of the particles
    for j in range(0,Npart):
        x[j] = x0[j]
        y[j] = y0[j]
        if n[j]==0:     #if it's the first time that changes
            if x[j]>=-1.1 and x[j]<-0.5:    #if it's close to 0
                randnumber=np.random.random(size=None)   #gives us a random number
                if randnumber<=prob:
                    x0[j] = x0[j] + float(v*dt)  #keeps going to the right
                    y0[j] = y0[j] - float(v*dt)  #keeps going onwards (y=0)
                    n[j]=1                       #n=1 means that it passed
                else:
                    x0[j] = x0[j] - float(v*dt)  #goes to the left
                    y0[j] = y0[j] - float(v*dt)  #goes down
                    n[j]=2                       #n=2 means particle going backwards
            else:       #still not in the separating region
                x0[j] = x0[j] + float(v*dt)  #keeps going to the right
                y0[j] = y0[j] - float(v*dt)  #keeps going onwards (y=0)
        else:
            if n[j]==1:
                x0[j] = x0[j] + float(v*dt)
                y0[j] = y0[j] - float(v*dt)
            elif n[j]==2:
                x0[j] = x0[j] - float(v*dt)  #goes to the left
                y0[j] = y0[j] - float(v*dt)  #goes  down     
    line.set_xdata(x)
    line.set_ydata(y)
    line2.set_xdata(x)
    line2.set_ydata(y)
    return mplfig_to_npimage(fig_mpl)
    
global dt,ddt,v,prob,x0,y0,n

fig_mpl, ax = plt.subplots(1,facecolor='black')
ax.set_axis_bgcolor('black')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

#plot particles
line, = ax.plot([],[], "*", ms=12, color='white')
line2, = ax.plot([],[], "o", ms=12, color='white',alpha=0.4)

#some parameters
timef=12    #total time of simulation
v=10.0      #velocity of the partciles (FIXED)
t=0.0       #initial time
dt=0.05     #time step (FIXED)
##prob=0.50    #define probability == T trans. coeff.
ddt=1.0e-7  #defined for not having problems with int() and the number of particles

#reads the T coeff
datacoef=open('llum.dat','r')
coef=datacoef.readlines()
valueT=float((coef[0]).split('\t')[1])
valueR=float((coef[0]).split('\t')[0])
valueTot=valueT + valueR
coefT=valueT/valueTot
prob=coefT    #define probability == T trans. coeff.

#we configure the plot (size)
ax.set_ylim(-18.0,18.0)
ax.set_xlim(-18.0,18.0)

#steps=int(timef/dt)     #to define the number of frames, one for each time step (dt)

Ninter=10000000         #we define some arrays to be used
x0=np.empty([Ninter])
y0=np.empty([Ninter])
n=np.empty([Ninter])    #counter for each particle

for j in range(0,Ninter):           #we define the initial position of the supposed particles
    x0[j]=-13.75
    y0[j]=13.75

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
anim.write_gif('simulation_1.gif',program='ffmpeg',fps=15)
#plt.show()