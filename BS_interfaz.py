# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:02:05 2016

@author: laura18
"""
#all imports
import os, glob
import subprocess

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
import math
import zipfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.animation as animation  #for the animation
#plt.rcParams['animation.ffmpeg_path'] = './brightsolitons/bs_evolution/ffmpegprog/bin/ffmpeg'   #relative to the ultracoldUB file
import matplotlib.image as mpimg

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT)

import time

Ui_MainWindow,QMainWindow=loadUiType('BS.ui')
class BS(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.file=open('output.txt','a')
        self.file.write('#################')
        self.file.write('Interfaz seleccionada: Bright Solitons')
        self.file.write('#################\n\n')
        self.setupUi(self)
        self.timer1=QtCore.QTimer(self)
        self.timer2=QtCore.QTimer(self)
        self.sim=0
        self.format=' '   #to know whether demo or start has been clicked
        
        #information about project
        showAction=QtGui.QAction('&Authors', self)
        showAction.triggered.connect(self.showAuthors)
        mainMenu=self.menuBar()
        fileMenu=mainMenu.addMenu('&About')
        fileMenu.addAction(showAction)      
        
        #let's hide unnecessary buttons for the moment and preselect buttons
        self.ButtonOn.hide() 
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.harm.hide()
        self.none.hide()
        self.info1.hide()
        self.wall.hide()
        self.label_5.hide()
        self.slider_simulation.hide()
        self.none_20.click()
        self.wall_1.click()
        self.window_sims.hide()
        self.btn_none.click()  #we select a potential (just in case no potential is chosen)
        
        self.demo1.clicked.connect(self.demo_1)  #for the harmonic movement demo
        self.demo2.clicked.connect(self.demo_2)  #for the split in 2 equal parts of the soliton
        
        #unzip all material in pulse_data (takes a few seconds the first time...)
        if (not os.path.exists('./brightsolitons/bs_evolution/pulse_data')):
            zip_ref = zipfile.ZipFile('./brightsolitons/bs_evolution/pulse_data.zip', 'r')
            zip_ref.extractall('./brightsolitons/bs_evolution/')
            zip_ref.close()
        else:
            pass
        #unzip all material in Demo_2 (takes a few seconds the first time...)
        if (not os.path.exists('./brightsolitons/Demo_2')):
            zip_ref = zipfile.ZipFile('./brightsolitons/Demo_2.zip', 'r')
            zip_ref.extractall('./brightsolitons/')
            zip_ref.close()
        else:
            pass

        #creating signals and connecting them with the function            
        self.slider_simulation.valueChanged.connect(self.simulation)
        self.ButtonOn.clicked.connect(self.on)
        self.ButtonBack.clicked.connect(self.backsim)
        self.ButtonPause.clicked.connect(self.pause)
        
        #let's give the possible values to sliders
        self.horizontalSlider_4.setMinimum(-60)
        self.horizontalSlider_4.setMaximum(-20)
        self.horizontalSlider_4.setSingleStep(1)
        self.horizontalSlider_4.TicksBelow
        self.horizontalSlider_5.setMinimum(1)
        self.horizontalSlider_2.setSingleStep(2)
        
        #show an initial image of an arbitrary soliton
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
            example=open('pinta.dat','r')
            lines=example.readlines()
            x=[]
            phi2=[]
            for i in range(0,len(lines)):
                x.append(float(lines[i].split('\t')[0]))
                phi2.append(float(lines[i].split('\t')[1]))
            example.close()
            ax=np.array(x)
            aphi=np.array(phi2)
        finally:
            os.chdir(prevdir)            
        self.fig=Figure()
        figini=self.fig.add_subplot(111)
        figini.set_xlabel("Position ($x/ \\xi$)")
        figini.set_ylabel("Density $|\psi|^2 \\xi$")
        figini.set_title("An example of bright soliton")
        figini.plot(ax,aphi)
        self.addmpl(self.fig)

        #keep on setting the initial configuration        
        self.play_2.hide()
        self.play.hide()
        self.play.clicked.connect(self.juga)
        self.tanca.clicked.connect(self.torna)
        self.intenta.clicked.connect(self.grafica)
        self.lot.hide()
        self.lot.setText("Light: On")
        self.btn_sim.hide()
        self.btn_sim.setText("Sim: 1")
        
        #connecting actions with functions
        self.lot.clicked.connect(self.turn_light)
        self.btn_sim.clicked.connect(self.change_sim)    
        self.horizontalSlider.valueChanged.connect(self.escriu2x)
        self.horizontalSlider_2.valueChanged.connect(self.escriu2v)
        self.hb.valueChanged.connect(self.escriu2hb)
        
        self.btn_none.clicked.connect(self.initial)
        self.btn_harm.clicked.connect(self.initial)
        self.btn_wall.clicked.connect(self.initial)
        
        self.horizontalSlider_5.valueChanged.connect(self.initial)  #velocity (barrier case)
        self.hb.valueChanged.connect(self.initial)                  #height barrier
        self.wb.valueChanged.connect(self.initial)                  #width barrier
        
        self.fig_dict={}
        
        self.mplfigs.itemClicked.connect(self.changefig)

        self.start.clicked.connect(self.start2)
        self.back.clicked.connect(self.close)
        
        #again the initial state
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
            example=open('pinta.dat','r')
            lines=example.readlines()
            x=[]
            phi2=[]
            for i in range(0,len(lines)):
                x.append(float(lines[i].split('\t')[0]))
                phi2.append(float(lines[i].split('\t')[1]))
            example.close()
            ax=np.array(x)
            aphi=np.array(phi2)
        finally:
            os.chdir(prevdir)
        
        if self.fig==None:
            self.rmmpl()            
            self.fig=Figure()
            self.addmpl(self.fig)
        self.fig.clear()
        figini=self.fig.add_subplot(111)
        figini.set_xlabel("Position ($x/ \\xi $)")
        figini.set_ylabel("Density $|\psi|^2 \\xi$")
        figini.set_title("An example of bright soliton")
        figini.plot(ax,aphi)
        self.canvas.draw()
        
        #keep on hiding things
        self.slider_simulation.hide()
        self.ButtonOn.hide()
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.value_sim.hide()
        self.label_5.hide()
        
    def turn_light(self):
        #to turn on or off the light in one of the animations
        if self.lot.text()=="Light: On":
            self.lot.setText("Light: Off")
        elif self.lot.text()=="Light: Off":
            self.lot.setText("Light: On")
            
    def change_sim(self):
        #to change the simulation that can be seen
        if self.format=='Demo' and self.btn_sim.text()=="Sim: 1":
            self.timer1.stop()
            self.timer2.stop()
            self.btn_sim.setText("Sim: 2")  #updating the name of the simulation
            self.rmmpl()
            self.mpl_window.hide()
            self.window_sims.show()
            self.sims_2.hide()
            self.sims.show()
            #make some buttons unable
            self.mplfigs.setEnabled(False)
            self.interaction.setEnabled(False)
            self.Confinement.setEnabled(False)
            self.ext_potential.setEnabled(False)
            self.slider_simulation.hide()
            self.ButtonOn.hide()
            self.ButtonBack.hide()
            self.ButtonPause.hide()
            self.label_5.hide()
            self.value_sim.hide()   
        
        elif self.format=='Start' and self.btn_sim.text()=="Sim: 1":
          #  self.fig=None  #added!
            self.timer1.stop()
            self.timer2.stop()
            self.btn_sim.setText("Sim: 2")  #updating the name of the simulation
            self.rmmpl()            
            self.mpl_window.hide()
            self.window_sims.show()
            self.sims_2.hide()
            self.sims.show()
            #make some buttons unable
            self.mplfigs.setEnabled(False)
            self.interaction.setEnabled(False)
            self.Confinement.setEnabled(False)
            self.ext_potential.setEnabled(False)
            self.slider_simulation.hide()
            self.ButtonOn.hide()
            self.ButtonBack.hide()
            self.ButtonPause.hide()
            self.label_5.hide()
            self.value_sim.hide() 
            
            """Let's write the animation here"""
            def update(i):
                global dt,ddt,t,v,prob,x0,y0,n
                prova = t/(15.0*dt) + ddt
                Npart = 1 + int(prova)
                x = np.empty([Npart])
                y = np.empty([Npart])
                for j in range(0,Npart):
                    x[j] = x0[j]
                    y[j] = y0[j]
                    if n[j]==0:
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
                t += dt 
                return line,line2
                     
            global dt,ddt,t,v,prob,x0,y0,n
            
            fig3 = plt.figure()
            ax = fig3.add_subplot(111)
            ax.set_axis_bgcolor('black')
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            #we configure the plot (size)
            ax.set_ylim(-18.0,18.0)
            ax.set_xlim(-18.0,18.0)
            
            self.addmpl4(fig3)
            
            #plot particles
            line, = ax.plot([],[], "*", ms=12, color='white')
            line2, = ax.plot([],[], "o", ms=12, color='white',alpha=0.4)
            
            #some parameters
            timef=15    #total time of simulation
            v=6.0      #velocity of the partciles (FIXED)
            t=0.0       #initial time
            dt=0.05     #time step (FIXED)
            i=0         #a useless parameter, but given to the update() for not having problems with FuncAnimation()
            ##prob=0.10    #define probability == T trans. coeff.
            ddt=1.0e-7  #defined for not having problems with int() and the number of particles
            
            prevdir = os.getcwd()
            #reads the T coeff
            try:
                os.chdir(os.path.expanduser("./brightsolitons/bs_evolution"))
                datacoef=open('llum.dat','r')
                coef=datacoef.readlines()
                valueT=float((coef[0]).split('\t')[1])
                valueR=float((coef[0]).split('\t')[0])
                valueTot=valueT + valueR
                coefT=valueT/valueTot
                prob=coefT    #define probability == T trans. coeff.
                #and now the flashlight
                light=mpimg.imread('linterna4.png')
                ax.imshow(light,extent=(-18,-12,12,18),aspect='auto')
            finally:
                os.chdir(prevdir)            
            
            steps=int(timef/dt)     #to define the number of frames, one for each time step (dt)

            Ninter=10000000         #we define some arrays to be used
            x0=np.empty([Ninter])
            y0=np.empty([Ninter])
            n=np.empty([Ninter])    #counter for each particle

            for j in range(0,Ninter):           #we define the initial position of the supposed particles
                x0[j]=-13.75
                y0[j]=13.75
            
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
            
            self.ani = animation.FuncAnimation(fig3, update, frames=steps, interval=25,repeat=True)
            self.canvas.draw()            
            
        elif self.format=='Demo' and self.btn_sim.text()=="Sim: 2":
            self.timer1.stop()
            self.timer2.stop()
            self.btn_sim.setText("Sim: 3")  #updating the name of the simulation
            self.rmmpl4()
            self.mpl_window.hide()
            self.window_sims.show()
            #make some buttons unable
            self.mplfigs.setEnabled(False)
            self.interaction.setEnabled(False)
            self.Confinement.setEnabled(False)
            self.ext_potential.setEnabled(False)
            self.slider_simulation.hide()
            self.ButtonOn.hide()
            self.ButtonBack.hide()
            self.ButtonPause.hide()
            self.sims_2.show()
            self.sims.hide()
            self.label_5.hide()
            self.value_sim.hide()  
        
        elif self.format=='Start' and self.btn_sim.text()=="Sim: 2":
            self.timer1.stop()
            self.timer2.stop()
            self.btn_sim.setText("Sim: 3")  #updating the name of the simulation
            self.rmmpl4()               #added!
            self.mpl_window.hide()
            self.window_sims.show()
            #make some buttons unable
            self.mplfigs.setEnabled(False)
            self.interaction.setEnabled(False)
            self.Confinement.setEnabled(False)
            self.ext_potential.setEnabled(False)
            self.slider_simulation.hide()
            self.ButtonOn.hide()
            self.ButtonBack.hide()
            self.ButtonPause.hide()
            self.sims_2.show()
            self.sims.hide()
            self.label_5.hide()
            self.value_sim.hide()
            
            """Let's write the animation here"""
            def update(i):
                global dt2,ddt2,t2,v2,x0f,y0f,x0p,y0p,x0b,y0b,n2
                prova = t2/(15.0*dt2) + ddt2
                Npart = 1 + int(prova)
                xf = np.empty([Npart])             #x-positions of the forward-particles
                yf = np.empty([Npart])             #y-positions of the forward-particles
                xb = np.empty([Npart])             #x-positions of the backward-particles
                yb = np.empty([Npart])             #y-positions of the backward-particles
                xp = np.empty([Npart])             #x-positions of the previous-particles
                yp = np.empty([Npart])             #y-positions of the previous-particles
                for j in range(0,Npart):
                    if n2[j]==0:
                        xp[j] = x0p[j]
                        yp[j] = y0p[j]
                        xf[j] = -20
                        yf[j] = -20
                        xb[j] = -20
                        yb[j] = -20   #stop moving (out of range)
                        if xp[j]>=-1.1 and xp[j]<-0.5:    #if it's close to 0
                            x0f[j] = x0f[j] + float(v2*dt2)  #keeps going to the right
                            y0f[j] = y0f[j] - float(v2*dt2)  #keeps going onwards (y=0)
                            x0b[j] = x0b[j] - float(v2*dt2)  #goes to the left
                            y0b[j] = y0b[j] - float(v2*dt2)  #goes down
                            x0p[j] = -20
                            y0p[j] = -20  #stop moving
                            n2[j]=1
                        else:       #still not in the separating region
                            x0f[j] = x0f[j] + float(v2*dt2)  #keeps going to the right
                            y0f[j] = y0f[j] - float(v2*dt2)  #keeps going onwards (y=0)
                            x0b[j] = x0b[j] + float(v2*dt2)  #keeps going to the right
                            y0b[j] = y0b[j] - float(v2*dt2)  #keeps going onwards (y=0)
                            x0p[j] = x0p[j] + float(v2*dt2)  #keeps going to the right
                            y0p[j] = y0p[j] - float(v2*dt2)  #keeps going onwards (y=0)
                    else:
                        xf[j] = x0f[j]
                        yf[j] = y0f[j]
                        xb[j] = x0b[j]
                        yb[j] = y0b[j]
                        xp[j] = x0p[j]
                        yp[j] = y0p[j]
                        x0f[j] = x0f[j] + float(v2*dt2)
                        y0f[j] = y0f[j] - float(v2*dt2)
                        x0b[j] = x0b[j] - float(v2*dt2)  #goes to the left
                        y0b[j] = y0b[j] - float(v2*dt2)  #goes  down
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
                t2 += dt2 
                return line,line2,line3,line4,line5,line6
                     
            global dt2,ddt2,t2,v2,x0f,y0f,x0p,y0p,x0b,y0b,n2
            fig4 = plt.figure()
            ax = fig4.add_subplot(111)
            ax.set_axis_bgcolor('black')
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            #we configure the plot (size)
            ax.set_ylim(-18.0,18.0)
            ax.set_xlim(-18.0,18.0)
            
            self.addmpl5(fig4)
            
            prevdir = os.getcwd()
            #reads the T coeff
            try:
                os.chdir(os.path.expanduser("./brightsolitons/bs_evolution"))
                datacoef=open('llum.dat','r')
                coef=datacoef.readlines()
                valueT=float((coef[0]).split('\t')[1])
                valueR=float((coef[0]).split('\t')[0])
                valueTot=valueT + valueR
                coefT=valueT/valueTot
                #and now the flashlight
                light=mpimg.imread('linterna4.png')
                ax.imshow(light,extent=(-18,-12,12,18),aspect='auto')
            finally:
                os.chdir(prevdir) 
                
            prob=coefT    #define probability == T trans. coeff.
       #     print (prob)
            
            #plot particles
            line, = ax.plot([],[], "*", ms=15*prob, color='white')  #onwards (already passed)
            line2, = ax.plot([],[], "o", ms=15*prob, color='white',alpha=0.4)
            line3, = ax.plot([],[], "*", ms=15*(1.0-prob), color='white') #backwards (already hit)
            line4, = ax.plot([],[], "o", ms=15*(1.0-prob), color='white',alpha=0.4)
            line5, = ax.plot([],[], "*", ms=15, color='white') #going to the wall
            line6, = ax.plot([],[], "o", ms=15, color='white',alpha=0.4)
            
            #some parameters
            timef=15    #total time of simulation
            v2=6.0      #velocity of the partciles (FIXED)
            t2=0.0       #initial time
            dt2=0.05     #time step (FIXED)
            i=0         #a useless parameter, but given to the update() for not having problems with FuncAnimation()
         ##   prob2=0.10    #define probability == T trans. coeff.
            ddt2=1.0e-7  #defined for not having problems with int() and the number of particles
                
            steps=int(timef/dt2)     #to define the number of frames, one for each time step (dt)

            Ninter=10000000         #we define some arrays to be used
            x0f=np.empty([Ninter])
            y0f=np.empty([Ninter])
            x0b=np.empty([Ninter])
            y0b=np.empty([Ninter])
            x0p=np.empty([Ninter])
            y0p=np.empty([Ninter])
            n2=np.empty([Ninter])    #counter for each particle

            for j in range(0,Ninter):           #we define the initial position of the supposed particles
                x0f[j]=-13.75
                y0f[j]=13.75
                x0b[j]=-13.75
                y0b[j]=13.75
                x0p[j]=-13.75
                y0p[j]=13.75
            
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
            
            self.ani = animation.FuncAnimation(fig4, update, frames=steps, interval=25,repeat=True)
            self.canvas.draw() 
            
        elif self.btn_sim.text()=="Sim: 3":
            self.btn_sim.setText("Sim: 1")  #updating the name of the simulation
            self.sims_2.hide()
            self.sims.hide()
            self.window_sims.hide()
            self.rmmpl5()            #added!!
          #  self.fig=None
            #make some buttons able again
            self.mplfigs.setEnabled(True)
            self.interaction.setEnabled(True)
            self.Confinement.setEnabled(True)
            self.ext_potential.setEnabled(True)
            self.ButtonOn.setEnabled(True)
            self.ButtonBack.setEnabled(True)
            self.ButtonPause.setEnabled(True)
            self.slider_simulation.show()
            self.ButtonOn.show()
            self.ButtonBack.show()
            self.ButtonPause.show()
            self.label_5.show()
            self.value_sim.show()
            
            
            #### Plot the state previously shown before changing simulation
            if self.format=='Start':            
                initialdata=open('./brightsolitons/input.txt','r')
                data0=initialdata.readline().split('\t')
                valuex0=float(data0[2]) #initial position
                valuev0=float(data0[3]) #initial velocity
                valueconf=int(data0[4]) #confinement
                valuewb=float(data0[5]) #width barrier
                valuehb=float(data0[6]) #height barrier
                valuetime=float(data0[7]) #total time of simulation
                valuegn=int(data0[1]) #gn
            elif self.format=='Demo':
                valuex0=-20.0 #initial position
                valuev0=1.0 #initial velocity
                valueconf=1 #confinement
                valuewb=1.0 #width barrier
                valuehb=1.1 #height barrier
                valuetime=1.0 #total time of simulation
                valuegn=3 #gn code == -0.8
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser("./brightsolitons/bs_evolution"))
                if self.format=='Start':
                    datener=open('energies.dat','r')
                elif self.format=='Demo':
                    prevdir2=os.getcwd()
                    try:
                        os.chdir('..')
                        os.chdir(os.path.expanduser("./Demo_2"))
                        datener=open('energies.dat','r')
                    finally:
                        os.chdir(prevdir2)
                linener=datener.readlines()
                epart=float((linener[1].split('\t'))[1]) #as total energy is cte, we take the first one
                self.lot.show() 
                self.btn_sim.show()
                self.mpl_window.show()
                self.window_sims.hide()
                if self.format=='Start':
                    names=open("namefiles.dat",'r')
                elif self.format=='Demo':
                    prevdir2=os.getcwd()
                    try:
                        os.chdir('..')
                        os.chdir(os.path.expanduser("./Demo_2"))
                        names=open('namefiles.dat','r')
                    finally:
                        os.chdir(prevdir2)
                listnames=names.readlines()
                name=int(listnames[int(self.slider_simulation.value())])
                if self.format=='Start':
                    data=open("WfBs-%08d.dat" %(name),'r')
                elif self.format=='Demo':
                    prevdir2=os.getcwd()
                    try:
                        os.chdir('..')
                        os.chdir(os.path.expanduser("./Demo_2"))
                        data=open("WfBs-%08d.dat" %(name),'r')
                    finally:
                        os.chdir(prevdir2)
                lines=data.readlines()
                listpos=[]
                listphi=[]
                listpot=[]
                listconf=[]
                listtote=[]
                hb=[]
                listx1=[]
                listx2=[]
                listx3=[]
                if valuegn == 1:
                    a_s = -0.005e-3
                elif valuegn == 2:
                    a_s = -0.01e-3
                elif valuegn == 3:
                    a_s = -0.02e-3
                xiv=1.0/np.sqrt(2.0*(20.0e+3*a_s)**2) #from exact formula
                limp=0.5*valuewb*xiv
                
                for j in range(2,len(lines)):
                    listpos.append(float((lines[j].split('\t'))[0]))
                    listphi.append(float((lines[j].split('\t'))[1]))
                    listpot.append(float((lines[j].split('\t'))[5])-float((lines[j].split('\t'))[6])) #only barrier
                    listconf.append(float((lines[j].split('\t'))[6]))
                    listtote.append(epart)
                    if (np.abs(listpos[j-2])<=limp):
                        hb.append(1.0)
                    else:
                        hb.append(-1.0)
                    if listpos[j-2]<=0.0:                        
                        if valueconf==1 and listpos[j-2]>=-73:
                            listx1.append(float((lines[j].split('\t'))[0]))
                        elif valueconf==0 and listpos[j-2]>=-100:
                            listx1.append(float((lines[j].split('\t'))[0])) 
                        listx2.append(float((lines[j].split('\t'))[0]))
                    elif listpos[j-2]>=0.0:
                        listx3.append(float((lines[j].split('\t'))[0]))
                posit=np.array(listpos)
                phi2=np.array(listphi)
                pote=np.array(listpot)
                tote=np.array(listtote)
                confin=np.array(listconf)
                energymax=np.amax(tote)
                potmax=np.amax(pote)
                glass=np.array(hb)
                x1=np.array(listx1)
                x2=np.array(listx2)
                x3=np.array(listx3)
                        
            #    if self.fig==None:
            #        self.rmmpl()
            ##        self.fig=Figure()
            #        self.addmpl(self.fig)
            #    self.fig.clear()
                fig5=Figure()
                gs=GridSpec(8,1)  #8 rows and 1 column
                state=fig5.add_subplot(gs[2:,:])
                light=fig5.add_subplot(gs[0:2,:])
                light.axes.get_yaxis().set_visible(False)
                light.axes.get_xaxis().set_visible(False)
                state.set_xlabel("Position ($x/ \\xi$)")
                state.set_ylabel("Density $|\psi|^2 \\xi$")
                state.plot(posit,phi2)
                state.fill_between(posit,phi2,0,facecolor='0.80')
                potential=state.twinx()
                potential.plot(posit,pote,'g')
                potential.fill_between(posit,pote,0,hatch='-',facecolor='brown',alpha=0.6)
                potential.plot(posit,tote,'r', label='$E_{total}$') #in red the total energy
                potential.legend()
                if energymax >= potmax:
                    potential.set_ylim(0, 1.1*energymax)
                elif energymax <= potmax:
                    potential.set_ylim(0, 1.1*potmax)
                state.plot(posit,confin,'g')
                state.fill_between(posit,confin,0,hatch='-',facecolor='brown',alpha=0.6)
                potential.set_ylabel("Potential ($V $  ${m \\xi^2}/{\hbar^2}$)", color='g')
                state.set_ylim(0,0.3)
                light.set_ylim(-1,1)
                
                #we add the light analogy
                light.fill_between(posit,glass,-1,facecolor='blue',alpha=0.2)
                flight=mpimg.imread('linterna2.png')
                if self.format=='Start':
                    datacoef=open('llum.dat','r')
                elif self.format=='Demo':
                    prevdir2=os.getcwd()
                    try:
                        os.chdir('..')
                        os.chdir(os.path.expanduser("./Demo_2"))
                        datacoef=open('llum.dat','r')
                    finally:
                        os.chdir(prevdir2)
                coef=datacoef.readlines()
                valorT=float((coef[0]).split('\t')[1])
                valorR=float((coef[0]).split('\t')[0])
                valorTot=valorT + valorR
                coefT=valorT/valorTot
                coefR=valorR/valorTot
                
                if (valueconf==1):
                    state.set_xlim(-100,100)
                    light.set_xlim(-100,100)
                    light.imshow(flight,extent=(-100,-70,0,1),aspect='auto')
                    y1=-0.45*x1/73.0
                    y3=-0.45*x3/73.0
                    y2=0.45*x2/73.0
                else:
                    state.set_xlim(-128,128)
                    light.set_xlim(-128,128)
                    light.imshow(flight,extent=(-128,-98,0,1),aspect='auto')
                    y1=-0.42*x1/100.0
                    y3=-0.42*x3/100.0
                    y2=0.42*x2/100.0
                
                if self.lot.text()=="Light: On":
                    light.plot(x1,y1,color='yellow',linewidth=5.0,alpha=1.0)   #we plot the beams
                    light.plot(x2,y2,color='yellow',linewidth=5.0,alpha=coefR)
                    light.plot(x3,y3,color='yellow',linewidth=5.0,alpha=coefT)
                
                self.addmpl(fig5)  #plot it
            finally:
                os.chdir(prevdir) 
            
            #and show the plot
            self.mpl_window.show()
            self.fig=fig5
        
        
    def escriu2x(self):
        #to show in the interface the correct initial position (there's a change between the real and the slider value)
        self.valor_x0_none.setNum(2*self.horizontalSlider.value())
    
    def escriu2hb(self):
        #to show in the interface the correct initial position (there's a change between the real and the slider value)
        self.hb_valor.setNum(self.hb.value()/10.0)
        
    def escriu2v(self):
        #to show in the interface the correct initial velocity (there's a change between the real and the slider value)
        self.valor_v0_none.setNum(2*self.horizontalSlider_2.value())
        
    def initial(self):  #everytime we change the module (i.e. external potential)
        #hiding or showing things        
        self.lot.hide()
        self.btn_sim.hide()
        self.window_sims.hide()
        self.mpl_window.show()
        #let's show the initial state
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
            example=open('pinta.dat','r') #read data to plot an arbitrary soliton
            lines=example.readlines()
            x=[]
            phi2=[]
            if int(self.gn.value()) == 1: #get the input interaction, needed for barrier potential
                a_s = -0.005e-3
            elif int(self.gn.value()) == 2:
                a_s = -0.01e-3
            elif int(self.gn.value()) == 3:
                a_s = -0.02e-3
            xiv=1.0/np.sqrt(2.0*(20.0e+3*a_s)**2) #from exact formula
            if self.btn_wall.isChecked()==True:            
                limp=0.5*0.5*(2**self.wb.value())*xiv   #right wall of the barrier
                hb=[]
                Etot=[]
            for i in range(0,len(lines)):
                x.append(float(lines[i].split('\t')[0]))
                if self.btn_wall.isChecked()==True:
                    phi2.append(float(lines[int(len(lines))-(i+int(len(lines)/4.0))].split('\t')[1]))
                    if (np.abs(x[i])<=limp):
                        hb.append((self.hb.value()/10.0)*0.5*self.horizontalSlider_5.value()**2)
                    else:
                        hb.append(0.0)
                    Etot.append(0.5*self.horizontalSlider_5.value()**2)
                else:
                    phi2.append(float(lines[i].split('\t')[1]))
            example.close()
            ax=np.array(x)
            aphi=np.array(phi2)
            if self.btn_wall.isChecked()==True:
                tote=np.array(Etot)
                pote=np.array(hb)
        finally:
            os.chdir(prevdir)
        
        if self.fig==None:
            self.rmmpl()            
            self.fig=Figure()
            self.addmpl(self.fig)
        self.fig.clear()
        figini=self.fig.add_subplot(111)
        figini.set_xlabel("Position ($x/ \\xi $)")
        figini.set_ylabel("Density $|\psi|^2 \\xi$")
        figini.set_title("An example of bright soliton")
        figini.plot(ax,aphi)
        if self.btn_wall.isChecked()==True:  #draw the barrier and total energy in the plot to see the relation between them
            energymax=np.amax(tote)
            potmax=np.amax(pote)
            potential=figini.twinx()
            potential.plot(ax,pote,'g')
            potential.fill_between(ax,pote,0,hatch='-',facecolor='brown',alpha=0.6)
            potential.plot(ax,tote,'r', label='$E_{total}$') #in red the total energy
            potential.legend()
            if energymax >= potmax:
                potential.set_ylim(0, 1.1*energymax)
            elif energymax <= potmax:
                potential.set_ylim(0, 1.1*potmax)
            potential.set_ylabel("Potential ($V $  ${m \\xi^2}/{\hbar^2}$)", color='g')
        
        self.canvas.draw()
        
        self.slider_simulation.hide()
        self.ButtonOn.hide()
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.value_sim.hide()
        self.label_5.hide()
        
    def addmpl(self,fig):
        #to add the plots in the main layout
        self.canvas=FigureCanvas(fig)
        self.toolbar=NavigationToolbar(self.canvas,self.mpl_window,coordinates=True)
        self.mplvl.addWidget(self.toolbar)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw() 
        
    def rmmpl(self,): 
        #to delete the plots in the main layout
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        
    def addmpl4(self,fig):
        #to add the plots in the main layout
        self.canvas=FigureCanvas(fig)
        self.mplvl4.addWidget(self.canvas)
        self.canvas.draw() 
        
    def rmmpl4(self,): 
        #to delete the plots in the main layout
        self.mplvl4.removeWidget(self.canvas)
        self.canvas.close()
        
    def addmpl5(self,fig):
        #to add the plots in the main layout
        self.canvas=FigureCanvas(fig)
        self.mplvl5.addWidget(self.canvas)
        self.canvas.draw() 
        
    def rmmpl5(self,): 
        #to delete the plots in the main layout
        self.mplvl5.removeWidget(self.canvas)
        self.canvas.close()
        
    def addmpl2(self,fig):
        #to add the plots in the main layout
        self.canvas=FigureCanvas(fig)
        self.toolbar=NavigationToolbar(self.canvas,self.mpl_window,coordinates=True)
        self.mplvl_2.addWidget(self.toolbar)
        self.mplvl_2.addWidget(self.canvas)
        self.canvas.draw()        
        
    def rmmpl2(self,):
        #to delete the plots in the main layout
        self.mplvl_2.removeWidget(self.toolbar)
        self.toolbar.close()
        self.mplvl_2.removeWidget(self.canvas)
        self.canvas.close()       
        
    def addfig(self,name,fig):
        #add the figure to the list of plots
        self.fig_dict[name]=fig
        self.mplfigs.addItem(name)
        
    def changefig(self,item):
        #changing shown figure when clicked 
        self.mpl_window.show()
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        self.fig=None
        self.timer1.stop()
        self.timer2.stop()
        self.window_sims.hide()        
        
    def delfig(self):
        #delets all plots of the list
        listItems=self.mplfigs.selectedItems()
        if not listItems: return
        for item in listItems:
            self.mplfigs.takeItem(self.mplfigs.row(item))
            
    def demo_1(self): #harmonic
        if self.fig==None:
            self.rmmpl()            
            self.fig=Figure()
            self.addmpl(self.fig)
        self.fig.clear()
      #parat el 6/2/17  self.rmmpl()
        self.btn_none.click()   #for not having weird errors
        self.btn_harm.click()
        self.horizontalSlider_3.setValue(-25)
        self.spinBox.setValue(2)
        self.gn.setValue(3)
        self.yes_no.setValue(0)
        self.start.click()
        
    def demo_2(self): #barrier   #it does the same as start but with all fields on a folder (faster, everything already computed)
        self.format='Demo'      
        print self.format
        self.btn_none.click()   #for not having weird errors
        self.btn_wall.click()
        self.horizontalSlider_4.setValue(-20)
        self.horizontalSlider_5.setValue(1)
        self.wb.setValue(1)
        self.hb.setValue(11)
        self.gn.setValue(3)
        self.yes_no.setValue(1)
        self.wall_1.click()
        
        time_b=time.time()  #time counter (the computation starts)
        
        self.timer1.stop()
        self.timer2.stop()
        self.sim=0
        self.lot.hide()
        self.btn_sim.hide()
        self.btn_sim.setText("Sim: 1")
        self.window_sims.hide()
        
        #let's show the progress bar
        dialog = QtGui.QDialog()    
        progressBar = Ui_porcessProgress()
        progressBar.setupUi(dialog)
        dialog.show()       
        
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
            self.file.write('...Módulo seleccionado: Barrier potential...\n\n' )
            self.file.write('¿Se encuentra el solitón en una caja? '+'Sí'+'\n')
            self.file.write('Interacción=%.1f\nPosición inicial del solitón=%s\nVelocidad inicial del solitón=%s\nAnchura barrera=%.1f\nAltura barrera=%.1f\n\n' %(-0.8,self.horizontalSlider_4.value()*2.0,self.horizontalSlider_5.value()*2.0,0.5*(2**self.wb.value()),self.hb.value()/10.0))
            time1=2.5  #it lasts 5 seconds                
            progressBar.porcessProgressBar.setMaximum(time1)
            diff=0            
            prevdir2=os.getcwd()
            try:
                os.chdir(os.path.expanduser('./Demo_2'))
                while diff<time1:
                    diff=time.time()-time_b
                    progressBar.label.setText('Preparing everything for Demo 2...')
                    progressBar.porcessProgressBar.setValue(diff)                     
                    QApplication.processEvents()
                time.sleep(1)          
                time_e=time.time() #time counter (end of computation)
                print("Total time of computation: %.2f s" %(time_e-time_b)) #shows how long it takes to run the program (computation, files, etc)
                file=open('output_data.txt','r')
                self.file.write('%s\n\n' %file.read())
                self.file.write('Durada de la computación=%.2f s\n\n' %(time_e-time_b))
                #let's read the ouput files to plot the data            
                energyfile=open('./energies.dat','r')
                energy=energyfile.readlines()
                energyfile.close()
                meanvalfile=open('./meanvalues.dat','r')
                meanval=meanvalfile.readlines()
                meanvalfile.close()
            finally:
                os.chdir(prevdir2)
        finally:
            os.chdir(prevdir)
        
        #meanvalues (1st line of the data file is information)
        tmv=[]  #time
        mv=[]   #mean value
        smv=[]  #sigma
        velm=[]
        for i in range(1,len(meanval)):
            tmv.append(float((meanval[i].split('\t'))[0]))
            mv.append(float((meanval[i].split('\t'))[1]))
            smv.append(float((meanval[i].split('\t'))[2]))
            velm.append(float((meanval[i].split('\t'))[3]))
        fig1=Figure()
        figmv=fig1.add_subplot(111) #only one plot in the window
        atmv=np.array(tmv)
        amv=np.array(mv)
        asig=np.array(smv)
        sigsalt=[]
        for i in range(0,len(asig)):
            if(not(i%10)):
                sigsalt.append(asig[i])
            else:
                sigsalt.append(0.0)
        sigsalt=np.array(sigsalt)
          
        figmv.axes.errorbar(atmv,amv,yerr=sigsalt)
        figmv.axes.set_ylim([-25.0,25.0])
        figmv.set_title("Position of the soliton")
        figmv.set_xlabel("Time ($t$  $ {\hbar}/({m \\xi^2})$)") #all parameters are dimensionless
        figmv.set_ylabel("Position ($x/ \\xi$)")  
        
        #energies
        ftime=[]
        etot=[]
        chem=[]
        ekin=[]
        epot=[]
        eint=[]
        lint=[]
        iint=[]
        rint=[]
        for i in range(1,len(energy)):
            ftime.append(float((energy[i].split('\t'))[0]))
            etot.append(float((energy[i].split('\t'))[1]))
            chem.append(float((energy[i].split('\t'))[2]))
            ekin.append(float((energy[i].split('\t'))[3]))
            epot.append(float((energy[i].split('\t'))[4]))
            eint.append(float((energy[i].split('\t'))[5]))
            lint.append(float((energy[i].split('\t'))[6]))
            iint.append(float((energy[i].split('\t'))[7]))
            rint.append(float((energy[i].split('\t'))[8]))
        
        fig2=Figure()
        fig3=Figure()
          
        atime=np.array(ftime)
        aetot=np.array(etot)
        achem=np.array(chem)
        aekin=np.array(ekin)
        aepot=np.array(epot)
        aeint=np.array(eint)
        alint=np.array(lint)
        aiint=np.array(iint)
        arint=np.array(rint)
        
        allenergies=fig2.add_subplot(111)
        allenergies.plot(atime,aetot,label='$E_{tot}$')
        allenergies.plot(atime,achem,label='$\mu$')
        allenergies.plot(atime,aekin,label='$E_{kin}$')
        allenergies.plot(atime,aepot,label='$E_{pot}$')
        allenergies.plot(atime,aeint,label='$E_{int}$')
        allenergies.set_title("Energies")
        
        allenergies.set_xlabel("Time ($t $  ${\hbar}/({m \\xi^2})$)")
        allenergies.set_ylabel("Energy per particle ($E $  $({m \\xi^2})/{\hbar^2}$)")
        allenergies.legend()
        integrals=fig3.add_subplot(111)
        integrals.plot(atime,alint,label='left side')
        integrals.plot(atime,aiint,label='inside')
        integrals.plot(atime,arint,label='right side')
        integrals.set_xlabel("Time ($t$  $ {\hbar}/({m \\xi^2})$)")
        integrals.set_title("Integrals of the wave function")
        integrals.legend()
        
        fig4=Figure()
        avelm=np.array(velm)
        meanvelocity=fig4.add_subplot(111)
        meanvelocity.plot(atmv,avelm)
        meanvelocity.set_title("Mean velocity of the soliton")
        meanvelocity.set_xlabel("Time ($t $  ${\hbar}/({m \\xi^2})$)")
        meanvelocity.set_ylabel("$<v>$ ($v $  ${m \\xi}/{\hbar}$)")
        
        self.delfig()
        self.delfig()
        self.delfig()
        self.delfig()
        self.addfig("Integral",fig3)
        self.addfig("Position's mean value", fig1)
        self.addfig("Energies",fig2)
        self.addfig("Velocity",fig4)
        self.slider_simulation.setMinimum(0)
        self.slider_simulation.setMaximum(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))            
        self.slider_simulation.setSingleStep(1)
        
        #we remove and add animation
        try:
            self.mplvl4.removeWidget(self.movie_scr)
            self.mplvl5.removeWidget(self.movie_scr2)
        except:
            pass
        
        prevdir=os.getcwd()
        try:                
            os.chdir(os.path.expanduser("./brightsolitons/Demo_2"))
            self.movie = QMovie("simulation_1.gif", QByteArray(), self)
            self.movie_scr = QLabel()
            self.mplvl4.addWidget(self.movie_scr)
            self.movie.setCacheMode(QMovie.CacheAll)
            self.movie.setSpeed(100)
            self.movie_scr.setMovie(self.movie)
            self.movie.start()
            
            self.movie2 = QMovie("simulation_2.gif", QByteArray(), self)
            self.movie_scr2 = QLabel()
            self.mplvl5.addWidget(self.movie_scr2)
            self.movie2.setCacheMode(QMovie.CacheAll)
            self.movie2.setSpeed(100)
            self.movie_scr2.setMovie(self.movie2)
            self.movie2.start()
        finally:
            os.chdir(prevdir)
                
        self.ButtonOn.show() 
        self.ButtonBack.show()
        self.ButtonPause.show()
        self.slider_simulation.show()
        self.label_5.show()
        self.value_sim.show()
        self.play.hide()
        
        self.sim=0
        self.slider_simulation.setValue(self.sim+1)
        self.slider_simulation.setValue(self.sim-1)
        
    def start2(self):
        self.format='Start'
        print self.format
        time_b=time.time()  #time counter (the computation starts)
        self.timer1.stop()
        self.timer2.stop()
        self.sim=0
        self.lot.hide()
        self.btn_sim.hide()
        self.btn_sim.setText("Sim: 1")
        self.window_sims.hide()
        
        #let's show the progress bar
        dialog = QtGui.QDialog()    
        progressBar = Ui_porcessProgress()
        progressBar.setupUi(dialog)
        dialog.show()
        diff = 0
        
        #first we have to delete all previous files related to evolution
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
            
            dir = "bs_evolution" # name of the directory
            name = "WfBs" # general name of the files
            
            files_evolution = "%s/%s-*.dat" % (dir, name)
            files_energies = "%s/energies.dat" % (dir)
            for f in glob.glob(files_evolution):
                os.remove( f )
            for f in glob.glob(files_energies):
                os.remove( f )
            
            if (self.btn_none.isChecked()==True):
                pot=0
                if self.none_20.isChecked()==True:
                    tempss=20.0
                elif self.none_40.isChecked()==True:
                    tempss=40.0
                elif self.none_40.isChecked()==False or self.none_20.isChecked()==False:
                    tempss=20.0
            elif (self.btn_harm.isChecked()==True):
                pot=1
            else:
                pot=2
                if self.wall_1.isChecked()==True:
                    tempss=1.0
                elif self.wall_2.isChecked()==True:
                    tempss=2.0
                elif self.wall_3.isChecked()==True:
                    tempss=3.0
                elif self.wall_1.isChecked()==False or self.wall_2.isChecked()==False:
                    tempss=1.0
            file_data=open('input.txt','w')
