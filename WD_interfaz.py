# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:02:58 2016

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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from PyQt4 import QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT)
import time
pause_spr = False
on_spr = True
back_spr = False  
Ui_MainWindow,QMainWindow=loadUiType('WD.ui')
class WD(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.file=open('output.txt','a')
        self.ButtonBack.clicked.connect(self.back1)
        self.radioButton.setChecked(True)
        self.sim=0
        self.true1=0
        
        self.ButtonOn.hide()
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.label_5.hide()
        self.interact_game.hide()
        self.game.hide()
        
        self.start.clicked.connect(self.start1)
        self.back.clicked.connect(self.close)
        self.ButtonOn.clicked.connect(self.on)
        
        self.ButtonPause.clicked.connect(self.pause)        
        self.fig_dict={}
        
        self.slider_simulation.hide()
#        self.horizontalSlider.valueChanged.connect(self.initial)
        self.slider_simulation.valueChanged.connect(self.simulation)
        self.fig_dict={}
        self.mplfigs.itemClicked.connect(self.changefig)
        self.fig=plt.figure()
        self.addmpl(self.fig)
        
        self.pushButton_game.clicked.connect(self.game_call)
        self.pushButton_try.clicked.connect(self.graph_try)
        self.pushButton_return.clicked.connect(self.game_return)
        self.mplwindow_2.hide()
        
        self.timer1=QtCore.QTimer(self)
        self.timer2=QtCore.QTimer(self)
        
        self.ani_co=0
        

    def start1(self):
        self.timer1.stop()
        self.timer2.stop()
        dialog = QtGui.QDialog()    
        progressBar = Ui_porcessProgress()
        progressBar.setupUi(dialog)
        dialog.show()
        self.file.write('...Nuevo proceso...\n')
        diff = 0
        self.sim=0
        self.true1=0
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./Wavepackdisper'))
            file=open('input.txt','w')  
            if (self.radioButton.isChecked()==True):
                self.true1=1
            if (self.radioButton_2.isChecked()==True):
                self.true1=0
            file.write ('%s\t%s\t%s\t%s' %(self.horizontalSlider.value(),self.true1,self.spinBox.value(),self.spinBox_2.value()))
            file.close()
            
            time1=self.spinBox.value()*int((10*np.pi*2.0))-1
            start_sub=time.time()
            subprocess.Popen('python gpe_fft_ts_WP_v1.py',shell=True)
            for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        if file.startswith("WfWd"):
                             os.remove((os.path.join(root, file)))
                             
            progressBar.porcessProgressBar.setMaximum(time1)
            diff=0
            while diff<time1+1:
                diff=0
                for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        if file.startswith("WfWd"):
                            diff +=1
                    
                    if (diff<10):
                        progressBar.label.setText('Initiation of the progress...')
                    if (diff<time1-10) and (diff>10):
                        progressBar.label.setText('Solving Schrodinger equation...')
                    if (diff<time1) and (diff>time1-10):
                        progressBar.label.setText('Writing results ...')
                                            
                    progressBar.porcessProgressBar.setValue(diff)                     
                    QApplication.processEvents()
                        
            if (self.true1==1):
                self.file.write('Posición inicial del paquete de ondas=%s\nPotential armónico: YES\nExcitación del estado=%s\nNúmero de oscilaciones=%s\n\n' %(self.horizontalSlider.value(),self.spinBox_2.value(),self.spinBox.value()))
            if (self.true1==0):
                self.file.write('Posición inicial del paquete de ondas=%s\nPotential armónico: NO\nExcitación del estado=%s\nNúmero de oscilaciones=%s\n\n' %(self.horizontalSlider.value(),self.spinBox_2.value(),self.spinBox.value()))
            end_sub=time.time()            
            print (os.getcwd())
            print ("READY")
            self.label_5.show()
            self.ButtonOn.show()
            self.ButtonBack.show()
            self.ButtonPause.show()
            self.label_5.show()
            self.slider_simulation.show()
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(self.spinBox.value()*int((10*np.pi*2.0))-1)
            self.slider_simulation.setSingleStep(1)
            if (self.radioButton.isChecked()==True):
                self.interact_game.show()
                self.radioButton_oscil.setChecked(True)
            if (self.radioButton_2.isChecked()==True):
                self.interact_game.hide()
            time.sleep(2)
            
            file=open('output_sp.txt','r')
            self.file.write('%s\n' %file.read())
            self.file.write('Durada de la computación=%s\n\n' %(end_sub-start_sub))
            
            file = open('energies.txt', 'r')
            lines = file.readlines()
            file.close()
            
            file2 = open('mean_value.txt','r')
            lines2 = file2.readlines()
            file2.close()
            
            file4=open('WfWd-%08d.txt'%(0),'r')
            lines4=file4.readlines()
            file4.close()

        finally:
            os.chdir(prevdir)
            
        x1=[]
        x2=[]
        x3=[]
        for line in lines4:
            p=line.split()
            x1.append(float(p[0]))
            x2.append(float(p[1]))
            x3.append(float(p[5]))
        xv1=np.array(x1)
        xv2=np.array(x2)
        xv3=np.array(x3)
        
        
        self.rmmpl()
        self.fig=plt.figure()
        axf=self.fig.add_subplot(111)
        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
        axf.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
        axf.fill_between(xv1,0,xv2,label='$R-Space$',facecolor='blue',alpha=0.5)
        axf.fill_between(xv1,0,xv3,label='$K-Space$',facecolor='yellow',alpha=0.5)
        axf.set_xlim([-20,20])
        if (self.true1==0):
            axf.set_ylim(0,0.6)
        axf.set_title('state at %s' %(0))
        axf.legend()
        self.addmpl(self.fig)
        
 
        x1 = []
        y1 = []
        z1 = []
        j1 = []
        for line in lines:
            p = line.split()
            x1.append(float(p[0]))
            y1.append(float(p[1]))
            z1.append(float(p[3]))
            j1.append(float(p[4]))                            
        xv = np.array(x1)
        yv = np.array(y1)
        zv = np.array(z1)
        jv=np.array(j1)
        
        fig=Figure()
        ax1f1=fig.add_subplot(111)
        ax1f1.set_xlabel('$T/t_{ho}$',fontsize=17)        
        ax1f1.set_ylabel('$E/hw$',fontsize=17)
        ax1f1.plot(xv,yv,'r.-',label='$E_{tot}$')
        ax1f1.plot(xv,zv,'y.-',label='Kinetic Energy')
        ax1f1.plot(xv,jv,'b.-',label='Potential Energy')
        ax1f1.legend()
        ax1f1.set_title('Energies')
        
        
    
        x1 = []
        y1 = []
        z1 = []
        i1 = []
        j1 = []
        for line in lines2:
            p = line.split()
            x1.append(float(p[0]))
            y1.append(float(p[1]))
            z1.append(float(p[2]))  
            i1.append(float(p[3]))
            j1.append(float(p[4]))                          
        xv = np.array(x1)
        yv = np.array(y1)
        zv = np.array(z1)
        iv = np.array(i1)
        jv = np.array(j1)
        
        self.fig2=Figure()
        ax1f2=self.fig2.add_subplot(111)
        ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)        
        ax1f2.set_ylabel('$x/a_{ho}$',fontsize=17)
        ax1f2.plot(xv,yv, 'b.',label='$R-Space:<x> $')
        ax1f2.plot(xv,iv, 'y--',label='$k-Space:<k>$')
        ax1f2.plot(xv,zv, 'b--',label='$R-Space:dispersion$')
        ax1f2.plot(xv,jv, 'y.',label='$k-Space:dispersion$')

        ax1f2.legend(loc='best')
        
        self.delfig()        
        self.delfig()
        self.delfig()
        self.addfig('ENERGY',fig)
        self.addfig('MEAN VALUE X',self.fig2)
        self.slider_simulation.setValue(0)
        
    def simulation(self):
        time1=self.spinBox.value()*int((10*np.pi*2.0))-1
        value=self.slider_simulation.value()
        self.sim=value
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./Wavepackdisper'))
            for i in range(0,time1+1):
                file=open('WfWd-%08d.txt'%(i),'r')
                globals()['lines%s' %i]=file.readlines()
                file.close()
