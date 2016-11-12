# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:00:59 2016

@author: laura18
"""
import os
import subprocess

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
import math
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from PyQt4 import QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT)
pause_spr = False
on_spr = True
back_spr = False  
pause_nc = False
on_nc = True
back_nc = False 
Ui_MainWindow,QMainWindow=loadUiType('DS.ui')

class DS(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
#        self.mplfigs.hide()
#        self.mplwindow.hide()
        self.file=open('output.txt','a')
        self.ButtonOn.hide()
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.interact.hide()
        self.interact_2.hide()
        self.interact_3.hide()
        self.interact_game.hide()
        self.game.hide()
        self.state.hide()
        self.start.clicked.connect(self.start1)
        self.back.clicked.connect(self.close)
        self.ButtonOn.clicked.connect(self.on)
        self.ButtonBack.clicked.connect(self.back1)
        self.ButtonPause.clicked.connect(self.pause)        
        self.fig_dict={}
        
        self.mplfigs.itemClicked.connect(self.changefig)
        self.label_5.hide()
        self.slider_simulation.hide()
        self.horizontalSlider.valueChanged.connect(self.initial)
        self.slider_simulation.valueChanged.connect(self.simulation)
        
        self.pushButton_game.clicked.connect(self.game_call)
        self.pushButton_try.clicked.connect(self.graph_try)
        self.pushButton_return.clicked.connect(self.game_return)
        self.mplwindow_2.hide()
        
        self.timer1=QtCore.QTimer(self)
        self.timer2=QtCore.QTimer(self)
        
        self.ani_co=0
        
        file=open('position_0.txt','r')
        lines=file.readlines()
        file.close()
        x=[]
        x1=[]
        for line in lines:
            p=line.split()
            x.append(float(p[0]))
            x1.append(float(p[1]))
        xv=np.array(x)
        xv1=np.array(x1)

        self.fig=Figure()
        axf=self.fig.add_subplot(111)
        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
        axf.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
        axf.fill_between(xv,xv1,0.10,facecolor='black')
        axf.set_ylim(0.,0.1)
        axf.set_title('Bose-Einstein condensate')
        self.addmpl(self.fig) 

    def initial(self):
        file=open('initial.txt','r')
        lines=file.readlines()
        file.close()
        for i in range(1,13):
            globals()['x%s' %i]=[]
        for line in lines:
            p=line.split()
            for i in range(1,13):
                globals()['x%s' %i].append(float(p[i-1]))
        for i in range(1,13):
                globals()['xv%s' %i]=np.array(globals()['x%s' %i])       
        value=self.horizontalSlider.value()/10.
        
        for i in range(2,13):
            if value==i-7:
                if self.fig==None:
                    self.rmmpl()
                    self.fig=Figure()
                    self.addmpl(self.fig)
                    
                
                self.fig.clear()
                ax1f2=self.fig.add_subplot(111)
                ax1f2.set_xlabel('$x/a_{ho}$',fontsize=17)
                ax1f2.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                ax1f2.fill_between(xv1,globals()['xv%s' %i],0.10,facecolor='black')
                ax1f2.set_ylim(0.,0.1)
                ax1f2.set_title('initial state')
                self.canvas.draw()

    def changefig(self,item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        self.fig=None
        self.timer1.stop()
        self.timer2.stop()
        
    def addfig(self,name,fig):
        self.fig_dict[name]=fig
        self.mplfigs.addItem(name)       
        
    def delfig(self):
        listItems=self.mplfigs.selectedItems()
        if not listItems: return
        for item in listItems:
            self.mplfigs.takeItem(self.mplfigs.row(item))
            
    def addmpl(self,fig):
        self.canvas=FigureCanvas(fig)
        self.toolbar=NavigationToolbar(self.canvas,self,coordinates=True)
        self.mplvl.addWidget(self.toolbar)        
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        
    def rmmpl(self):
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()        
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()

    def addmpl2(self,fig):
        self.canvas=FigureCanvas(fig)
        self.toolbar=NavigationToolbar(self.canvas,self,coordinates=True)
        self.mplvl_2.addWidget(self.toolbar)        
        self.mplvl_2.addWidget(self.canvas)
        self.canvas.draw()
        
    def rmmpl2(self):
        self.mplvl_2.removeWidget(self.toolbar)
        self.toolbar.close()        
        self.mplvl_2.removeWidget(self.canvas)
        self.canvas.close()
        
    def plot(self):
        self.sim +=1
        self.slider_simulation.setValue(self.sim)
        
        if (self.radioButton.isChecked()==True):
            if (self.sim==74):
                self.timer1.stop()
            if (self.sim==self.spinBox.value()*int((10*np.pi*2.*np.sqrt(2.)))-1):
                self.timer1.stop()
        if (self.radioButton_3.isChecked()==True):
            if (self.sim==self.spinBox_4.value()*int((10*np.pi*2.*np.sqrt(2.)))-1):
                self.timer1.stop()
                
                
            
    def plot2(self):
        self.sim -=1
        self.slider_simulation.setValue(self.sim)

        
        if (self.sim==0):
            self.timer2.stop()
            
    def on(self):
        if self.timer2==None:
            self.timer1=QtCore.QTimer(self)
            self.timer1.timeout.connect(self.plot)
            self.timer1.start(75)
        else:
            self.timer1=QtCore.QTimer(self)
            self.timer1.timeout.connect(self.plot)
            self.timer2.stop()
            self.timer1.start(75)
    
    def pause(self):
        self.timer1.stop()
        self.timer2.stop()
        
    def back1(self):
        if self.timer1==None:
            self.timer2=QtCore.QTimer(self)
            self.timer2.timeout.connect(self.plot2)
            self.timer2.start(75)
        else:
            self.timer2=QtCore.QTimer(self)
            self.timer2.timeout.connect(self.plot2)
            self.timer1.stop()
            self.timer2.start(75)
            
    def game_call(self):
        self.timer1.stop()
        self.timer2.stop()
        if (self.radioButton.isChecked()==True):
            if (self.radioButton_densi.isChecked()==True):
                self.widget_osci.hide()
                time1=74
                self.widget_densi.show()
                self.textBrowser_2.show()
                self.textBrowser.hide()
                self.mplwindow.hide()
                self.start.hide()
                self.mplfigs.hide()
                self.rmmpl()
                self.rmmpl2()
                self.spin_mu.setValue(10.)
                self.spin_gn.setValue(100.)
                
                
                prevdir = os.getcwd()
                try:
                    os.chdir(os.path.expanduser('./darksolitons/output_0'))
                    for i in range(0,time1+1):
                        file=open('WfDs_Lin-%08d.txt'%(i),'r')
                        globals()['lines%s' %i]=file.readlines()
                        file.close()
        #               
        #            
                        if self.sim==i:                    
                            x1=[]
                            x2=[]
                            for line in (globals()['lines%s' %(i)]):
                                p=line.split()
                                x1.append(float(p[0]))
                                x2.append(float(p[1]))
                            globals()['xv1_lin%s' %(i)]=np.array(x1)
                            globals()['xv2_lin%s' %(i)]=np.array(x2)
                finally:
                        os.chdir(prevdir)
                
                    
                fig4=Figure()
                axf=fig4.add_subplot(111)
                axf.set_xlabel('$x/a_{ho}$',fontsize=17)
                axf.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                axf.fill_between(globals()['xv1_lin%s' %(self.sim)],globals()['xv2_lin%s' %(self.sim)],0.6,facecolor='black')
                axf.set_title('state at %s' %np.real(self.sim/10.))
                axf.set_ylim(0.,0.6)
                self.canvas.draw()
                self.addmpl2(fig4)
                
        if (self.radioButton_2.isChecked()==True) or (self.radioButton_3.isChecked()==True):
            
            if (self.radioButton_oscil.isChecked()==True):
                self.rmmpl()
                self.textBrowser_2.hide()
                self.textBrowser.show()
                self.rmmpl2()
                self.mplwindow.hide()
                if (self.radioButton_2.isChecked()==True):
                    self.widget_osci.show()
                    self.widget_osci_2.hide()
                    self.spin_amplitude.setValue(3.)
                    self.spin_frequency.setValue(0.5)
                if (self.radioButton_3.isChecked()==True):
                    self.widget_osci_2.show()
                    self.widget_osci.hide()
                    self.spin_amplitude_2.setValue(3.)
                    self.spin_frequency_2.setValue(0.5)
                self.widget_densi.hide()
                self.start.hide()
                self.mplfigs.hide()
                self.addmpl2(self.fig3)
                    
            if (self.radioButton_densi.isChecked()==True):
                self.spin_mu.setValue(25.)
                self.spin_gn.setValue(200.)
                if (self.radioButton_2.isChecked()==True):
                    time1=self.spinBox.value()*int((10*np.pi*2.*np.sqrt(2.)))
    
                if (self.radioButton_3.isChecked()==True):
                    time1=self.spinBox_4.value()*int((10*np.pi*2.*np.sqrt(2.)))
                    
                self.widget_osci.hide()
                self.widget_densi.show()
                self.textBrowser_2.show()
                self.textBrowser.hide()
                self.mplwindow.hide()
                self.start.hide()
                self.mplfigs.hide()
                self.rmmpl()
                self.rmmpl2()
                prevdir = os.getcwd()
                try:
                    os.chdir(os.path.expanduser('./darksolitons'))
                    for i in range(0,time1+1):
                        file=open('WfDs-%08d.txt'%(i),'r')
                        globals()['lines%s' %i]=file.readlines()
                        file.close()
        #               
        #            
                        if self.sim==i:                    
                            x1=[]
                            x2=[]
                            for line in (globals()['lines%s' %(i)]):
                                p=line.split()
                                x1.append(float(p[0]))
                                x2.append(float(p[1]))
                            globals()['xv1_%s' %(i)]=np.array(x1)
                            globals()['xv2_%s' %(i)]=np.array(x2)
                finally:
                        os.chdir(prevdir)
                 
                    
                fig3=Figure()
                ax1f3=fig3.add_subplot(111)
                ax1f3.set_xlabel('$x/a_{ho}$',fontsize=17)
                ax1f3.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                ax1f3.fill_between(globals()['xv1_%s' %(self.sim)],globals()['xv2_%s' %(self.sim)],0.1,facecolor='black')
                ax1f3.set_title('state at %s' %np.real(self.sim/10.)) 
                ax1f3.set_ylim(0.,0.1)
                self.addmpl2(fig3)                           
                
                
        self.game.show()
        self.mplwindow_2.show()
        
    def graph_try(self):
        if (self.radioButton.isChecked()==True):
            if (self.radioButton_densi.isChecked()==True):
                self.rmmpl()
                self.rmmpl2()
                
                xv3=self.spin_mu.value()-0.5*globals()['xv1_lin%s' %(self.sim)]**2
                for i in range(len(xv3)):
                    if xv3[i]<0:
                        xv3[i]=0
                xv3=np.abs(np.sqrt((xv3)/self.spin_gn.value()))**2.  
                fig5=Figure()
                self.addmpl2(fig5)
                ax1f3=fig5.add_subplot(111)
                ax1f3.set_xlabel('$x/a_{ho}$',fontsize=17)
                ax1f3.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                ax1f3.fill_between(globals()['xv1_lin%s' %(self.sim)],globals()['xv2_lin%s' %(self.sim)],0.6,facecolor='black')
                ax1f3.set_ylim(0.,0.6)                
                ax1f3.plot(globals()['xv1_lin%s' %(self.sim)],xv3,'y-',lw=2)
                ax1f3.set_title('state at %s' %np.real(self.sim/10.)) 
                self.canvas.draw() 
                
        if (self.radioButton_2.isChecked()==True) or (self.radioButton_3.isChecked()==True):
            if (self.radioButton_oscil.isChecked()==True):
                
                if (self.radioButton_2.isChecked()==True):
                    time1=self.spinBox.value()*int((10*np.pi*2.*np.sqrt(2.)))
    
                if (self.radioButton_3.isChecked()==True):
                    time1=self.spinBox_4.value()*int((10*np.pi*2.*np.sqrt(2.)))
                
                self.rmmpl2()
                psi_time=np.empty([512,time1])
                prevdir = os.getcwd()
                try:
                    os.chdir(os.path.expanduser('./darksolitons'))
                    for i in range (0,time1+1):
                        file=open('WfDs-%08d.txt'%(i),'r')
                        globals()['lines%s' %i]=file.readlines()
                        file.close()
                        x1=[]
                        x2=[]
                        for line in globals()['lines%s' %i]:
                            p=line.split()
                            x1.append(float(p[0]))
                            x2.append(float(p[1]))
                        xv1=np.array(x1)
                        xv2=np.array(x2)
                        psi_time[:,i-1]=xv2
                finally:
                    os.chdir(prevdir)
                
#                if (self.radioButton_2.isChecked()==True) and not (self.spinBox_2.value()==1) or (self.radioButton_3.isChecked()==True):
#                    fig3=Figure()
#                    self.addmpl2(fig3)
#                    ax1f3=fig3.add_subplot(111)
#                    ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
#                    ax1f3.set_xlabel('$T*w_{ho}$',fontsize=17)
#                    ax1f3.set_xlim(0,(time1-1)/10.)
#                    
#                    x=np.arange(0,time1+1)/10.
#                    y=self.spin_amplitude.value()*np.cos(self.spin_frequency.value()*x)
#                    
#                    ax1f3.pcolor(np.arange(0,time1+1)/10.,xv1,psi_time, cmap='Greys_r')  # plot the particle denisity
#                    ax1f3.plot(x,y)    
#                    ax1f3.set_ylim=(0.,0.6)
#                    ax1f3.set_title('evolution condensate')
#                    self.canvas.draw()
                
                if (self.radioButton_2.isChecked()==True):
                    self.ani_co += 1
                    if self.ani_co>1:
                        self.ani.event_source.stop()
                    tf_sim =  time1/10.
                    def simData():
                        L=self.spin_amplitude.value()
                        t_max =  time1/10.
                        dt = 0.05
                        w = self.spin_frequency.value()
                        y = 0.0
                        t = 0.0
                        while t <= t_max:
                            if on_spr and not back_spr and not pause_spr:
                                y = L*np.sin(w*t+np.pi/2.)
                                t = t + dt
                            if t<0:
                                y = L*np.sin(w*t+np.pi/2.)
                                t = t + dt
                            if back_spr and not on_spr and not pause_spr:
                                y = L*np.sin(w*t+np.pi/2.)
                                t = t - dt
                            yield y, t
                            
                    def onClick(event):
                        global pause_spr, on_spr, back_spr
                        back_spr ^= True
                        on_spr ^= True
                        
                    def init():
                        line.set_data([], [])
                        line2.set_data([], [])
                        line3.set_data([], [])
                        line4.set_data([], [])
                        for j in range (0,11):
                            globals() ['line_%s' %(j)].set_data([], [])
                        time_text.set_text('')
                        return line, time_text
                    
                    def simPoints(simData):
                        y, t = simData[0], simData[1]
                        if self.spin_amplitude.value()>=0:
                            ori = -self.spin_amplitude.value()-3.
                        if self.spin_amplitude.value()<=0:
                            ori = self.spin_amplitude.value()-3.
                        time_text.set_text(time_template%(t))
                        thisy = [ori, y]
                    
                        line.set_data(0,thisy)
                        for j in range (3,9):
                            globals() ['line_%s' %(j)].set_data([((-1)**(j-1))*0.5,((-1)**j)*0.5],[(j-1.)*((y-ori)/10.)+ori,((y-ori)/10.)*j+ori])
                        line_0.set_data([0.,0.5],[((((y-ori)/10.)*1.+ori)+(((y-ori)/10.)*2.+ori))/2.,((y-ori)/10.)*2.+ori])
                        line_1.set_data([0.5,0.],[((y-ori)/10.)*8.+ori,((((y-ori)/10.)*8.+ori)+(((y-ori)/10.)*9.+ori))/2.])
                        line2.set_data([1.,-1.],[ori,ori])  
                        line3.set_data([t,y])
                        tf = np.arange(0.0, t, 0.05)
                        line4.set_data([tf,self.spin_amplitude.value()*np.cos(tf*self.spin_frequency.value())])
                        time_text.set_text(time_template % (t))
                        return line, line2, line3, time_text,line_0, line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8, line_9, line4
    #                gs=0
                    ax=0
                    ax2=0
    #                import matplotlib.gridspec as gridspec 
                    fig3 = plt.figure()
    #                rcParams.update({'figure.autolayout': True})
    #                gs = gridspec.GridSpec(10, 10)
    #                ax = fig3.add_subplot(gs[:,03], xlim=(-0.5, 0.5), ylim=(-self.spin_amplitude.value()-2., +self.spin_amplitude.value()+2.))
    #                ax2 = fig3.add_subplot(gs[:,4:])
                    ax = plt.subplot2grid((10,10), (0,0), rowspan=10, colspan=2, autoscale_on=False, xlim=(-0.5, 0.5), ylim=(-10,10))
                    ax2 = plt.subplot2grid((10,10), (0,3), rowspan=10, colspan=7, autoscale_on=False, xlim=(0., tf_sim), ylim=(-10.,10))
    #                ax = fig3.add_subplot(121)   
    #                ax2 = fig3.add_subplot(122)
                    ax.set_title('Spring')
                    ax.set_xticks(np.arange(-1., 2., 1.))
                    ax.set_xlim(-1,1)
#                    if self.spin_amplitude.value()>=0:
#                        ax.set_ylim(-self.spin_amplitude.value()-2.,self.spin_amplitude.value()+2.)
#                    if self.spin_amplitude.value()<=0:
#                        ax.set_ylim(self.spin_amplitude.value()-2.,-self.spin_amplitude.value()+2.)
  
                    ax2.set_xlabel('$T*w_{ho}$',fontsize=17)        
                    ax2.set_ylabel('$x/a_{ho}$',fontsize=17)
                    ax2.pcolor(np.arange(0,time1+1)/10.,xv1,psi_time, cmap='Greys_r')  # plot the particle denisity
                    ax2.set_title('Condensate: real time evolution')
                    self.addmpl2(fig3)
                    
                    line, = ax.plot([], [], 'o-', lw=2)
                    line2, = ax.plot([], [], 'g-', lw=2)
                    line3, = ax2.plot([], [], 'o-', lw=2)
                    line4, = ax2.plot([], [], 'b-', lw=2)
                    for j in range (0,11):
                        globals() ['line_%s' %(j)], = ax.plot([], [], 'b-', lw=2)
                    time_template = 'time = %.1fs'
                    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
                    
                    fig3.canvas.mpl_connect('button_press_event', onClick)
                    self.ani = animation.FuncAnimation(fig3, simPoints, simData,
                                                  interval=25, blit=True, init_func=init, repeat=False)
                    
                    #ani.save('muelle.mp4', fps=15)
                    self.canvas.draw()
                
                if (self.radioButton_3.isChecked()==True):
                    self.ani_co += 1
                    if self.ani_co>1:
                        self.ani.event_source.stop()
                    on = True
                    back = False
                    pause = False
                      
                    B=self.spin_amplitude_2.value()
                    tf_sim =  time1/10.
                    r0=self.spin_rad.value()
                    def simData():
                        tf_sim =  time1/10.
                        dt = 0.01
                        M=self.spin_M.value()
                        N=self.spin_N.value()
                        r0=self.spin_rad.value()
                        A = 0.0
                        C = 0.0
                        D = 0.0
                        B=self.spin_amplitude_2.value()
                        w = self.spin_frequency_2.value()
                        impac=0
                        t_max = tf_sim
                        m2 = 1.
                        m1 = self.spin_ratio.value()
                        y = 0.0
                        y2=0.0
                        t = 0.0
                        t_1=0.0
                        i=0
                        r = ((1.+((N-1)/2.))*2.*r0)+(((M-1))*r0)
                        y_=np.empty([int(t_max/dt)+2,2])
                        t_=np.empty([int(t_max/dt)+2])
                        y_[0,0]=B
                        y_[0,1]=D
                        t_[0]=t
                        
                        while t <= t_max:
                            if on_nc and not back_nc and not pause_nc:
                                t += dt
                                t_1 += dt
                                i += 1
                            if t<0:
                                t += dt
                                t_1 += dt
                                i += 1
                            if back_nc and not on_nc and not pause_nc:
                                t -= dt
                                t_1 -= dt
                                i -= 1
                             
                            y = A*np.sin(w*t_1)+B*np.cos(w*t_1)
                            y2 = C*np.sin(w*t_1)+D*np.cos(w*t_1)
#                            der_y = A*w*np.cos(w*t_1)-B*w*np.sin(w*t_1)
#                            der_y2 = C*w*np.cos(w*t_1)-D*w*np.sin(w*t_1) 
                            
                            y_[i,0]=y
                            y_[i,1]=y2
                            t_[i]=t
                            if np.abs(y-y2)<(r+(r/100.)):
                              t1=t_1
                              impac +=1
                              A_=A
                              B_=B
                              C_=C
                              D_=D
                              
                              C=((m1-m2)/(m1+m2))*(A_*np.cos(w*t1)-B_*np.sin(w*t1))+((2*m2/(m1+m2))*(C_*np.cos(w*t1)-D_*np.sin(w*t1)))
                              D=A_*np.sin(w*t1)+B_*np.cos(w*t1)
                              A=(2*m1/(m1+m2))*(A_*np.cos(w*t1)-B_*np.sin(w*t1))+(((m2-m1)/(m1+m2))*(C_*np.cos(w*t1)-D_*np.sin(w*t1)))
                              B=C_*np.sin(w*t1)+D_*np.cos(w*t1)
                              
                              if (y-y2)>0:
                                  D=D-((N-1)/2.)*2.*r0+((M-1)*r0)
                                  B=B-((N-1)/2.)*2.*r0+((M-1)*r0)
                              if (y-y2)<0:
                                  D=D+((N-1)/2.)*2.*r0-((M-1)*r0)
                                  B=B+((N-1)/2.)*2.*r0-((M-1)*r0)
                                 
                              m1_=m1
                              m2_=m2
                              m1=m2_
                              m2=m1_
#                              print impac,np.abs(y-y2),t
                              t_1=0.
                            yield y, t, y2,t_,y_
        
                    def onClick(event):
                        global pause_nc, on_nc, back_nc
                        back_nc ^= True
                        on_nc ^= True
                        
                    def init():
                    #    time_text.set_text('')
                        line_nc_.set_data([], [])
                        line_nc_2.set_data([], [])
                        for i in range(0,14):
                            globals()['line_nc%s' %(i)].set_data([], [])
                    
                            return line_nc_,line_nc_2,line_nc_3,line_nc_4, globals()['line_nc%s' %(i)]
                        
                    def simPoints(simData):
                        dt = 0.01
                        M=self.spin_M.value()
                        N=self.spin_N.value()
                        r0=self.spin_rad.value()
                        B = self.spin_amplitude_2.value()
                        B_0=B
                        r=2*r0
                        y, t, y2, t_, y_ = simData[0], simData[1], simData[2], simData[3], simData[4]
                    #    time_text.set_text(time_template%(t))
                        
                        circle1.center=(y+(r*(M-1.)/2.),np.sqrt(B_0**2-(y+(r*(M-1.)/2.))**2.))
                        line_nc1.set_data([0.,y+(r*(M-1.)/2.)],[0.,np.sqrt(B_0**2-(y+(r*(M-1.)/2.))**2.)])
                        line_nc2.set_data(t,y+(r*(M-1.)/2.))
                        circle2.center=(t,y+(r*(M-1.)/2.))
                        line_nc_.set_data(t_[:int(t/dt)],y_[:int(t/dt),0])
                        if M==2:
                            line_nc11.set_data([0.,y-r/2.],[0.,np.sqrt(B_0**2-(y-r/2.)**2.)])
                            circle11.center=(y-r/2.,np.sqrt(B_0**2-(y-r/2.)**2.))
                            line_nc12.set_data(t,y-r/2.)
                            circle12.center=(t,y-r/2.)
                            
                        circle3.center=(y2-(r*(N-1.)/2.),np.sqrt(B_0**2-(y2-(r*(N-1.)/2.))**2.))
                        line_nc3.set_data([0.,y2-(r*(N-1.)/2.)],[0.,np.sqrt(B_0**2-(y2-(r*(N-1.)/2.))**2.)])
                        line_nc4.set_data([t,y2-(r*(N-1.)/2.)])
                        circle4.center=(t,y2-(r*(N-1.)/2.))
                        line_nc_2.set_data(t_[:int(t/dt)],y_[:int(t/dt),1]-(r*(N-1.)/2.))
                        if N==2:
                            circle5.center=(y2+r/2.,np.sqrt(B_0**2-(y2+r/2.)**2.))
                            line_nc5.set_data([0.,y2+r/2.],[0.,np.sqrt(B_0**2-(y2+r/2.)**2.)])
                            line_nc6.set_data([t,y2+r/2.])
                            circle6.center=(t,y2+r/2.)
                            line_nc_3.set_data(t_[:int(t/dt)],y_[:int(t/dt),1]+r/2.)
                        if N==3:
                            circle9.center=(y2,np.sqrt(B_0**2-y2**2.))
                            line_nc9.set_data([0.,y2],[0.,np.sqrt(B_0**2-y2**2.)])
                            line_nc10.set_data([t,y2])
                            line_nc_3.set_data(y_[:int(t/dt),1],t_[:int(t/dt)])
                            circle10.center=(t,y2)
                            circle7.center=(y2+r,np.sqrt(B_0**2-(y2+r)**2.))
                            line_nc7.set_data([0.,y2+r],[0.,np.sqrt(B_0**2-(y2+r)**2.)])
                            line_nc8.set_data([t,y2+r])
                            line_nc_4.set_data(t_[:int(t/dt)],y_[:int(t/dt),1]+r)
                            circle8.center=(t,y2+r)
                            
                    #    time_text.set_text(time_template % (t))
                        return (line_nc0, line_nc_, line_nc1, line_nc_2, line_nc_3, line_nc_4, line_nc3, line_nc4, line_nc5, line_nc6, line_nc7, line_nc8, line_nc9, line_nc10, line_nc11, line_nc12,
                               circle0, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, circle10, circle11, circle12)      
                        
                    fig = plt.figure()
                    ax = plt.subplot2grid((100,100), (0,0), rowspan=30, colspan=30, autoscale_on=False, xlim=(-B-r0-0.05,B+r0+0.05), ylim=(+B+r0+0.05,-B-r0-0.05))
                    ax2 = plt.subplot2grid((100,100), (0,40), rowspan=100, colspan=60, autoscale_on=False, xlim=(0., tf_sim), ylim=(-10.,10))
                    ax.set_title('NC')
                    #ax.set_xticks(np.arange(-1., 2., 1.))
                    ax.grid()
                    
                    
                    ax2.set_xlabel('$T*w_{ho}$',fontsize=17)        
                    ax2.set_ylabel('$x/a_{ho}$',fontsize=17)
                    ax2.pcolor(np.arange(0,time1+1)/10.,xv1,psi_time, cmap='Greys_r')  # plot the particle denisity
                    ax2.set_title('Condensate: real time evolution')
                    
                    for i in range(0,17,2):
                        globals()['line_nc%s' %(i)], = ax2.plot([], [], 'o-', lw=2)
                        globals() ['circle%s' %(i)] = plt.Circle((10., 10.), radius=r0)
                        ax2.add_patch(globals() ['circle%s' %(i)])
                    for i in range(1,17,2):
                        globals()['line_nc%s' %(i)], = ax.plot([], [], 'b-', lw=1)
                        globals() ['circle%s' %(i)] = plt.Circle((10., 10.), radius=r0)
                        ax.add_patch(globals() ['circle%s' %(i)])
                        
                    line_nc_, = ax2.plot([], [], 'b-', lw=2)
                    for i in range(2,5):
                        globals()['line_nc_%s' %(i)], = ax2.plot([], [], 'r-', lw=2)
                    #time_template = 'time = %.1fs'
                    #time_text = ax2.text(0.05, 0.9, '', transform=ax.transAxes)
                    self.addmpl2(fig)
                    fig.canvas.mpl_connect('button_press_event', onClick)
                    self.ani = animation.FuncAnimation(fig, simPoints, simData,
                                                  interval=1, blit=True, init_func=init, repeat=False)
                    #dt=0.01
                    #ani.save('NC_3_1.mp4')
                    self.canvas.draw()
                    
                    
            if (self.radioButton_densi.isChecked()==True):
                self.rmmpl2()
                
                xv3=self.spin_mu.value()-0.5*globals()['xv1_%s' %(self.sim)]**2
                for i in range(len(xv3)):
                    if xv3[i]<0:
                        xv3[i]=0
                xv3=np.abs(np.sqrt((xv3)/self.spin_gn.value()))**2.            
                
                fig3=Figure()
                self.addmpl2(fig3)
                ax1f3=fig3.add_subplot(111)
                ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
                ax1f3.set_xlabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                ax1f3.set_xlabel('$x/a_{ho}$',fontsize=17)
                ax1f3.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                ax1f3.fill_between(globals()['xv1_%s' %(self.sim)],globals()['xv2_%s' %(self.sim)],0.1,facecolor='black')
                ax1f3.set_ylim(0.,0.1)                  
                ax1f3.plot(globals()['xv1_%s' %(self.sim)],xv3,'y-',lw=2)
                ax1f3.set_title('state at %s' %np.real(self.sim/10.)) 
                self.canvas.draw()    
            
            
    def game_return(self):
        self.rmmpl2()
        self.rmmpl2()
        self.mplwindow_2.hide()
        self.game.hide()
        self.fig=Figure()
        self.addmpl(self.fig)
        self.mplwindow.show()
        self.start.show()
        self.mplfigs.show()

    def start1(self):
        self.timer1.stop()
        self.timer2.stop()
        dialog = QtGui.QDialog()    
        progressBar = Ui_porcessProgress()
        progressBar.setupUi(dialog)
        dialog.show()
        diff = 0

        
        if (self.radioButton.isChecked()==True):
            self.file.write('...Módulo seleccionado: Lineal continuation...\n\n' )
            self.file.write('Estado de excitación=%s\n\n' %(self.spinBox_3.value()))
            self.state.hide()
            self.interact_game.show()
            self.radioButton_oscil.hide()
            self.pushButton_game.show()
            self.sim=0
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons/output_0'))
                time1=75
                
                progressBar.porcessProgressBar.setMaximum(time1)
                diff=0
                while diff<time1:
                    diff=0
                    for root, dirs, files in os.walk(os.getcwd()):
                        for file in files:
                            if file.startswith("WfDs_Lin"):
                                diff += 1
#                                time.sleep(0.1)                      
#                        if (diff<2):
#                            progressBar.label.setText('Starting with Schrodinger equation...')
#                        if (diff<time1-10) and (diff>2):
#                            progressBar.label.setText('Imaginary time method in progress, adding non-lineality...')
#                        if (diff<time1) and (diff>time1-5):
#                            progressBar.label.setText('Writing results ...')
                        progressBar.porcessProgressBar.setValue(diff)                     
                        QApplication.processEvents()
                        
                print (os.getcwd())
                print ("READY")
                self.label_5.show()
                self.ButtonOn.show()
                self.ButtonBack.show()
                self.ButtonPause.show()
                self.radioButton_densi.setChecked(True)
                self.slider_simulation.show()
                self.slider_simulation.setMinimum(0)
                self.slider_simulation.setMaximum(74)
                self.slider_simulation.setSingleStep(1)
                time.sleep(2)
                file = open('lin.txt', 'r')
                lines = file.readlines()
                file.close()
                file2 = open('WfDs_Lin-%08d.txt'%(0))
                lines2 = file2.readlines()
                file2.close()
            finally:
                os.chdir(prevdir)   
                
            x2 = []
            y2 = []
            
            for line in lines2:
                p2 = line.split()
                x2.append(float(p2[0]))
                y2.append(float(p2[1]))
                
                
            xv2 = np.array(x2)
            yv2 = np.array(y2)
            
            
            self.rmmpl()
            self.fig=Figure()
            axf=self.fig.add_subplot(111)
            axf.set_xlabel('$x/a_{ho}$',fontsize=17)
            axf.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
            axf.fill_between(xv2,yv2,0.6,facecolor='black')
            axf.set_title('state at %s' %np.real(0/10.))
            self.addmpl(self.fig)
            
            
            
            x2 = []
            y2 = []
            z2 = []
            c2 = []
            v2 = []
            b2 = []
            for line in lines:
                p2 = line.split()
                x2.append(float(p2[1]))
                y2.append(float(p2[2]))
                b2.append(float(p2[3]))
                z2.append(float(p2[4]))
                c2.append(float(p2[5]))
                v2.append(float(p2[6]))
                
            xv2 = np.array(x2)
            yv2 = np.array(y2)
            zv2 = np.array(z2)
            cv2 = np.array(c2)
            vv2 = np.array(v2)
            bv2 = np.array(b2)
            
            fig1=Figure()
            ax1f1=fig1.add_subplot(111)
            ax1f1.set_ylabel('$\mu/hw$',fontsize=14)
            ax1f1.set_xlabel('$g_{int}$',fontsize=17)        
            ax1f1.plot(xv2,yv2, 'b.-')
            ax1f1.set_title('non-linear continuation')     
            
            
            
            fig2=Figure()
            ax1f2=fig2.add_subplot(111)
            ax1f2.set_ylabel('$E_{cin}/hw$',fontsize=14)
            ax1f2.set_xlabel('$g_{int}$',fontsize=17)        
            ax1f2.plot(xv2,zv2, 'b.-')
            ax1f2.set_title('non-linear continuation')     
            
            
            fig3=Figure()
            ax1f3=fig3.add_subplot(111)
            ax1f3.set_ylabel('$E_{pot}/hw$',fontsize=14)
            ax1f3.set_xlabel('$g_{int}$',fontsize=17)        
            ax1f3.plot(xv2,cv2, 'b.-')
            ax1f3.set_title('non-linear continuation')     
            
            fig4=Figure()
            ax1f4=fig4.add_subplot(111)
            ax1f4.set_ylabel('$E_{int}/hw$',fontsize=14)
            ax1f4.set_xlabel('$g_{int}$',fontsize=17)        
            ax1f4.plot(xv2,vv2, 'b.-')
            ax1f4.set_title('non-linear continuation')
            
            fig5=Figure()
            ax1f5=fig5.add_subplot(111)
            ax1f5.set_ylabel('$x/a_{ho}$',fontsize=14)
            ax1f5.set_xlabel('$g_{int}$',fontsize=17)        
            ax1f5.plot(xv2,bv2, 'b.-')
            ax1f5.set_title('non-linear continuation')
            
            self.delfig()
            self.delfig()
            self.delfig()
            self.delfig()
            self.addfig('CHEMICAL POTENTIAL',fig1)
            self.addfig('KINETIC ENERGY',fig2)
            self.addfig('POTENTIAL ENERGY',fig3)
            self.addfig('INTERACTION ENERGY',fig4)
            self.addfig('ATOMIC CLOUD LENGTH',fig5)
            self.slider_simulation.setValue(0)
        
        if (self.radioButton_2.isChecked()==True) or (self.radioButton_3.isChecked()==True):
            self.sim=0
            self.radioButton_dens.setChecked(True)
            if (self.radioButton_2.isChecked()==True):
                time1=self.spinBox.value()*int((10*np.pi*2.*np.sqrt(2.)))
                self.file.write('...Módulo seleccionado: Dark solitons study...\n\n' )
                self.file.write('Posición inicial del solitón=%s\nNúmero de oscilaciones=%s\nNúmero de solitones simétricos=%s\n\n' %(self.horizontalSlider.value()/10.0,self.spinBox.value(),self.spinBox_2.value()))

            if (self.radioButton_3.isChecked()==True):
                time1=self.spinBox_4.value()*int((10*np.pi*2.*np.sqrt(2.)))
                self.file.write('...Módulo seleccionado: Newton,s cradle...\n\n' )
                self.file.write('Número de solitones en movimiento=%s\nPosición de los solitones en movimiento=%s\nNúmero de oscilaciones=%s\nNúmero de solitones en cadena estacionaria=%s\n\n' %(self.spinBox_6.value(),self.horizontalSlider_2.value()/10.0,self.spinBox_4.value(),self.spinBox_5.value()))

            self.interact_game.show()
            self.radioButton_oscil.show()
            self.radioButton_oscil.setChecked(True)
            psi_time=np.empty([512,time1])
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons'))
                for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        if file.startswith("WfDs-"):
                             os.remove((os.path.join(root, file)))
                         
                file=open('input.txt','w')  
                if (self.radioButton_2.isChecked()==True):
                    file.write ('%s\t%s\t%s' %(self.horizontalSlider.value()/10.0,self.spinBox.value(),self.spinBox_2.value()))
                if (self.radioButton_3.isChecked()==True):
                    file.write ('%s\t%s\t%s' %(self.horizontalSlider_2.value()/10.0,self.spinBox_4.value(),self.spinBox_5.value()*self.spinBox_6.value()*2))
                file.close()
                
                start_sub=time.time()
                subprocess.Popen('python gpe_fft_ts_DS_v1.py',shell=True)
                progressBar.porcessProgressBar.setMaximum(time1)
                diff=0
                while diff<time1+1:
                    diff=0
                    for root, dirs, files in os.walk(os.getcwd()):
                        for file in files:
                            if file.startswith("WfDs-"):
                                diff +=1
                        
                        if (diff<10):
                            progressBar.label.setText('Imaginary time method in progress...')
                        if (diff<time1-10) and (diff>10):
                            progressBar.label.setText('Evolution in real time in progress...')
                        if (diff<time1) and (diff>time1-10):
                            progressBar.label.setText('Writing results ...')
                                                
                        progressBar.porcessProgressBar.setValue(diff)                     
                        QApplication.processEvents()
                  
                print (os.getcwd())
                print ("READY")
                self.state.show()
                self.interact_game.show()
                self.label_5.show()
                self.ButtonOn.show()
                self.ButtonBack.show()
                self.ButtonPause.show()
                self.slider_simulation.show()
                self.slider_simulation.setMinimum(0)
                if (self.radioButton_2.isChecked()==True):
                    self.slider_simulation.setMaximum(self.spinBox.value()*int((10*np.pi*2.*np.sqrt(2.)))-1)
                if (self.radioButton_3.isChecked()==True):
                    self.slider_simulation.setMaximum(self.spinBox_4.value()*int((10*np.pi*2.*np.sqrt(2.)))-1)
                self.slider_simulation.setSingleStep(1)
            
                time.sleep(2)
                end_sub=time.time()
                file=open('output_sp.txt','r')
                self.file.write('%s\n\n' %file.read())
                self.file.write('Durada de la computación=%s\n\n' %(end_sub-start_sub))
                
                file = open('energies.txt', 'r')
                lines = file.readlines()
                file.close()
                file2=open('phase.txt','r')
                lines2=file2.readlines()
                file2.close()
                file4=open('WfDs-%08d.txt'%(0),'r')
                lines4=file4.readlines()
                file4.close()
#                file3=open('min.txt','r')
#                lines3=file3.readlines()
#                file3.close()
                for i in range (0,time1+1):
                    file=open('WfDs-%08d.txt'%(i),'r')
                    globals()['lines%s' %i]=file.readlines()
                    file.close()
                    x1=[]
                    x2=[]
                    for line in globals()['lines%s' %i]:
                        p=line.split()
                        x1.append(float(p[0]))
                        x2.append(float(p[1]))
                    xv1=np.array(x1)
                    xv2=np.array(x2)
                    psi_time[:,i-1]=xv2
            finally:
                os.chdir(prevdir)
            
            x2 = []
            y2 = []
            
            for line in lines4:
                p2 = line.split()
                x2.append(float(p2[0]))
                y2.append(float(p2[1]))
                
                
            xv2 = np.array(x2)
            yv2 = np.array(y2)
            
            self.rmmpl()
            self.fig=Figure()
            axf4=self.fig.add_subplot(111)
            axf4.set_xlabel('$x/a_{ho}$',fontsize=17)
            axf4.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
            axf4.fill_between(xv2,yv2,0.1,facecolor='black')
            axf4.set_ylim(0.,0.10)
            axf4.set_title('state at %s' %np.real(0/10.))
            self.addmpl(self.fig)            
            
            self.fig3=Figure()
            ax1f3=self.fig3.add_subplot(111)
            ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
            ax1f3.set_xlabel('$T*w_{ho}$',fontsize=17)
            ax1f3.set_xlim(0,(time1-1)/10.)
            
            ax1f3.pcolor(np.arange(0,time1+1)/10.,xv1,psi_time, cmap='Greys_r')  # plot the particle denisity
            ax1f3.set_title('evolution condensate')
            
            
            
            x2 = []
            y2 = []
            for line in lines2:
                p2 = line.split()
                x2.append(float(p2[0]))
                y2.append(float(p2[1]))
            xv2 = np.array(x2)
            yv2 = np.array(y2)
            fig1=Figure()
            ax1f1=fig1.add_subplot(111)
            ax1f1.set_ylabel('PHASE',fontsize=14)
            ax1f1.set_xlabel('$T/t_{ho}$',fontsize=17)        
            ax1f1.plot(xv2,yv2, 'b.-')
            ax1f1.set_ylim(0,2*np.pi)
            ax1f1.set_title('Phase difference produced by soliton')
          
    
    
            
            x1 = []
            y1 = []
            z1 = []
            c1 = []
            v1 = []
            b1 = []
            for line in lines:
                p = line.split()
                x1.append(float(p[0]))
                y1.append(float(p[1]))
                z1.append(float(p[2]))       
                c1.append(float(p[3]))
                v1.append(float(p[4]))
                b1.append(float(p[5]))
            xv = np.array(x1)
            yv = np.array(y1)
            zv = np.array(z1)
            cv = np.array(c1)
            vv = np.array(v1)
            bv = np.array(b1)
            
            fig2=Figure()
            ax1f2=fig2.add_subplot(111)
            ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)        
            ax1f2.set_ylabel('$E/hw$',fontsize=17)
            ax1f2.plot(xv,yv, 'r.-' , label='Mean Energy')
            
            ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)
            ax1f2.set_ylabel('$E/hw$',fontsize=17)
            ax1f2.plot(xv,zv, 'g.-', label='Chemical Potential')
            
            ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)
            ax1f2.set_ylabel('$E/hw$',fontsize=17)
            ax1f2.plot(xv,cv, 'y.-', label='Kinetic energy')
            
            ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)
            ax1f2.set_ylabel('$E/hw$',fontsize=17)
            ax1f2.plot(xv,vv, 'b.-',label='Potential energy')
            
            ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)
            ax1f2.set_ylabel('$E/hw$',fontsize=17)
            ax1f2.plot(xv,bv, 'm.-', label='Interaction energy')
            
            ax1f2.legend()
              
            self.slider_simulation.setValue(0)
            
            if (self.radioButton_2.isChecked()==True):
                self.delfig()
                self.delfig()
                self.delfig()
                self.delfig()
                self.delfig()
                self.delfig()
                self.delfig()
                self.addfig('PHASE',fig1)
                self.addfig('ENERGY',fig2)
                self.addfig('DENSITY MAP',self.fig3)
                
            if (self.radioButton_3.isChecked()==True):
                self.delfig()
                self.delfig()
                self.delfig()
                self.delfig()
                self.delfig()
                self.delfig()
                self.addfig('ENERGY',fig2)
                self.addfig('DENSITY MAP',self.fig3)
                
                
    def simulation(self):
        if (self.radioButton.isChecked()==True):
            value=self.slider_simulation.value()
            time1=74
            self.sim=value
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons/output_0'))
                for i in range(0,time1+1):
                    file=open('WfDs_Lin-%08d.txt'%(i),'r')
                    globals()['lines%s' %i]=file.readlines()
                    file.close()
    #               
    #            
                    if value==i:                    
                        x1=[]
                        x2=[]
                        for line in (globals()['lines%s' %(i)]):
                            p=line.split()
                            x1.append(float(p[0]))
                            x2.append(float(p[1]))
                        xv1=np.array(x1)
                        xv2=np.array(x2)
                        
                        if self.fig==None:
                            self.rmmpl()
                            self.fig=Figure()
                            self.addmpl(self.fig)
                        self.fig.clear()
                        axf=self.fig.add_subplot(111)
                        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
                        axf.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                        axf.set_ylim([0,0.6])
                        axf.fill_between(xv1,xv2,0.6,facecolor='black')
                        axf.set_title('state at %s' %np.real(i/10.))
                        self.canvas.draw()
            finally:
                os.chdir(prevdir)
                
        if (self.radioButton_2.isChecked()==True) or (self.radioButton_3.isChecked()==True):
            if (self.radioButton_2.isChecked()==True):
                time1=self.spinBox.value()*int((10*np.pi*2.*np.sqrt(2.)))
            if (self.radioButton_3.isChecked()==True):
                time1=self.spinBox_4.value()*int((10*np.pi*2.*np.sqrt(2.)))
            value=self.slider_simulation.value()
            self.sim=value
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons'))
                for i in range(0,time1+1):
                    file=open('WfDs-%08d.txt'%(i),'r')
                    globals()['lines%s' %i]=file.readlines()
                    file.close()
    #               
    #            
                    if value==i:                    
                        x1=[]
                        x2=[]
                        for line in (globals()['lines%s' %i]):
                            p=line.split()
                            x1.append(float(p[0]))
#                            x2.append(float(p[2]))
                            if (self.radioButton_dens.isChecked()==True):
                                x2.append(float(p[1]))
                            if (self.radioButton_ph.isChecked()==True):
                                x2.append(float(p[2]))
                        xv1=np.array(x1)
                        xv2=np.array(x2)
                        
                        if self.fig==None:
                            self.rmmpl()
                            self.fig=Figure()
                            self.addmpl(self.fig)
                        self.fig.clear()
                        axf=self.fig.add_subplot(111)
                        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
                        axf.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                        if (self.radioButton_ph.isChecked()==True):
                            axf.set_xlim([-8.5,8.5])
                            axf.set_ylim(-4.,4.)
                            axf.plot(xv1,xv2)
                        if (self.radioButton_dens.isChecked()==True):
                            axf.fill_between(xv1,xv2,0.1,facecolor='black')
                            axf.set_ylim(0.,0.1)
                        axf.set_title('state at %s' %(i/10.))
                        self.canvas.draw()
            finally:
                os.chdir(prevdir)
            
    def close(self):
        self.hide()
        self.file.close()
        self.parent().show()
            
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.file.close()            
            event.accept()
        else:
            event.ignore()
 
class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home','Pan', 'Zoom', 'Save','Back','Forward')]
                 
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