#            self.slider_simulation.setValue(self.sim)
            if self.yes_no.value()==0:
                con="No"
            elif self.yes_no.value()==1:
                con="Sí"
            gn_val=-0.1*2**(self.gn.value())
            if (self.btn_none.isChecked()==True):
                self.file.write('...Módulo seleccionado: No external potential...\n\n')
                self.file.write('¿Se encuentra el solitón en una caja? '+con+'\n')
                self.file.write('Interacción=%.1f\nPosición inicial del solitón=%s\nVelocidad inicial del solitón=%s\n\n' %(gn_val,self.horizontalSlider.value()*2.0,self.horizontalSlider_2.value()*2.0))
                file_data.write('%d \t %d \t %f \t %f \t %d \t %f' %(0,self.gn.value(),self.horizontalSlider.value()*2.0,self.horizontalSlider_2.value()*2.0,self.yes_no.value(),tempss))
            elif (self.btn_harm.isChecked()==True):
                self.file.write('...Módulo seleccionado: Harmonic trap...\n\n' )
                self.file.write('¿Se encuentra el solitón en una caja? '+con+'\n')
                self.file.write('Interacción=%.1f\nPosición inicial del solitón=%s\nNúmero de oscilaciones=%s\n\n' %(gn_val,self.horizontalSlider_3.value(),int(self.spinBox.value())))
                file_data.write('%d \t %d \t %f \t %d \t %d' %(1,self.gn.value(),self.horizontalSlider_3.value(),self.spinBox.value(),0))
            elif (self.btn_wall.isChecked()==True):
                self.file.write('...Módulo seleccionado: Barrier potential...\n\n' )
                self.file.write('¿Se encuentra el solitón en una caja? '+con+'\n')
                self.file.write('Interacción=%.1f\nPosición inicial del solitón=%s\nVelocidad inicial del solitón=%s\nAnchura barrera=%.1f\nAltura barrera=%.1f\n\n' %(gn_val,self.horizontalSlider_4.value()*2.0,self.horizontalSlider_5.value()*2.0,0.5*(2**self.wb.value()),self.hb.value()/10.0))
                file_data.write('%d \t %d \t %f \t %f \t %d \t %f \t %f \t %f' %(2,self.gn.value(),self.horizontalSlider_4.value(),self.horizontalSlider_5.value(),self.yes_no.value(),0.5*(2**self.wb.value()),self.hb.value()/10.0, tempss))
            file_data.close()
                       
            subprocess.Popen('python gpe_bright_solitons.py',shell=True)

            if (self.btn_none.isChecked()==True):
                time1=101                
                progressBar.porcessProgressBar.setMaximum(time1)
                diff=0
                prev=os.getcwd()
                os.chdir(os.path.expanduser('./bs_evolution'))
                while diff<time1:
                    diff=0                    
                    for root, dirs, files in os.walk(os.getcwd()):
                        for file in files:
                            if file.startswith("WfBs"):
                                diff +=1
                                
                        if (diff<10):
                            progressBar.label.setText(u'Starting with Gross-Pitaevskii equation...')
                        if (diff<time1-10) and (diff>10):
                            progressBar.label.setText('Evolution in real time in progress...')
                        if (diff<time1) and (diff>time1-10):
                            progressBar.label.setText('Writing results ...')
                        progressBar.porcessProgressBar.setValue(diff)                     
                        QApplication.processEvents()
                os.chdir(prev)
                    
            if (self.btn_harm.isChecked()==True):
                time1=60*self.spinBox.value()+1                
                progressBar.porcessProgressBar.setMaximum(time1)
                diff=0
                prev=os.getcwd()
                os.chdir(os.path.expanduser('./bs_evolution'))
                while diff<time1:
                    diff=0
                    for root, dirs, files in os.walk(os.getcwd()):
                        for file in files:
                            if file.startswith("WfBs"):
                                diff +=1
                            
                        if (diff<10):
                            progressBar.label.setText(u'Starting with Gross-Pitaevskii equation...')
                        if (diff<time1-10) and (diff>10):
                            progressBar.label.setText('Evolution in real time in progress...')
                        if (diff<time1) and (diff>time1-10):
                            progressBar.label.setText('Writing results ...')
                        progressBar.porcessProgressBar.setValue(diff)                     
                        QApplication.processEvents()
                os.chdir(prev)
                    
            if (self.btn_wall.isChecked()==True):
                time1=5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value()))+1                
                progressBar.porcessProgressBar.setMaximum(time1)
                diff=0
                prev=os.getcwd()
                os.chdir(os.path.expanduser('./bs_evolution'))
                while diff<time1:
                    diff=0                    
                    for root, dirs, files in os.walk(os.getcwd()):
                        for file in files:
                            if file.startswith("WfBs"):
                                diff +=1
                                
                        if (diff<10):
                            progressBar.label.setText(u'Starting with Gross-Pitaevskii equation...')
                        if (diff<time1-10) and (diff>10):
                            progressBar.label.setText('Evolution in real time in progress...')
                        if (diff<time1-5) and (diff>time1-10):
                            progressBar.label.setText('Writing results ...')
                        if (diff<time1) and (diff>time1-5):
                            progressBar.label.setText('Taking stars from the sky to build the simulation...')
                        progressBar.porcessProgressBar.setValue(diff)                     
                        QApplication.processEvents()
                os.chdir(prev)
            
            time.sleep(2)
            
            time_e=time.time() #time counter (end of computation)
            print("Total time of computation: %.2f s" %(time_e-time_b)) #shows how long it takes to run the program (computation, files, etc)
            
            prevdir_2=os.getcwd()
            try:
                os.chdir("..")
                file=open('output_data.txt','r')
                self.file.write('%s\n\n' %file.read())
                self.file.write('Durada de la computación=%.2f s\n\n' %(time_e-time_b))
                file.close()    
            finally:
                os.chdir(prevdir_2)
                
            self.ButtonOn.show() 
            self.ButtonBack.show()
            self.ButtonPause.show()
            self.slider_simulation.show()
            self.label_5.show()
            self.value_sim.show()
            #show play plots depending on the chosen potential
            if pot==1:
                self.play.show()
            else:
                self.play.hide()
            #let's read the ouput files to plot the data            
            energyfile=open('./bs_evolution/energies.dat','r')
            energy=energyfile.readlines()
            energyfile.close()
            meanvalfile=open('./bs_evolution/meanvalues.dat','r')
            meanval=meanvalfile.readlines()
            meanvalfile.close()
        
        finally:
            os.chdir(prevdir)
                        
        #meanvalues (1st line of the data file is information)
        tmv=[]  #time
        mv=[]   #mean value
        smv=[]  #sigma
        velm=[]
        for i in range(1,len(meanval)):
            tmv.append(float((meanval[i].split('\t'))[0]))
            mv.append(float((meanval[i].split('\t'))[1]))
            smv.append(float((meanval[i].split('\t'))[2]))
            velm.append(float((meanval[i].split('\t'))[3]))
        fig1=Figure()
        figmv=fig1.add_subplot(111) #only one plot in the window
        atmv=np.array(tmv)
        amv=np.array(mv)
        asig=np.array(smv)
        sigsalt=[]
        for i in range(0,len(asig)):
            if(not(i%10)):
                sigsalt.append(asig[i])
            else:
                sigsalt.append(0.0)
        sigsalt=np.array(sigsalt)
        if pot==1:
            figmv.plot(atmv,amv)
            figmv.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
            figmv.axes.set_ylim([-abs(self.horizontalSlider_3.value())-2.0,abs(self.horizontalSlider_3.value())+2.0])
        elif pot==2:
            figmv.axes.errorbar(atmv,amv,yerr=sigsalt)
            figmv.axes.set_ylim([min(amv)-10.0,max(amv)+10.0])
        elif pot==0:
            figmv.plot(atmv,amv)
            figmv.axes.set_ylim([min(amv)-10.0,max(amv)+10.0])
        figmv.set_title("Position of the soliton")
        if pot==0 or pot==2:
            figmv.set_xlabel("Time ($t$  $ {\hbar}/({m \\xi^2})$)") #all parameters are dimensionless
            figmv.set_ylabel("Position ($x/ \\xi$)")
        elif pot==1:
            figmv.set_xlabel("Time ($t$ $\omega_{ho}$)")
            figmv.set_ylabel("Position ($x/a_{ho}$)")
            
        #energies
        ftime=[]
        etot=[]
        chem=[]
        ekin=[]
        epot=[]
        eint=[]
        lint=[]
        iint=[]
        rint=[]
        for i in range(1,len(energy)):
            ftime.append(float((energy[i].split('\t'))[0]))
            etot.append(float((energy[i].split('\t'))[1]))
            chem.append(float((energy[i].split('\t'))[2]))
            ekin.append(float((energy[i].split('\t'))[3]))
            epot.append(float((energy[i].split('\t'))[4]))
            eint.append(float((energy[i].split('\t'))[5]))
            if pot==2:
                lint.append(float((energy[i].split('\t'))[6]))
                iint.append(float((energy[i].split('\t'))[7]))
                rint.append(float((energy[i].split('\t'))[8]))
            else:
                pass
                
        fig2=Figure()
        fig3=Figure()
          
        atime=np.array(ftime)
        aetot=np.array(etot)
        achem=np.array(chem)
        aekin=np.array(ekin)
        aepot=np.array(epot)
        aeint=np.array(eint)
        if pot==2:
            alint=np.array(lint)
            aiint=np.array(iint)
            arint=np.array(rint)
        else:
            pass
           
        allenergies=fig2.add_subplot(111)
        allenergies.plot(atime,aetot,label='$E_{tot}$')
        allenergies.plot(atime,achem,label='$\mu$')
        allenergies.plot(atime,aekin,label='$E_{kin}$')
        allenergies.plot(atime,aepot,label='$E_{pot}$')
        allenergies.plot(atime,aeint,label='$E_{int}$')
        allenergies.set_title("Energies")
        if pot==0 or pot==2:
            allenergies.set_xlabel("Time ($t $  ${\hbar}/({m \\xi^2})$)")
            allenergies.set_ylabel("Energy per particle ($E $  $({m \\xi^2})/{\hbar^2}$)")
        elif pot==1:
            allenergies.set_xlabel("Time ($t$ $\omega_{ho}$)")
            allenergies.set_ylabel("Energy per particle ($E/ \hbar \omega_{ho}$)")
        allenergies.legend()
        if pot==2:
            integrals=fig3.add_subplot(111)
            integrals.plot(atime,alint,label='left side')
            integrals.plot(atime,aiint,label='inside')
            integrals.plot(atime,arint,label='right side')
            integrals.set_xlabel("Time ($t$  $ {\hbar}/({m \\xi^2})$)")
            integrals.set_title("Integrals of the wave function")
            integrals.legend()
        elif pot==1:    
            allenergies.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
            
        fig4=Figure()
        avelm=np.array(velm)
        meanvelocity=fig4.add_subplot(111)
        meanvelocity.plot(atmv,avelm)
        meanvelocity.set_title("Mean velocity of the soliton")
        if pot==0 or pot==2:
            meanvelocity.set_xlabel("Time ($t $  ${\hbar}/({m \\xi^2})$)")
            meanvelocity.set_ylabel("$<v>$ ($v $  ${m \\xi}/{\hbar}$)")
        elif pot==1:
            meanvelocity.set_xlabel("Time ($t$ $\omega_{ho}$)")
            meanvelocity.set_ylabel("$<v>$ ($v/ a_{ho} \omega_{ho}$)")
            meanvelocity.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
            
        fig7=Figure()       #only for harmonic potential
        velpos=fig7.add_subplot(111)
        velpos.plot(amv,avelm)
        velpos.set_title("$<v>$ with $<x>$")
        velpos.set_xlabel("Position ($x/ a_{ho}$)")
        velpos.set_ylabel("$<v>$ ($v/ a_{ho} \omega_{ho}$)")
          
        self.delfig()
        self.delfig()
        self.delfig()
        self.delfig()
        if pot==2:
            self.addfig("Integral",fig3)
        elif pot==1:
            self.addfig("Mean velocity with position",fig7)
        else:
            pass
        self.addfig("Position's mean value", fig1)
        self.addfig("Energies",fig2)
        self.addfig("Velocity",fig4)
        
        if self.btn_none.isChecked()==True:
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(100)
            self.slider_simulation.setSingleStep(1)
        elif self.btn_wall.isChecked()==True:
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))            
            self.slider_simulation.setSingleStep(1)
        else:
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(60*self.spinBox.value())
            self.slider_simulation.setSingleStep(1)
        
        self.sim=0
        self.slider_simulation.setValue(self.sim+1)
        self.slider_simulation.setValue(self.sim-1)
            
    def juga(self): #enables a window for play-plot
        self.interaction.setEnabled(False)
        self.Confinement.setEnabled(False)
        self.ext_potential.setEnabled(False)
        self.rmmpl()
        self.timer1.stop()
        self.timer2.stop()
        self.mpl_window.hide()
        fig=Figure()
        self.addmpl2(fig)
        self.play_2.show()
       
    def torna(self): #hides the play-plot window and returns to normal plots
        self.interaction.setEnabled(True)
        self.Confinement.setEnabled(True)
        self.ext_potential.setEnabled(True)
        self.ButtonOn.setEnabled(True)
        self.ButtonBack.setEnabled(True)
        self.ButtonPause.setEnabled(True)
        self.rmmpl2()
        self.play_2.hide()        
        fig=Figure()
        self.addmpl(fig)
        self.mpl_window.show()
        self.fig=None
        
    def grafica(self): #play-plot
        self.rmmpl()
        figura=Figure()
        self.addmpl2(figura)
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
            meanvalfile=open('./bs_evolution/meanvalues.dat','r')
            meanval=meanvalfile.readlines()
            meanvalfile.close()
        finally:
            os.chdir(prevdir)
        tmv=[]
        mv=[]
        listcos=[]
        for i in range(1,len(meanval)):
            tmv.append(float((meanval[i].split('\t'))[0]))
            mv.append(float((meanval[i].split('\t'))[1]))
            listcos.append(float(self.A.value()*np.cos(self.w.value()*float((meanval[i].split('\t'))[0]))))
        figmv=figura.add_subplot(111)
        atmv=np.array(tmv)
        amv=np.array(mv)
        acos=np.array(listcos)
        figmv.plot(atmv,amv)
        figmv.plot(atmv,acos)
        figmv.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
        figmv.axes.set_ylim([-34.0,34.0])
        figmv.set_title("Position of the soliton")
        figmv.set_xlabel("Time ($t$ $\omega_{ho}$)")
        figmv.set_ylabel("Position ($x/ a_{ho}$)")
            
    def simulation(self):
        self.lot.hide()
        self.btn_sim.hide()
        self.sim=self.slider_simulation.value()
        if self.format=='Start':
            initialdata=open('./brightsolitons/input.txt','r')
            data0=initialdata.readline().split('\t')
            pot=int(data0[0])  #input: external potential
        elif self.format=='Demo':
            pot=2 #barrier potential
        if self.format=='Start' and pot==0:
            valuex0=float(data0[2]) #initial position
            valuev0=float(data0[3]) #initial velocity
            valueconf=int(data0[4]) #confinement
            valuetime=float(data0[5]) #total time of simulation
            valuegn=int(data0[1]) #gn
        elif self.format=='Start' and pot==1:
            valuex0=float(data0[2]) #initial position
            valueoscil=int(data0[3]) #number oscillations
            valuegn=int(data0[1]) #gn
        elif self.format=='Start' and pot==2:
            valuex0=float(data0[2]) #initial position
            valuev0=float(data0[3]) #initial velocity
            valueconf=int(data0[4]) #confinement
            valuewb=float(data0[5]) #width barrier
            valuehb=float(data0[6]) #height barrier
            valuetime=float(data0[7]) #total time of simulation
            valuegn=int(data0[1]) #gn
        elif self.format=='Demo':
            valuex0=-20.0 #initial position
            valuev0=1.0 #initial velocity
            valueconf=1 #confinement
            valuewb=1.0 #width barrier
            valuehb=1.1 #height barrier
            valuetime=1.0 #total time of simulation
            valuegn=3 #gn code == -0.8
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser("./brightsolitons/bs_evolution"))
            if self.format=='Start':    
                datener=open('energies.dat','r')
            elif self.format=='Demo':
                prevdir2=os.getcwd()
                try:
                    os.chdir('..')
                    os.chdir(os.path.expanduser("./Demo_2"))
                    datener=open('energies.dat','r')
                finally:
                    os.chdir(prevdir2)
            linener=datener.readlines()
            epart=float((linener[1].split('\t'))[1]) #as total energy is cte, we take the first one
            if self.format=='Start' and pot==0:
                self.mpl_window.show()
                self.window_sims.hide()
                if int(valuetime)==20:
                    i=self.slider_simulation.value()*200
                elif int(valuetime)==40:
                    i=self.slider_simulation.value()*400
                else:
                    i=self.slider_simulation.value()*200
                data=open("WfBs-%08d.dat" %(i),'r')
                lines=data.readlines()
                listpos=[]
                listphi=[]
                listpot=[]
                listconf=[]
                for j in range(2,len(lines)):
                    listpos.append(float((lines[j].split('\t'))[0]))
                    listphi.append(float((lines[j].split('\t'))[1]))
                    listpot.append(float((lines[j].split('\t'))[5]))
                    listconf.append(float((lines[j].split('\t'))[6]))
                posit=np.array(listpos)
                phi2=np.array(listphi)
                pote=np.array(listpot)
                confin=np.array(listconf)
                
                if (valueconf==1): #soliton in a box
                    if self.fig==None:
                        self.rmmpl()
                        self.fig=Figure()
                        self.addmpl(self.fig)
                    self.fig.clear()
                    gs=GridSpec(8,1)  #8 rows and 1 column
                    state=self.fig.add_subplot(gs[0:6,:])
                    wave=self.fig.add_subplot(gs[6:8,:])
                    wave.set_xlabel("Position ($x/ \\xi$)")
                    state.set_ylabel("Density $|\psi|^2 \\xi$")
                    state.plot(posit,phi2)
                    state.fill_between(posit,phi2,0,facecolor='0.80')
                    state.plot(posit,pote,'g',label="Potential")
                    state.plot(posit,confin,'g')
                    state.fill_between(posit,confin,0,hatch='-',facecolor='brown',alpha=0.6)
                    state.set_ylim(0,0.3)
                    state.set_xlim(-120,120)
                    wave.set_xlim(-120,120)
                    state.axes.get_xaxis().set_visible(False)
                    wave.axes.get_yaxis().set_visible(False)                    
                    
                    state.legend()
                    
                    #let's plot the wave on the string
                    Nini=10.0*(valuex0+50.0)
                    Nnow=int(Nini + (i/100.0)*valuev0) #for any time (t=20 or t=40)
                    data=open('./pulse_data/string-%08d.dat' %(round(Nnow)),'r')
                    datalin=data.readlines()
                    xstringl=[]
                    ystringl=[]
                    for l in range(1,386):
                        xstringl.append(float(datalin[l].split('\t')[0])*100.0)
                        ystringl.append(float(datalin[l].split('\t')[1]))
                    xstring=np.array(xstringl)
                    ystring=np.array(ystringl)
                    wave.plot(xstring,ystring,color='brown',linewidth=2.0)
                    wave.set_ylim(-1.05,1.05)
                    
                    left=mpimg.imread('lside_hand.png')
                    right=mpimg.imread('rside_hand.png')
                    wave.imshow(left,extent=(-120,-96,-0.5,0.5),aspect='auto')
                    wave.imshow(right,extent=(96,120,-0.5,0.5),aspect='auto')
                                        
                    self.canvas.draw()
                
                elif (valueconf==0): #soliton in a ring                                           
                    if self.fig==None:
                        self.rmmpl()
                        self.fig=Figure()
                        self.addmpl(self.fig)
                    self.fig.clear()
                    state=self.fig.add_subplot(111)
                    state.set_xlabel("Position ($x/ \\xi$)")
                    state.set_ylabel("Density $|\psi|^2 \\xi$")
                    state.plot(posit,phi2)
                    state.fill_between(posit,phi2,0,facecolor='0.80')
                    state.plot(posit,pote,'g',label="Potential")
                    state.plot(posit,confin,'g')
                    state.fill_between(posit,confin,0,hatch='-',facecolor='brown',alpha=0.6)
                    state.set_ylim(0,0.3)
                    state.set_xlim(-128,128)
                    state.legend()
                    self.canvas.draw()
                    
            elif (pot==2 or self.format=='Demo') and self.btn_sim.text()=="Sim: 1":
                self.lot.show() 
                self.btn_sim.show()
                self.mpl_window.show()
                self.window_sims.hide()
                if self.format=='Start':
                    names=open("namefiles.dat",'r')
                elif self.format=='Demo':
                    prevdir2=os.getcwd()
                    try:
                        os.chdir("..")
                        os.chdir(os.path.expanduser("./Demo_2"))
                        names=open("namefiles.dat",'r')
                    finally:
                        os.chdir(prevdir2)
                listnames=names.readlines()
                name=int(listnames[int(self.slider_simulation.value())])
                if self.format=='Start':
                    data=open("WfBs-%08d.dat" %(name),'r')
                elif self.format=='Demo':
                    prevdir2=os.getcwd()
                    try:
                        os.chdir("..")
                        os.chdir(os.path.expanduser("./Demo_2"))
                        data=open("WfBs-%08d.dat" %(name),'r')
                    finally:
                        os.chdir(prevdir2)
                lines=data.readlines()
                listpos=[]
                listphi=[]
                listpot=[]
                listconf=[]
                listtote=[]
                hb=[]
                listx1=[]
                listx2=[]
                listx3=[]
                if valuegn == 1:
                    a_s = -0.005e-3
                elif valuegn == 2:
                    a_s = -0.01e-3
                elif valuegn == 3:
                    a_s = -0.02e-3
                xiv=1.0/np.sqrt(2.0*(20.0e+3*a_s)**2) #from exact formula
                limp=0.5*valuewb*xiv
                
                for j in range(2,len(lines)):
                    listpos.append(float((lines[j].split('\t'))[0]))
                    listphi.append(float((lines[j].split('\t'))[1]))
                    listpot.append(float((lines[j].split('\t'))[5])-float((lines[j].split('\t'))[6])) #only barrier
                    listconf.append(float((lines[j].split('\t'))[6]))
                    listtote.append(epart)
                    if (np.abs(listpos[j-2])<=limp):
                        hb.append(1.0)
                    else:
                        hb.append(-1.0)
                    if listpos[j-2]<=0.0:                        
                        if valueconf==1 and listpos[j-2]>=-73:
                            listx1.append(float((lines[j].split('\t'))[0]))
                        elif valueconf==0 and listpos[j-2]>=-100:
                            listx1.append(float((lines[j].split('\t'))[0])) 
                        listx2.append(float((lines[j].split('\t'))[0]))
                    elif listpos[j-2]>=0.0:
                        listx3.append(float((lines[j].split('\t'))[0]))
                posit=np.array(listpos)
                phi2=np.array(listphi)
                pote=np.array(listpot)
                tote=np.array(listtote)
                confin=np.array(listconf)
                energymax=np.amax(tote)
                potmax=np.amax(pote)
                glass=np.array(hb)
                x1=np.array(listx1)
                x2=np.array(listx2)
                x3=np.array(listx3)
                        
                if self.fig==None:
                    self.rmmpl()
                    self.fig=Figure()
                    self.addmpl(self.fig)
                self.fig.clear()
                gs=GridSpec(8,1)  #8 rows and 1 column
                state=self.fig.add_subplot(gs[2:,:])
                light=self.fig.add_subplot(gs[0:2,:])
                light.axes.get_yaxis().set_visible(False)
                light.axes.get_xaxis().set_visible(False)
                state.set_xlabel("Position ($x/ \\xi$)")
                state.set_ylabel("Density $|\psi|^2 \\xi$")
                state.plot(posit,phi2)
                state.fill_between(posit,phi2,0,facecolor='0.80')
                potential=state.twinx()
                potential.plot(posit,pote,'g')
                potential.fill_between(posit,pote,0,hatch='-',facecolor='brown',alpha=0.6)
                potential.plot(posit,tote,'r', label='$E_{total}$') #in red the total energy
                potential.legend()
                if energymax >= potmax:
                    potential.set_ylim(0, 1.1*energymax)
                elif energymax <= potmax:
                    potential.set_ylim(0, 1.1*potmax)
                state.plot(posit,confin,'g')
                state.fill_between(posit,confin,0,hatch='-',facecolor='brown',alpha=0.6)
                potential.set_ylabel("Potential ($V $  ${m \\xi^2}/{\hbar^2}$)", color='g')
                state.set_ylim(0,0.3)
                light.set_ylim(-1,1)
                
                light.fill_between(posit,glass,-1,facecolor='blue',alpha=0.2)
                flight=mpimg.imread('linterna2.png')
                if self.format=='Start':
                    datacoef=open('llum.dat','r')
                elif self.format=='Demo':
                    prevdir2=os.getcwd()
                    try:
                        os.chdir("..")
                        os.chdir(os.path.expanduser("./Demo_2"))
                        datacoef=open("llum.dat",'r')
                    finally:
                        os.chdir(prevdir2)
                coef=datacoef.readlines()
                valorT=float((coef[0]).split('\t')[1])
                valorR=float((coef[0]).split('\t')[0])
                valorTot=valorT + valorR
                coefT=valorT/valorTot
                coefR=valorR/valorTot
                
                if (valueconf==1):
                    state.set_xlim(-100,100)
                    light.set_xlim(-100,100)
                    light.imshow(flight,extent=(-100,-70,0,1),aspect='auto')
                    y1=-0.45*x1/73.0
                    y3=-0.45*x3/73.0
                    y2=0.45*x2/73.0
                else:
                    state.set_xlim(-128,128)
                    light.set_xlim(-128,128)
                    light.imshow(flight,extent=(-128,-98,0,1),aspect='auto')
                    y1=-0.42*x1/100.0
                    y3=-0.42*x3/100.0
                    y2=0.42*x2/100.0
                
                if self.lot.text()=="Light: On":
                    light.plot(x1,y1,color='yellow',linewidth=5.0,alpha=1.0)   #we plot the beams
                    light.plot(x2,y2,color='yellow',linewidth=5.0,alpha=coefR)
                    light.plot(x3,y3,color='yellow',linewidth=5.0,alpha=coefT)
                
                self.canvas.draw()
                
            elif (pot==2 or self.format=='Demo') and (self.btn_sim.text()=="Sim: 2" or self.btn_sim.text()=="Sim: 3"):
                self.btn_sim.show()                
                pass
                
            else:
                self.mpl_window.show()
                self.window_sims.hide()
                names=open("namefiles.dat",'r')
                listnames=names.readlines()
                name=int(listnames[int(self.slider_simulation.value())])
                data=open("WfBs-%08d.dat" %(name),'r')
                lines=data.readlines()
                listpos=[]
                listphi=[]
                listpot=[]
                listtote=[]
                for j in range(2,len(lines)):
                    listpos.append(float((lines[j].split('\t'))[0]))
                    listphi.append(float((lines[j].split('\t'))[1]))
                    listpot.append(float((lines[j].split('\t'))[5]))
                    listtote.append(epart)
                posit=np.array(listpos)
                phi2=np.array(listphi) 
                pote=np.array(listpot)
                tote=np.array(listtote)
                if self.fig==None:
                    self.rmmpl()
                    self.fig=Figure()
                    self.addmpl(self.fig)
                self.fig.clear()
                state=self.fig.add_subplot(111)
                potential=state.twinx()
                state.plot(posit,phi2,'b')
                state.fill_between(posit,phi2,0,facecolor='0.80')
                potential.plot(posit,pote,'g')
                potential.plot(posit,tote,'r', label='$E_{total}$') #in red the total energy
                potential.legend()
                state.set_xlabel("Position ($x/ a_{ho}$)")
                state.set_ylabel("Density $|\psi|^2 a_{ho}$", color='b')
                potential.set_ylabel("Potential ($V/ \hbar \omega_{ho}$)", color='g')
                potential.set_ylim(0,0.5*(np.abs(valuex0)+7)**2)
                if (valuex0 <= 0):
                    state.set_xlim(valuex0-7,-valuex0+7)
                elif (valuex0 > 0):
                    state.set_xlim(-valuex0-7,valuex0+7)
                if valuegn==1:
                    state.set_ylim(0,7.2)    
                elif valuegn==2:
                    state.set_ylim(0,4)
                elif valuegn==3:
                    state.set_ylim(0,2.2)
                self.canvas.draw()
        finally:
            os.chdir(prevdir)
            