#            
#            
                if value==i:                    
                    x1=[]
                    x2=[]
                    x3=[]
                    for line in (globals()['lines%s' %i]):
                        p=line.split()
                        x1.append(float(p[0]))
                        x2.append(float(p[1]))
                        x3.append(float(p[5]))
                    xv1=np.array(x1)
                    xv2=np.array(x2)
                    xv3=np.array(x3)
                    
                    
                    if self.fig==None:
                        self.rmmpl()
                        self.fig=plt.figure()
                        self.addmpl(self.fig)
                    self.fig.clear()
                    axf=self.fig.add_subplot(111)
                    axf.set_xlabel('$x/a_{ho}$',fontsize=17)
                    axf.set_ylabel('density $|\psi|^2/a_{ho}$',fontsize=14)
                    axf.fill_between(xv1,0,xv2,label='$R-Space$',facecolor='blue',alpha=0.5)
                    axf.fill_between(xv1,0,xv3,label='$K-Space$',facecolor='yellow',alpha=0.5)
                    axf.set_xlim([-20,20])
                    if (self.true1==0):
                        axf.set_ylim(0,0.6)
                    axf.set_title('state at %s' %(i))
                    axf.legend()
                    self.canvas.draw()
        finally:
            os.chdir(prevdir)
    
    def game_call(self):
        self.timer1.stop()
        self.timer2.stop()
        if (self.radioButton.isChecked()==True):
            
            if (self.radioButton_oscil.isChecked()==True):
                self.rmmpl()
                self.textBrowser.show()
                self.rmmpl2()
                self.mplwindow.hide()
                self.widget_osci.show()
                self.start.hide()
                self.mplfigs.hide()
                self.spin_amplitude.setValue(3.)
                self.spin_frequency.setValue(0.5)
                prevdir = os.getcwd()
                try:
                    os.chdir(os.path.expanduser('./Wavepackdisper'))
                    file2 = open('mean_value.txt','r')
                    lines2 = file2.readlines()
                    file2.close()
                    x1 = []
                    y1 = []
                    for line in lines2:
                        p = line.split()
                        x1.append(float(p[0]))
                        y1.append(float(p[1]))                        
                    xv = np.array(x1)
                    yv = np.array(y1)
                finally:
                    os.chdir(prevdir)
                fig3=Figure()
                ax1f3=fig3.add_subplot(111)
                ax1f3.set_xlabel('$T/t_{ho}$',fontsize=17)        
                ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
                ax1f3.plot(xv,yv, 'r.-',label='$R-Space$')                
                ax1f3.set_title('Mean value x')
                ax1f3.legend()
                self.addmpl2(fig3)

        self.game.show()
        self.mplwindow_2.show()
        
    def graph_try(self):
        if (self.radioButton.isChecked()==True):
            if (self.radioButton_oscil.isChecked()==True):
                self.ani_co += 1
                if self.ani_co>1:
                    self.ani.event_source.stop()
                time1=self.spinBox.value()*int((10*np.pi*2.0))-1
                self.rmmpl2()
                prevdir = os.getcwd()
                try:
                    os.chdir(os.path.expanduser('./Wavepackdisper'))
                    file2 = open('mean_value.txt','r')
                    lines2 = file2.readlines()
                    file2.close()
                    x1 = []
                    y1 = []
                    for line in lines2:
                        p = line.split()
                        x1.append(float(p[0]))
                        y1.append(float(p[1]))                        
                    xv = np.array(x1)
                    yv = np.array(y1)
                finally:
                    os.chdir(prevdir)
                
