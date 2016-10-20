# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:14:44 2016

@author: ivan
"""
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
import math
Ui_MainWindow,QMainWindow=loadUiType('Main.ui')

class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self)
        self.button1.clicked.connect(self.darkbutton)
        self.button2.clicked.connect(self.brightbutton)
        self.button3.clicked.connect(self.dispersionbutton)
        
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap('initial.png'))
        self.DS.setScene(scene)
    
        scene2=QGraphicsScene()        
        scene2.addPixmap(QPixmap('initialbs.png').scaled(141,91))
        self.BS.setScene(scene2)
    
        self.DS.show()
        
        self.eng.clicked.connect(self.english)
        self.spa.clicked.connect(self.spanish)
        
        if self.eng.isChecked()==False and self.spa.isChecked()==False:
            lang=open('language.txt','w')
            lang.write('1')   #english by default in case the user does not introduce a language        
            lang.close()
        
    def english(self):        
        lang=open('language.txt','w')
        lang.write('1')           
        lang.close()
    
    def spanish(self):        
        lang=open('language.txt','w')
        lang.write('2')           
        lang.close()
        
    def darkbutton(self):
        self.hide()
        self.dark_window = DS(self)
        self.dark_window.show()
        self.dark_window.raise_()
    
    def brightbutton(self):
        self.hide()
        self.bright_window = BS(self)
        self.bright_window.show()
        self.bright_window.raise_()   
        
    def dispersionbutton(self):
        self.hide()
        self.dispersion_window = WD(self)
        self.dispersion_window.show()
        self.dispersion_window.raise_()   
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
          
          
Ui_MainWindow,QMainWindow=loadUiType('DS.ui')
import os
import subprocess
import time

from PyQt4 import QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
class DS(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
#        self.mplfigs.hide()
#        self.mplwindow.hide()
        self.ButtonOn.hide()
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.interact.hide()
        self.interact_2.hide()
        self.interact_3.hide()
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
#        xv2=np.sqrt((42.-(0.5*xv**2.0))/(507.733))        
        
#        file=open('TF.txt','w')
#        for i in range(0,512):
#            file.write('%s\t%s\n' %(xv[i],xv2[i]))
#        file.close()
        self.fig=Figure()
        axf=self.fig.add_subplot(111)
        axf.set_xlabel('$x/a_{ho}$',fontsize=17)
        axf.set_ylabel('density $|\psi|^2$',fontsize=14)
        axf.plot(xv,xv1,label='Numerical solution')
#        axf.plot(xv,xv2**2, label='TF aproximation')
        axf.legend()
        axf.set_title('condensate')
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
                ax1f2.set_ylabel('density $|\psi|^2$',fontsize=14)
                ax1f2.plot(xv1,globals()['xv%s' %i])
                ax1f2.set_title('initial state')
                self.canvas.draw()

    def changefig(self,item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        self.fig=None
        
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


    def plot(self):
        self.sim +=1
        self.slider_simulation.setValue(self.sim)
        
        if (self.radioButton.isChecked()==True):
            if (self.sim==75):
                self.timer.stop()
        if (self.radioButton_2.isChecked()==True):
            if (self.sim==self.spinBox.value()*int((10*np.pi*np.sqrt(2.)))-1):
                self.timer.stop()
        if (self.radioButton_3.isChecked()==True):
            if (self.sim==self.spinBox_4.value()*int((10*np.pi*np.sqrt(2.)))-1):
                self.timer.stop()
            
    def plot2(self):
        self.sim -=1
        self.slider_simulation.setValue(self.sim)

        
        if (self.sim==1):
            self.timer.stop()
            
    def on(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot)
        self.timer.start(75)
    
    def pause(self):
        self.timer.stop()
        
    def back1(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot2)
        self.timer.start(75)


    def start1(self):
        if (self.radioButton.isChecked()==True):
            self.sim=0
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons'))
                file=open('input_2.txt','w')  
                file.write ('%s' %(self.spinBox_3.value()))
                file.close()
                subprocess.call('python gpe_fft_ts_LN_v1.py',shell=True)
                print (os.getcwd())
                print ("READY")
                self.label_5.show()
                self.ButtonOn.show()
                self.ButtonBack.show()
                self.ButtonPause.show()
                self.slider_simulation.show()
                self.slider_simulation.setMinimum(0)
                self.slider_simulation.setMaximum(74)
                self.slider_simulation.setSingleStep(1)
                self.slider_simulation.setValue(self.sim)
                file = open('lin.txt', 'r')
                lines = file.readlines()
                file.close()
            finally:
                os.chdir(prevdir)                
            x2 = []
            y2 = []
            for line in lines:
                p2 = line.split()
                x2.append(float(p2[1]))
                y2.append(float(p2[2]))
            xv2 = np.array(x2)
            yv2 = np.array(y2)
            fig1=Figure()
            ax1f1=fig1.add_subplot(111)
            ax1f1.set_ylabel('$\mu/hw$',fontsize=14)
            ax1f1.set_xlabel('$g_{int}$',fontsize=17)        
            ax1f1.plot(xv2,yv2, 'b.-')
            ax1f1.set_title('non-linear continuation')     
            self.delfig()
            self.addfig('CHEMICAL POTENTIAL',fig1)   
                
        if (self.radioButton_2.isChecked()==True) or (self.radioButton_3.isChecked()==True):
            self.sim=0
            if (self.radioButton_2.isChecked()==True):
                time=self.spinBox.value()*int((10*np.pi*np.sqrt(2.)))
            if (self.radioButton_3.isChecked()==True):
                time=self.spinBox_4.value()*int((10*np.pi*np.sqrt(2.)))
            psi_time=np.empty([512,time])
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons'))
                file=open('input.txt','w')  
                if (self.radioButton_2.isChecked()==True):
                    file.write ('%s\t%s\t%s' %(self.horizontalSlider.value()/10.0,self.spinBox.value(),self.spinBox_2.value()))
                if (self.radioButton_3.isChecked()==True):
                    file.write ('%s\t%s\t%s' %(self.horizontalSlider_2.value()/10.0,self.spinBox_4.value(),self.spinBox_5.value()*self.spinBox_6.value()*2))
                file.close()
                subprocess.call('python gpe_fft_ts_DS_v1.py',shell=True)
                print (os.getcwd())
                print ("READY")
                self.label_5.show()
                self.ButtonOn.show()
                self.ButtonBack.show()
                self.ButtonPause.show()
                self.slider_simulation.show()
                self.slider_simulation.setMinimum(0)
                if (self.radioButton_2.isChecked()==True):
                    self.slider_simulation.setMaximum(self.spinBox.value()*int((10*np.pi*np.sqrt(2.)))-1)
                if (self.radioButton_3.isChecked()==True):
                    self.slider_simulation.setMaximum(self.spinBox_4.value()*int((10*np.pi*np.sqrt(2.)))-1)
                self.slider_simulation.setSingleStep(1)
                self.slider_simulation.setValue(self.sim)
            
                file = open('energies.txt', 'r')
                lines = file.readlines()
                file.close()
                file2=open('phase.txt','r')
                lines2=file2.readlines()
                file2.close()
#                file3=open('min.txt','r')
#                lines3=file3.readlines()
#                file3.close()
                for i in range (1,time+1):
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
            
            fig3=Figure()
            ax1f3=fig3.add_subplot(111)
            ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
            ax1f3.set_xlabel('$T*w_{ho}$',fontsize=17)
            ax1f3.set_xlim(0,time-1)
            ax1f3.pcolor(range(0,time+1),xv1,psi_time, cmap='Greys_r')  # plot the particle denisity
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
            ax1f1.set_title('Phase difference produced by soliton')
          
    
    
            
            x1 = []
            y1 = []
            z1 = []
            for line in lines:
                p = line.split()
                x1.append(float(p[0]))
                y1.append(float(p[1]))
                z1.append(float(p[2]))                            
            xv = np.array(x1)
            yv = np.array(y1)
            zv = np.array(z1)
            
            fig2=Figure()
            ax1f2=fig2.add_subplot(121)
            ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)        
            ax1f2.set_ylabel('$E/hw$',fontsize=17)
            ax1f2.plot(xv,yv, 'b.-')
            ax1f2.set_title('Medium Energy')
            
            ax2f2=fig2.add_subplot(122)
            ax2f2.set_xlabel('$T/t_{ho}$',fontsize=17)
            ax2f2.plot(xv,zv, 'r.-')
            ax2f2.set_title('Chemical Potential')
           
            
            
#            x3 = []
#            y3 = []
#            for line in lines3:
#                p3 = line.split()
#                x3.append(float(p3[0]))
#                y3.append(float(p3[1]))
#            xv3 = np.array(x3)
#            yv3 = np.array(y3)
#            
#            fig3=Figure()
#            ax1f3=fig3.add_subplot(111)
#            ax1f3.set_xlabel('$T/t_{ho}$',fontsize=17)        
#            ax1f3.set_ylabel('$x/a_{ho}$',fontsize=17)
#            ax1f3.plot(xv3,yv3,'b.-')
#            ax1f3.set_title('Soliton Position')
    
            
            
            self.delfig()
            self.delfig()
            self.delfig()
            self.addfig('PHASE',fig1)
            self.addfig('ENERGY',fig2)
            self.addfig('MINUS',fig3)
        
                
    def simulation(self):
        if (self.radioButton.isChecked()==True):
            value=self.slider_simulation.value()
            time=74
            self.sim=value
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons'))
                for i in range(1,time+1):
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
                        axf.set_ylabel('density $|\psi|^2$',fontsize=14)
                        axf.plot(xv1,xv2)
                        axf.set_title('state at %s' %(i))
                        self.canvas.draw()
            finally:
                os.chdir(prevdir)
                
        if (self.radioButton_2.isChecked()==True) or (self.radioButton_3.isChecked()==True):
            if (self.radioButton_2.isChecked()==True):
                time=self.spinBox.value()*int((10*np.pi*np.sqrt(2.)))
            if (self.radioButton_3.isChecked()==True):
                time=self.spinBox_4.value()*int((10*np.pi*np.sqrt(2.)))
            value=self.slider_simulation.value()
            self.sim=value
            prevdir = os.getcwd()
            try:
                os.chdir(os.path.expanduser('./darksolitons'))
                for i in range(1,time+1):
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
                        axf.set_ylabel('density $|\psi|^2$',fontsize=14)
                        axf.plot(xv1,xv2)
                        axf.set_title('state at %s' %(i))
                        self.canvas.draw()
            finally:
                os.chdir(prevdir)
            
            
    def rmmpl(self):
        self.mplvl.removeWidget(self.toolbar)
        self.canvas.close()        
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        
                
    def close(self):
        self.hide()
        self.parent().show()
            
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
 
 
Ui_MainWindow,QMainWindow=loadUiType('BS.ui')
class BS(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        global language
        QtGui.QWidget.__init__(self,parent)
        lang=open('language.txt','r')
        lang2=lang.readlines()
        language=int(lang2[0])
        lang.close()
        self.setupUi(self)
        self.ButtonOn.hide() #amaguem tots els sliders o botons no necessaris pel moment
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.harm.hide() #seguim amagant coses no necessaries pel moment
        self.none.hide()
        self.info1.hide()
        self.wall.hide()
        self.label_5.hide()
        self.slider_simulation.hide()
        self.moment.hide()
        self.playmoment.hide()
        
        self.playmoment.clicked.connect(self.play2)
        
        self.slider_simulation.valueChanged.connect(self.simulation)
        self.ButtonOn.clicked.connect(self.on)
        self.ButtonBack.clicked.connect(self.backsim)
        self.ButtonPause.clicked.connect(self.pause)
        
        #let's give the possible values to sliders
        self.horizontalSlider_4.setMinimum(-60)
        self.horizontalSlider_4.setMaximum(-20)
        self.horizontalSlider_4.setSingleStep(1)
        self.horizontalSlider_4.TicksBelow
        
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
        figini.set_xlabel("Position ($x/a_{ho}$)")
        figini.set_ylabel("Density $|\psi|^2$")
        figini.set_title("An example of bright soliton")
        figini.plot(ax,aphi)
        self.addmpl(self.fig)        
        
        self.play_2.hide()
        self.play.hide()
        self.play.clicked.connect(self.juga)
        self.tanca.clicked.connect(self.torna)
        self.intenta.clicked.connect(self.grafica)
        
#        self.btn_none.clicked.connect(self.V_none)
#        self.btn_harm.clicked.connect(self.V_harm)
#        self.btn_wall.clicked.connect(self.V_wall)
        
        self.btn_none.clicked.connect(self.initial)
        self.btn_harm.clicked.connect(self.initial)
        self.btn_wall.clicked.connect(self.initial)

        self.fig_dict={}
        
        self.mplfigs.itemClicked.connect(self.changefig)

        self.start.clicked.connect(self.start2) #despres definirem start2 que ens dona les dades inicials
        self.back.clicked.connect(self.close)
        
    def initial(self):
        global language
        #let's show the initial state
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
        figini.set_xlabel("Position ($x/a_{ho}$)")
        figini.set_ylabel("Density $|\psi|^2$")
        figini.set_title("An example of bright soliton")
        figini.plot(ax,aphi)
        self.canvas.draw()
        
    def addmpl(self,fig):
        self.canvas=FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)        
        self.toolbar=NavigationToolbar(self.canvas,self.mpl_window,coordinates=True)
        self.mplvl.addWidget(self.toolbar)
        self.canvas.draw()
        
    def rmmpl(self,):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()
        
    def addmpl2(self,fig):
        self.canvas=FigureCanvas(fig)
        self.mplvl_2.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar=NavigationToolbar(self.canvas,self.mpl_window,coordinates=True)
        self.mplvl_2.addWidget(self.toolbar)
        
    def rmmpl2(self,):
        self.mplvl_2.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl_2.removeWidget(self.toolbar)
        self.toolbar.close()
        
    def addfig(self,name,fig):
        self.fig_dict[name]=fig
        self.mplfigs.addItem(name)
        
    def changefig(self,item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        self.fig=None
        
    def delfig(self):
        listItems=self.mplfigs.selectedItems()
        if not listItems: return
        for item in listItems:
            self.mplfigs.takeItem(self.mplfigs.row(item))
        
#    def V_none(self):
#        file_pot=open('pot_input.txt','w')
#        file_pot.write('%d' %(0))
#        file_pot.close()
                
#    def V_harm(self):
#        file_pot=open('pot_input.txt','w')
#        file_pot.write('%d' %(1))
#        file_pot.close()
                
#    def V_wall(self):
#        file_pot=open('pot_input.txt','w')
#        file_pot.write('%d' %(2))
#        file_pot.close()
                
    def start2(self):
        self.timer=QtCore.QTimer(self)
        self.sim=0
        global language
#        pot_file=open('pot_input.txt','r')
        prevdir=os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons'))
#            pot=int((pot_file.readlines())[0])
            if (self.btn_none.isChecked()==True):
                pot=0
            if (self.btn_harm.isChecked()==True):
                pot=1
            if (self.btn_wall.isChecked()==True):
                pot=2
            file_data=open('input.txt','w')
            self.slider_simulation.setValue(self.sim)
            if pot==0:           
                file_data.write('%d \t %d \t %f \t %f \t %d' %(0,self.gn.value(),self.horizontalSlider.value(),self.horizontalSlider_2.value(),self.yes_no.value()))
            elif pot==1:
                file_data.write('%d \t %d \t %f \t %d \t %d' %(1,self.gn.value(),self.horizontalSlider_3.value(),self.spinBox.value(),0))
            elif pot==2:
                file_data.write('%d \t %d \t %f \t %f \t %d \t %d \t %f' %(2,self.gn.value(),self.horizontalSlider_4.value(),self.horizontalSlider_5.value(),self.yes_no.value(),0.5*(2**self.wb.value()),self.hb.value()/10.0))
            file_data.close()
#            pot_file.close()
            subprocess.call('python gpe_bright_solitons.py',shell=True)
            self.ButtonOn.show() 
            self.ButtonBack.show()
            self.ButtonPause.show()
            self.slider_simulation.show()
            self.label_5.show()
            if pot==1:
                self.play.show()
            else:
                self.play.hide()
            if pot==0:
                self.playmoment.show()
            else:
                self.playmoment.hide()
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
        vmean=[]#mean velocity
        vrem=[] #mean velocity[t=i]- mean velocity[t=0]
        velm=[]
        for i in range(1,len(meanval)):
            tmv.append(float((meanval[i].split('\t'))[0]))
            mv.append(float((meanval[i].split('\t'))[1]))
            smv.append(float((meanval[i].split('\t'))[2]))
            vmean.append(float((meanval[i].split('\t'))[3]))
            vrem.append(float((meanval[i].split('\t'))[4]))
#            vvalue=(float((meanval[i].split('\t'))[5]))
#            velm.append(vvalue-float((meanval[1].split('\t'))[5]))
            velm.append(float((meanval[i].split('\t'))[5]))
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
            figmv.axes.set_ylim([-34.0,34.0])
        elif pot==2:
#            figmv.axes.errorbar(atmv,amv,yerr=asig)
            figmv.axes.errorbar(atmv,amv,yerr=sigsalt)
            figmv.axes.set_xlim([0,math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value()))])
            figmv.axes.set_ylim([-128.0,128.0])
        elif pot==0:
            figmv.plot(atmv,amv)
            figmv.axes.set_xlim([0,20.0])
            figmv.axes.set_ylim([-128.0,128.0])
        figmv.set_title("Position of the soliton")
        figmv.set_xlabel("Time ($t/ \omega$)")
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
        allenergies.set_xlabel("Time ($t/ \omega$)")
        allenergies.set_ylabel("Energy per particle ($E/ \hbar \omega$)")
        allenergies.legend()
        if pot==2:
            integrals=fig3.add_subplot(111)
            integrals.plot(atime,alint,label='left side')
            integrals.plot(atime,aiint,label='inside')
            integrals.plot(atime,arint,label='right side')
            integrals.set_xlabel("Time ($t/ \omega$)")
            integrals.set_title("Integrals of the wave function")
            integrals.legend()
        elif pot==1:    
            allenergies.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
            
        fig4=Figure()
        avelm=np.array(velm)
        meanvelocity=fig4.add_subplot(111)
        meanvelocity.plot(atmv,avelm)
        meanvelocity.set_title("Mean velocity of the soliton")
        meanvelocity.set_xlabel("Time ($t/ \omega$)")
        meanvelocity.set_ylabel("$\sqrt{<v^2>}$ ($v/ a_{ho} \omega$)")
        if pot==1:
            meanvelocity.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
            
        fig7=Figure()
        velpos=fig7.add_subplot(111)
        velpos.plot(amv,avelm)
        velpos.set_title("Velocity with position")
        velpos.set_xlabel("Position ($x/ a_{ho}$)")
        velpos.set_ylabel("$\sqrt{<v^2>}$ ($v/ a_{ho} \omega$)")
          
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
        
        if pot==0:
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(100)
            self.slider_simulation.setSingleStep(1)
        if pot==2:
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))
            self.slider_simulation.setSingleStep(1)
        else:
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(60*self.spinBox.value())
            self.slider_simulation.setSingleStep(1)
            
    def juga(self): #enables a window for play-plot
        global language
        self.rmmpl()
        self.mpl_window.hide()
        fig=Figure()
        self.addmpl2(fig)
        self.play_2.show()
       
    def torna(self): #hides the play-plot window and returns to normal plots
        global language        
        self.rmmpl2()
        self.play_2.hide()        
        fig=Figure()
        self.addmpl(fig)
        self.mpl_window.show()
        self.fig=None
        
    def grafica(self): #play-plot
        global language
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
        figmv.set_xlabel("Time ($t/ \omega$)")
        figmv.set_ylabel("Position ($x/ a_{ho}$)")
            
    def simulation(self):
        global language
#        pot_file=open('pot_input.txt','r')
        self.sim=self.slider_simulation.value()
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./brightsolitons/bs_evolution'))
#            pot=int((pot_file.readlines())[0])
#            pot_file.close()
            if (self.btn_none.isChecked()==True):
                pot=0
            if (self.btn_harm.isChecked()==True):
                pot=1
            if (self.btn_wall.isChecked()==True):
                pot=2
            if pot==0:
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
                        
                if self.fig==None:
                    self.rmmpl()
                    self.fig=Figure()
                    self.addmpl(self.fig)
                self.fig.clear()
                state=self.fig.add_subplot(111)
                state.set_xlabel("Position ($x/ a_{ho}$)")
                state.set_ylabel("Density $|\psi|^2$")
                state.plot(posit,phi2)
                state.plot(posit,pote,'g',label="Potential")
                state.plot(posit,confin,'g')
                state.set_ylim(0,0.3)
                if (self.yes_no.value()==1):
                    state.set_xlim(-100,100)
                else:
                    state.set_xlim(-128,128)
                state.legend()
                self.canvas.draw()
            elif pot==2:
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
                        
                if self.fig==None:
                    self.rmmpl()
                    self.fig=Figure()
                    self.addmpl(self.fig)
                self.fig.clear()
                state=self.fig.add_subplot(111)
                state.set_xlabel("Position ($x/ a_{ho}$)")
                state.set_ylabel("Density $|\psi|^2$")
                state.plot(posit,phi2)
                state.plot(posit,pote,'g',label="Potential")
                state.plot(posit,confin,'g')
                state.set_ylim(0,0.3)
                if (self.yes_no.value()==1):
                    state.set_xlim(-100,100)
                else:
                    state.set_xlim(-128,128)
                state.legend()
                self.canvas.draw()
            else:
                names=open("namefiles.dat",'r')
                listnames=names.readlines()
                name=int(listnames[int(self.slider_simulation.value())])
                data=open("WfBs-%08d.dat" %(name),'r')
                lines=data.readlines()
                listpos=[]
                listphi=[]
                listpot=[]
                for j in range(2,len(lines)):
                    listpos.append(float((lines[j].split('\t'))[0]))
                    listphi.append(float((lines[j].split('\t'))[1]))
                    listpot.append(float((lines[j].split('\t'))[5]))
                posit=np.array(listpos)
                phi2=np.array(listphi) 
                pote=np.array(listpot)
                if self.fig==None:
                    self.rmmpl()
                    self.fig=Figure()
                    self.addmpl(self.fig)
                self.fig.clear()
                state=self.fig.add_subplot(111)
                potential=state.twinx()
                state.plot(posit,phi2,'b')
                potential.plot(posit,pote,'g')
                state.set_xlabel("Position ($x/ a_{ho}$)")
                state.set_ylabel("Density $|\psi|^2$", color='b')
                potential.set_ylabel("Potential ($V/ \hbar \omega$)", color='g')
#                state.plot(posit,phi2)
#                state.plot(posit,pote,'g',label="Potential")
                state.set_xlim(self.horizontalSlider_3.value()-7,-self.horizontalSlider_3.value()+7)
                if self.gn.value()==1:
                    state.set_ylim(0,7.2)    
                elif self.gn.value()==2:
                    state.set_ylim(0,4)
                elif self.gn.value()==3:
                    state.set_ylim(0,2.2)
                self.canvas.draw()
        finally:
            os.chdir(prevdir)
                
    def on(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plotsim)
        self.timer.start(75)
        
    def backsim(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plotsim2)
        self.timer.start(75)
        
    def pause(self):
#        self.timer=QtCore.QTimer(self)   #it gives some problems
        self.timer.stop()
        
    def plotsim(self):
        self.sim=self.sim+1
        self.slider_simulation.setValue(self.sim)
        
        if (self.btn_none.isChecked()==True):
            if (self.sim==100):
                self.timer.stop()
        if (self.btn_harm.isChecked()==True):
            if (self.sim==(60*self.spinBox.value())):
                self.timer.stop()
        if (self.btn_wall.isChecked()==True):
            if (self.sim==(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))):
                self.timer.stop()
        
    def plotsim2(self):
        self.sim=self.sim-1
        self.slider_simulation.setValue(self.sim)
        
        if (self.sim==0):
            self.timer.stop()
            
    def play2(self):
        global language
        if language==1:
            self.expltext.setPlainText('Linear momentum \n \nLinear momentum is a derived quantity' + 
            ' from other magnitudes or properties from the particle we are working with; in '+
            'particular it is related with velocity following the relation:\n \n'+ '\t \t $\vect{p} = m \vect{v} $ \n \n'+
            'In this case here, we have the soliton confined in a box, so once the soliton hits a wall '+
            'it will go back as a ball hitting a wall would do.' + 'During this process, both energy and linear ' + 
            'momentum are conserved, so in the end we have (for the whole system) the same energy and total linear momentum.\n\n' +  'How can we '+
            'understand that? Imagine the previous example, we have two "particles": the ball (1) and the wall (2). '+
            'Imagine that the ball has a mass $m$ and the wall, as a normal wall, is still and cannot change its place. '+
            'In an ideal case, if you threw the ball against the wall with a velocity $v$ it would hit the wall and come back '+
            'to you with the same velocity module. This situation corresponds to an elastic collision, though it may not seem at '+
            "first sight, let's see how to understand it: \n \n"+'\t     \vect{p_{i,1}} + \vect{p_{i,2}} = \vect{p_{f,1}} '+
            '\vect{p_{f,2}}\n\n' + 'We can consider a wall with a very huge mass compared to the one of the ball (imagine it as infinity), so as we '+
            'see in our daily life, a wall hitted by a ball does not move, right? So we could suppose that the velocity of the wall '+
            'is both in the begining and end zero, and thus also the momentum.' + '\n\nSo taking into account the previous '+
            'equation we could think that momentum is not conserved because in one side we have the initial momentum and on the '+
            'other side we have the same value but negative (because the ball changed its direction to the opposed one), so the '+
            'equality would not be true.'+' However, this is a bit tricky, because '+
            'this is not what happens in reality: the wall really absorbes the momentum during the change, but as it has infinite '+
            'mass, the observer is not able to appreciate a change in the wall, so we assume v=0, but it is not true. Thus, we '+
            'can see that the momentum is conserved, with an absorption of momentum by the wall given by:\n\n '+
            '\t   $\Delta{vect{p_{wall}}}=2|vect{p_{i,wall}}}|=2|vect{p_{f,wall}}}|' + '\n\nGiven that we now know that '+
            'both momentum and energy are conserved, we can justify it is an elastic collision.' + 'You can go now to '+
            'the plots of energy and velocity to check that this is shown there, that both magnitudes are conserved.')
        if language==2:
            self.expltext.setPlainText('Momento lineal \n \nEl momento lineal es una cantidad derivada' + 
            ' de otras magnitudes o propiedades de la partícula con la que tratamos; concretamente '+
            'se la relaciona con la velocidad a través de la siguiente expresión:\n \n'+ '\t \t $\vect{p} = m \vect{v} $ \n \n'+
            'En este caso que tratamos aquí tenemos el solitón confinado en una pared, así, cuando el solitón '+ 
            'llega a la pared y choca contra ésta, rebota y sigue su camino en sentido contrario, tal y como esperaríamos que '+
            'hiciera una pelota al chocar contra una pared. Durante este proceso tanto la energía total como el momento lineal se '+
            'conservan, y por lo tanto presentan el mismo valor para el conjunto del sistema al inicio y al final del proceso .\n' +  '¿Como podemos '+
            'interpretar eso? Tomemos como ejemplo el caso expuesto sobre la pelota y la pared; en este caso tenemos '+
            'dos "partículas": la pelota (1) y la pared (2). Imaginemos ahora que la pelota tiene una masa $m$ '+
            'y la pared, como se espera, está quieta y no puede cambiar su posición. En un caso ideal, si lanzáramos una '+
            'pelota contra una pared con una velocidad $v$ ésta chocaría contra la pared y volvería hacia el lanzador con '+
            'una velocidad del mismo valor absoluto. Esta situación se corresponde con un choque elástico, aunque puede '+
            'no parecerlo a primeras, veámoslo mejor: \n \n'+'\t     \vect{p_{i,1}} + \vect{p_{i,2}} = \vect{p_{f,1}} '+
            '\vect{p_{f,2}}\n\n' + 'Podemos considerar una pared con una masa muy mayor a la de la pelota (incluso podemos '+
            'suponer que la pared presenta una masa infinita) y tal y como vemos en nuestro día a día aunque una pelota '+
            'golpee una pared, esta última no se mueve, con lo que tendríamos que la pared tiene velocidad cero, y por lo '+
            'tanto, su momento también es cero.'+ '\nConsiderando pues la anterior ecuación podríamos pensar que el momento '+
            'no se conserva puesto que en un lado tenemos el momento inicial y en el otro lado tenemos el mismo valor pero '+
            'cambiado de signo (porqué la pelota ha cambiado su sentido aunque no su dirección ni valor absoluto de velocidad), '+
            'y por lo tanto la igualdad ya no se cumpliría. No obstante, esto no es del todo cierto, porqué no es lo que sucede en '+
            'realidad: de hecho, la pared absorbe momento lineal durante el proceso, pero al tener una masa infinita, el observador no '+
            'se percaa del cambio tan pequeño en la velocidad y se asume $v=0$, aunque como se ha dicho no es estrictamente cierto. '+
            'Por lo tanto, el momento lineal se conserva, y la absorción de momento por parte de la pared viene dada por:\n\n '+
            '\t   $\Delta{vect{p_{wall}}}=2|vect{p_{i,wall}}}|=2|vect{p_{f,wall}}}|' + '\n\nAhora ya sabemos que tanto la energía '+
            'como el momento lineal se conservan, así que podemos afirmar que efectivamente se trata de un choque elástico. '+
            'Puedes ahora comprovar en los gráficos de energía y velocidad que la energía total se conserva y que el módulo de la '+
            'velocidad al inicio y al final (ambos lejos de la pared) son iguales.')
            
    def close(self):
        self.hide()
        self.parent().show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
                
Ui_MainWindow,QMainWindow=loadUiType('WD.ui')
class WD(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.ButtonBack.clicked.connect(self.back1)
        self.sim=0
        self.true1=0
        
        self.ButtonOn.hide()
        self.ButtonBack.hide()
        self.ButtonPause.hide()
        self.label_5.hide()

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
        self.fig=Figure()
        self.addmpl(self.fig)


    def start1(self):
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
            subprocess.call('python gpe_fft_ts_WP_v1.py',shell=True)
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
            self.slider_simulation.setValue(self.sim)
        
            file = open('energies.txt', 'r')
            lines = file.readlines()
            file.close()
            
            file2 = open('mean_value.txt','r')
            lines2 = file2.readlines()
            file2.close()

        finally:
            os.chdir(prevdir)
                    
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
        
        fig2=Figure()
        ax1f2=fig2.add_subplot(111)
        ax1f2.set_xlabel('$T/t_{ho}$',fontsize=17)        
        ax1f2.set_ylabel('$x/a_{ho}$',fontsize=17)
        ax1f2.plot(xv,yv, 'b.-',label='$R-Space$')
        ax1f2.plot(xv,iv, 'y.-',label='$k-Space$')
        ax1f2.legend()
        ax1f2.set_title('Mean value x')
        
        fig3=Figure()
        ax2f3=fig3.add_subplot(111)
        ax2f3.set_xlabel('$T/t_{ho}$',fontsize=17)
        ax2f3.set_ylabel('$(-)$',fontsize=17)
        ax2f3.plot(xv,zv, 'b.-',label='$R-Space$')
        ax2f3.plot(xv,jv, 'y.-',label='$k-Space$')
        ax2f3.legend()
        ax2f3.set_title('Mean value x dispersion')

        self.delfig()        
        self.delfig()
        self.delfig()
        self.addfig('ENERGY',fig)
        self.addfig('MEAN VALUE X',fig2)
        self.addfig('DISPERSION', fig3)
    
    def simulation(self):
        time=self.spinBox.value()*int((10*np.pi*2.0))-1
        value=self.slider_simulation.value()
        self.sim=value
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./Wavepackdisper'))
            for i in range(1,time+1):
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
                        self.fig=Figure()
                        self.addmpl(self.fig)
                    self.fig.clear()
                    axf=self.fig.add_subplot(111)
                    axf.set_xlabel('$x/a_{ho}$',fontsize=17)
                    axf.set_ylabel('density $|\psi|^2$',fontsize=14)
                    axf.plot(xv1,xv2,label='R-Space')
                    axf.plot(xv1,xv3,label='K-Space')
                    axf.set_title('state at %s' %(i))
                    axf.legend()
                    self.canvas.draw()
        finally:
            os.chdir(prevdir)
            
    def plot(self):
        self.sim +=1
        self.slider_simulation.setValue(self.sim)

        if (self.sim==self.spinBox.value()*int((10*np.pi*(2.))-1)):
            self.timer.stop()
        
    def plot2(self):
        self.sim -=1
        self.slider_simulation.setValue(self.sim)

        
        if (self.sim==1):
            self.timer.stop()
            
    def on(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot)
        self.timer.start(75)
    
    def pause(self):
        self.timer.stop()
        
    def back1(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot2)
        self.timer.start(75)
        
    def changefig(self,item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        self.fig=None
        
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
        self.canvas.close()        
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        
    def close(self):
        self.hide()
        self.parent().show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
if __name__=='__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np
    
    
    app=QtGui.QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec_())