#        print os.getcwd()   correct
                
    def on(self):
        if self.timer2==None:
            self.timer1=QtCore.QTimer(self)
            self.timer1.timeout.connect(self.plotsim)
            self.timer1.start(75)
        else:
            self.timer1=QtCore.QTimer(self)
            self.timer1.timeout.connect(self.plotsim)
            self.timer2.stop()
            self.timer1.start(75)
        #things that the user can/can't change
        self.interaction.setEnabled(False)
        self.Confinement.setEnabled(False)
        self.ext_potential.setEnabled(False)
        self.ButtonOn.setEnabled(False)
        self.ButtonBack.setEnabled(True)
        self.ButtonPause.setEnabled(True)
        
    def backsim(self):
        if self.timer1==None:
            self.timer2=QtCore.QTimer(self)
            self.timer2.timeout.connect(self.plotsim2)
            self.timer2.start(75)
        else:
            self.timer2=QtCore.QTimer(self)
            self.timer2.timeout.connect(self.plotsim2)
            self.timer1.stop()
            self.timer2.start(75)
        #things that the user can/can't change
        self.interaction.setEnabled(False)
        self.Confinement.setEnabled(False)
        self.ext_potential.setEnabled(False)
        self.ButtonOn.setEnabled(True)
        self.ButtonBack.setEnabled(False)
        self.ButtonPause.setEnabled(True)
        
    def pause(self):
        self.timer1.stop()
        self.timer2.stop()
        #enabling things
        self.interaction.setEnabled(True)
        self.Confinement.setEnabled(True)
        self.ext_potential.setEnabled(True)
        self.ButtonOn.setEnabled(True)
        self.ButtonBack.setEnabled(True)
        self.ButtonPause.setEnabled(True)
        
    def plotsim(self):
        self.sim=self.sim+1
        self.slider_simulation.setValue(self.sim)
        
        if self.format=='Start':
            initialdata=open('./brightsolitons/input.txt','r')
            data0=initialdata.readline().split('\t')
            pot=int(data0[0])  #input: external potential
        elif self.format=='Demo':
            pot=2
        if self.format=='Start' and pot==1:
            valuex0=float(data0[2]) #initial position
            valueoscil=int(data0[3]) #number oscillations
            valuegn=int(data0[1]) #gn
        elif self.format=='Start' and pot==2:
            valuex0=float(data0[2]) #initial position
            valuev0=float(data0[3]) #initial velocity
        elif self.format=='Demo':
            valuex0=-20.0 #initial position
            valuev0=1.0 #initial velocity
        
        if (pot==0):
            if (self.sim==100):
                self.timer1.stop()
                self.interaction.setEnabled(True)
                self.Confinement.setEnabled(True)
                self.ext_potential.setEnabled(True)
                self.ButtonOn.setEnabled(True)
                self.ButtonBack.setEnabled(True)
                self.ButtonPause.setEnabled(True)
        elif (pot==1):
            if (self.sim==(60*valueoscil)):
                    self.timer1.stop()
                    self.interaction.setEnabled(True)
                    self.Confinement.setEnabled(True)
                    self.ext_potential.setEnabled(True)
                    self.ButtonOn.setEnabled(True)
                    self.ButtonBack.setEnabled(True)
                    self.ButtonPause.setEnabled(True)
        elif (pot==2):
            if (self.sim==(5*math.ceil(-2.0*valuex0/float(valuev0)))):
                self.timer1.stop()
                self.interaction.setEnabled(True)
                self.Confinement.setEnabled(True)
                self.ext_potential.setEnabled(True)
                self.ButtonOn.setEnabled(True)
                self.ButtonBack.setEnabled(True)
                self.ButtonPause.setEnabled(True)
        
    def plotsim2(self):
        self.sim=self.sim-1
        self.slider_simulation.setValue(self.sim)
        
        if (self.sim==0):
            self.timer2.stop()
            self.interaction.setEnabled(True)
            self.Confinement.setEnabled(True)
            self.ext_potential.setEnabled(True)
            self.ButtonOn.setEnabled(True)
            self.ButtonBack.setEnabled(True)
            self.ButtonPause.setEnabled(True)
        
    def close(self):
        self.timer1.stop()
        self.timer2.stop()
        self.hide()
        self.file.close()
        self.parent().show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            self.file.close() 
        else:
            event.ignore()
    
    def showAuthors(self):
        QtGui.QMessageBox.question(self, 'Authors',
            "ULTRACOLDUB\n\nUniversitat de Barcelona")
            