#                fig3=Figure()
#                self.addmpl2(fig3)
#                ax1f3=fig3.add_subplot(111)
#                ax1f3.set_xlabel('$T/t_{ho}$',fontsize=17)        
#                ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
#                
#                x=np.arange(0,time1+1)/10.
#                y=self.spin_amplitude.value()*np.cos(self.spin_frequency.value()*x)
#                
#                ax1f3.plot(xv,yv, 'r.-',label='$R-Space$')                
#                ax1f3.plot(x,y)            
#                ax1f3.set_title('Mean value x')
#                ax1f3.legend()
#                self.canvas.draw()
                
                tf_sim =  time1/10.
                def simData():
                    L=self.spin_amplitude.value()
                    t_max =  time1/10.
                    dt = 0.05
                    w = self.spin_frequency.value()
                    y = 0.0
                    t = 0.0
                    while t <= t_max and t >= 0:
                        if on_spr and not back_spr and not pause_spr:
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
                        ori = -self.spin_amplitude.value()-1.
                    if self.spin_amplitude.value()<=0:
                        ori = self.spin_amplitude.value()-1.
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
                ax = plt.subplot2grid((10,10), (0,0), rowspan=10, colspan=2, autoscale_on=False, xlim=(-0.5, 0.5), ylim=(-self.spin_amplitude.value()-2., +self.spin_amplitude.value()+2.))
                ax2 = plt.subplot2grid((10,10), (0,3), rowspan=10, colspan=7, autoscale_on=False, xlim=(0., tf_sim), ylim=(-self.spin_amplitude.value()-2., +self.spin_amplitude.value()+2.))
#                ax = fig3.add_subplot(121)   
#                ax2 = fig3.add_subplot(122)
                ax.set_title('Muelle')
                ax.set_xticks(np.arange(-1., 2., 1.))
                ax.set_xlim(-1,1)
                if self.spin_amplitude.value()>=0:
                    ax.set_ylim(-self.spin_amplitude.value()-2.,self.spin_amplitude.value()+2.)
                if self.spin_amplitude.value()<=0:
                    ax.set_ylim(self.spin_amplitude.value()-2.,-self.spin_amplitude.value()+2.)
                
                
                ax2.set_xlabel('t(s)',fontsize=13)        
                ax2.set_ylabel('x(m)',fontsize=13)
                ax2.plot(xv,yv, 'r.-')                
                ax2.set_title('Mean value x')
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
    def game_return(self):
        self.rmmpl2()
        self.rmmpl2()
        self.mplwindow_2.hide()
        self.game.hide()
        self.fig=plt.figure()
        self.addmpl(self.fig)
        self.mplwindow.show()
        self.start.show()
        self.mplfigs.show()
        
    def plot(self):
        self.sim +=1
        self.slider_simulation.setValue(self.sim)
        
        if (self.sim==self.spinBox.value()*int((10*np.pi*(2.))-1)):
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
        
    def close(self):
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