class Ui_porcessProgress(object):
    def setupUi(self, porcessProgress):
        porcessProgress.setObjectName("porcessProgress")
        porcessProgress.setWindowModality(QtCore.Qt.ApplicationModal)
        porcessProgress.resize(329, 81)
        porcessProgress.setMinimumSize(QtCore.QSize(329, 81))
        porcessProgress.setMaximumSize(QtCore.QSize(329, 81))
        porcessProgress.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(porcessProgress)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(porcessProgress)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.porcessProgressBar = QtGui.QProgressBar(porcessProgress)
        self.porcessProgressBar.setMaximum(10)
        self.porcessProgressBar.setProperty("value", 10)
        self.porcessProgressBar.setTextVisible(False)
        self.porcessProgressBar.setObjectName("porcessProgressBar")
        self.verticalLayout.addWidget(self.porcessProgressBar)
        porcessProgress.setWindowTitle(QtGui.QApplication.translate("porcessProgress", "Please wait...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("porcessProgress", " in progress...", None, QtGui.QApplication.UnicodeUTF8))
        QtCore.QMetaObject.connectSlotsByName(porcessProgress)

class NavigationToolbar(NavigationToolbar2QT):  
    #for not showing undesired buttons
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home','Pan', 'Zoom', 'Save','Back','Forward')]