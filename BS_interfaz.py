# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:02:05 2016

@author: laura18
"""

import os, glob
import subprocess

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
#from matplotlib._png import read_png
import matplotlib.image as mpimg
#from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

from PyQt4 import QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
#from matplotlib.cbook import get_sample_data

import time
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
        figini.set_xlabel("Position ($x/ \\xi$)")
        figini.set_ylabel("Density $|\psi|^2 \\xi$")
        figini.set_title("An example of bright soliton")
        figini.plot(ax,aphi)
        self.addmpl(self.fig)
        
        self.play_2.hide()
        self.play.hide()
        self.play.clicked.connect(self.juga)
        self.tanca.clicked.connect(self.torna)
        self.intenta.clicked.connect(self.grafica)
        
        self.horizontalSlider.valueChanged.connect(self.escriu2x)
        self.horizontalSlider_2.valueChanged.connect(self.escriu2v)
        
        self.btn_none.clicked.connect(self.initial)
        self.btn_harm.clicked.connect(self.initial)
        self.btn_wall.clicked.connect(self.initial)
        
#        if self.btn_none.isChecked()==True:
#            self.setWindowTitle("Bright solitons laboratory: Free bright solitons")
#        elif self.btn_harm.isChecked()==True:
#            self.setWindowTitle("Bright solitons laboratory: Solitons under an harmonic trap")
#        elif self.btn_wall.isChecked()==True:
#            self.setWindowTitle("Bright solitons laboratory: Solitons through a barrier")
        
        self.horizontalSlider_2.setSingleStep(2)

        self.fig_dict={}
        
        self.mplfigs.itemClicked.connect(self.changefig)

        self.start.clicked.connect(self.start2) #despres definirem start2 que ens dona les dades inicials
        self.back.clicked.connect(self.close)
        
    def escriu2x(self):
        self.valor_x0_none.setNum(2*self.horizontalSlider.value())
        
    def escriu2v(self):
        self.valor_v0_none.setNum(2*self.horizontalSlider_2.value())
        
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
        figini.set_xlabel("Position ($x/ \\xi $)")
        figini.set_ylabel("Density $|\psi|^2 \\xi$")
        figini.set_title("An example of bright soliton")
        figini.plot(ax,aphi)
        self.canvas.draw()
        self.slider_simulation.hide()
        self.ButtonOn.hide()
        self.ButtonBack.hide()
   #     self.ButtonPause.click()
        self.ButtonPause.hide()
        self.value_sim.hide()
        self.label_5.hide()
        
    def addmpl(self,fig):
        self.canvas=FigureCanvas(fig)
        self.toolbar=NavigationToolbar(self.canvas,self.mpl_window,coordinates=True)
        self.mplvl.addWidget(self.toolbar)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw() 
        
    def rmmpl(self,):        
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        
    def addmpl2(self,fig):
        self.canvas=FigureCanvas(fig)
        self.toolbar=NavigationToolbar(self.canvas,self.mpl_window,coordinates=True)
        self.mplvl_2.addWidget(self.toolbar)
        self.mplvl_2.addWidget(self.canvas)
        self.canvas.draw()        
        
    def rmmpl2(self,):
        self.mplvl_2.removeWidget(self.toolbar)
        self.toolbar.close()
        self.mplvl_2.removeWidget(self.canvas)
        self.canvas.close()       
        
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
        
    def start2(self):
        self.timer=QtCore.QTimer(self)
        self.sim=0
        
        #let's show the progress bar
        dialog = QtGui.QDialog()    
        progressBar = Ui_porcessProgress()
        progressBar.setupUi(dialog)
        dialog.show()
        diff = 0
        
        global language
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
            if (self.btn_harm.isChecked()==True):
                pot=1
            if (self.btn_wall.isChecked()==True):
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
            if pot==0:           
                file_data.write('%d \t %d \t %f \t %f \t %d \t %f' %(0,self.gn.value(),self.horizontalSlider.value()*2.0,self.horizontalSlider_2.value()*2.0,self.yes_no.value(),tempss))
            elif pot==1:
                file_data.write('%d \t %d \t %f \t %d \t %d' %(1,self.gn.value(),self.horizontalSlider_3.value(),self.spinBox.value(),0))
            elif pot==2:
                file_data.write('%d \t %d \t %f \t %f \t %d \t %d \t %f \t %f' %(2,self.gn.value(),self.horizontalSlider_4.value(),self.horizontalSlider_5.value(),self.yes_no.value(),0.5*(2**self.wb.value()),self.hb.value()/10.0, tempss))
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
                            progressBar.label.setText(u'Starting with Schrödinger equation...')
                        if (diff<time1-10) and (diff>10):
                            progressBar.label.setText('Evolution in real time in progress...')
                        if (diff<time1) and (diff>time1-10):
                            progressBar.label.setText('Writing results ...')
                        progressBar.porcessProgressBar.setValue(diff)                     
                        QApplication.processEvents()
                os.chdir(prev)
                    
            if (self.btn_harm.isChecked()==True):
  #              if self.spinBox.value()==1 or self.spinBox.value()==2:
  #                  time1=60*self.spinBox.value()+1
  #              elif self.spinBox.value()==3:
  #                  time1=201
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
                            progressBar.label.setText(u'Starting with Schrödinger equation...')
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
                            progressBar.label.setText(u'Starting with Schrödinger equation...')
                        if (diff<time1-10) and (diff>10):
                            progressBar.label.setText('Evolution in real time in progress...')
                        if (diff<time1) and (diff>time1-10):
                            progressBar.label.setText('Writing results ...')
                        progressBar.porcessProgressBar.setValue(diff)                     
                        QApplication.processEvents()
                os.chdir(prev)
            
            time.sleep(2)
            
            self.ButtonOn.show() 
            self.ButtonBack.show()
            self.ButtonPause.show()
            self.slider_simulation.show()
            self.label_5.show()
            self.value_sim.show()
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
       #     figmv.axes.set_xlim([0,math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value()))])
            figmv.axes.set_ylim([-128.0,128.0])
        elif pot==0:
            figmv.plot(atmv,amv)
       #     figmv.axes.set_xlim([0,20.0])
            figmv.axes.set_ylim([-128.0,128.0])
        figmv.set_title("Position of the soliton")
        if pot==0 or pot==2:
            figmv.set_xlabel("Time ($t$  $ {\hbar}/({m \\xi^2})$)")
            figmv.set_ylabel("Position ($x/ \\xi$)")
        elif pot==1:
            figmv.set_xlabel("Time ($t/ \omega_{ho}$)")
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
        if pot==0 or pot==1:
            allenergies.set_xlabel("Time ($t $  ${\hbar}/({m \\xi^2})$)")
            allenergies.set_ylabel("Energy per particle ($E $  $({m \\xi^2})/{\hbar^2}$)")
        elif pot==1:
            allenergies.set_xlabel("Time ($t/ \omega_{ho}$)")
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
        if pot==0 or pot==1:
            meanvelocity.set_xlabel("Time ($t $  ${\hbar}/({m \\xi^2})$)")
            meanvelocity.set_ylabel("$\sqrt{<v^2>}$ ($v $  ${m \\xi}/{\hbar}$)")
        elif pot==1:
            meanvelocity.set_xlabel("Time ($t/ \omega$)")
            meanvelocity.set_ylabel("$\sqrt{<v^2>}$ ($v/ a_{ho} \omega$)")
            meanvelocity.axes.set_xlim([0,2*np.pi*self.spinBox.value()])
            
        fig7=Figure()       #only for harmonic potential
        velpos=fig7.add_subplot(111)
        velpos.plot(amv,avelm)
        velpos.set_title("$<|v|>$ with $<x>$")
        velpos.set_xlabel("Position ($x/ a_{ho}$)")
        velpos.set_ylabel("$\sqrt{<v^2>}$ ($v/ a_{ho} \omega_{ho}$)")
          
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
      #      if self.wall_1.isChecked()==True:
      #          self.slider_simulation.setMaximum(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))
      #      elif self.wall_2.isChecked()==True:
      #          self.slider_simulation.setMaximum(10*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))
      #      else:
      #          self.slider_simulation.setMaximum(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))            
            self.slider_simulation.setMaximum(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))            
            self.slider_simulation.setSingleStep(1)
        else:
            self.slider_simulation.setMinimum(0)
            self.slider_simulation.setMaximum(60*self.spinBox.value())
            self.slider_simulation.setSingleStep(1)
            
        self.slider_simulation.setValue(0)
            
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
        figmv.set_title("Position of the soliton")
        figmv.set_xlabel("Time ($t/ \omega_{ho}$)")
        figmv.set_ylabel("Position ($x/ a_{ho}$)")
            
    def simulation(self):
        global language
        self.sim=self.slider_simulation.value()
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser("./brightsolitons/bs_evolution"))
            datener=open('energies.dat','r')
            linener=datener.readlines()
            epart=float((linener[1].split('\t'))[1]) #as total energy is cte, we take the first one
            if (self.btn_none.isChecked()==True):
                pot=0
            if (self.btn_harm.isChecked()==True):
                pot=1
            if (self.btn_wall.isChecked()==True):
                pot=2
            if pot==0:
                if self.none_20.isChecked()==True:
                    i=self.slider_simulation.value()*200
                elif self.none_40.isChecked()==True:
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
                
                if (self.yes_no.value()==1): #soliton in a box
                    if self.fig==None:
                        self.rmmpl()
                        self.fig=Figure()
                        self.addmpl(self.fig)
                    self.fig.clear()
                    gs=GridSpec(8,1)  #7 rows and 1 column
                    state=self.fig.add_subplot(gs[0:6,:])
                    wave=self.fig.add_subplot(gs[6:8,:])
             #       state=self.fig.add_subplot(111)
             #       wave=plt.subplot2grid((3,3),(0,0),rowspan=1,colspan=3,autoscale_on=False,xlim=(-100,100),ylim=(-1,1))
             #       state=plt.subplot2grid((3,3),(1,0),rowspan=2,colspan=3,autoscale_on=False,xlim=(-100,100),ylim=(0,0.3))                    
                    wave.set_xlabel("Position ($x/ \\xi$)")
                    state.set_ylabel("Density $|\psi|^2 \\xi$")
                    state.plot(posit,phi2)
                    state.fill_between(posit,phi2,0,facecolor='0.80')
                    state.plot(posit,pote,'g',label="Potential")
                    state.plot(posit,confin,'g')
                    state.set_ylim(0,0.3)
                    state.set_xlim(-120,120)
                    wave.set_xlim(-120,120)
                    state.axes.get_xaxis().set_visible(False)
                    wave.axes.get_yaxis().set_visible(False)                    
                    
                    state.legend()
                    
                    #let's plot the wave on the string
                    Nini=10.0*(2.0*self.horizontalSlider.value()+50.0)
                    Nnow=int(Nini + (i/100.0)*self.horizontalSlider_2.value()*2.0) #for any time (t=20 or t=40)
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
                
                elif (self.yes_no.value()==0): #soliton in a ring                                           
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
                    state.set_ylim(0,0.3)
                    state.set_xlim(-128,128)
                    state.legend()
                    self.canvas.draw()
                    
            elif pot==2:
           #     i=self.slider_simulation.value()*200
           #     data=open("WfBs-%08d.dat" %(i),'r')
                names=open("namefiles.dat",'r')
                listnames=names.readlines()
                name=int(listnames[int(self.slider_simulation.value())])
                data=open("WfBs-%08d.dat" %(name),'r')
                lines=data.readlines()
                listpos=[]
                listphi=[]
                listpot=[]
                listconf=[]
                listtote=[]
                for j in range(2,len(lines)):
                    listpos.append(float((lines[j].split('\t'))[0]))
                    listphi.append(float((lines[j].split('\t'))[1]))
                    listpot.append(float((lines[j].split('\t'))[5]))
                    listconf.append(float((lines[j].split('\t'))[6]))
                    listtote.append(epart)
                posit=np.array(listpos)
                phi2=np.array(listphi)
                pote=np.array(listpot)
                tote=np.array(listtote)
                confin=np.array(listconf)
                        
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
                potential=state.twinx()
                potential.plot(posit,pote,'g')
                potential.plot(posit,tote,'r', label='$E_{total}$') #in red the total energy
                potential.legend()
                potential.set_ylim(bottom=0)
                state.plot(posit,confin,'g')
                potential.set_ylabel("Potential ($V $  ${m \\xi^2}/{\hbar^2}$)", color='g')
                state.set_ylim(0,0.3)
                if (self.yes_no.value()==1):
                    state.set_xlim(-100,100)
                else:
                    state.set_xlim(-128,128)
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
                state.set_ylabel("Density $|\psi|^2 \a_{ho}$", color='b')
                potential.set_ylabel("Potential ($V/ \hbar \omega_{ho}$)", color='g')
                potential.set_ylim(0,0.5*(np.abs(self.horizontalSlider_3.value())+7)**2)
                if (self.horizontalSlider_3.value() <= 0):
                    state.set_xlim(self.horizontalSlider_3.value()-7,-self.horizontalSlider_3.value()+7)
                elif (self.horizontalSlider_3.value() > 0):
                    state.set_xlim(-self.horizontalSlider_3.value()-7,self.horizontalSlider_3.value()+7)
                if self.gn.value()==1:
                    state.set_ylim(0,7.2)    
                elif self.gn.value()==2:
                    state.set_ylim(0,4)
                elif self.gn.value()==3:
                    state.set_ylim(0,2.2)
                self.canvas.draw()
        finally:
            os.chdir(prevdir)
            
#        print os.getcwd()   correct
                
    def on(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plotsim)
        self.timer.start(25)
     #   self.ext_potential.hide()
     #   self.Confinement.hide()
     #   self.interaction.hide()
        
    def backsim(self):
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.plotsim2)
        self.timer.start(25)
     #   self.ext_potential.hide()
     #   self.Confinement.hide()
     #   self.interaction.hide()
        
    def pause(self):
#        self.timer=QtCore.QTimer(self)   #it gives some problems
        self.timer.stop()
     #   self.ext_potential.show()
     #   self.Confinement.show()
     #   self.interaction.show()
        
    def plotsim(self):
        self.sim=self.sim+1
        self.slider_simulation.setValue(self.sim)
        
        if (self.btn_none.isChecked()==True):
            if (self.sim==100):
                self.timer.stop()
     #           self.ButtonPause.click()
        if (self.btn_harm.isChecked()==True):
       #     if (self.spinBox.value()==1) or (self.spinBox.value()==2):
       #         if (self.sim==(60*self.spinBox.value())):
       #             self.timer.stop()
       #     elif (self.spinBox.value()==3):
       #         if (self.sim==200):
       #             self.timer.stop()
            if (self.sim==(60*self.spinBox.value())):
                    self.timer.stop()
     #               self.ButtonPause.click()
        if (self.btn_wall.isChecked()==True):
            if self.wall_1.isChecked()==True:
                if (self.sim==(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))):
                    self.timer.stop()
     #               self.ButtonPause.click()
            elif self.wall_2.isChecked()==True:
                if (self.sim==(10*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))):
                    self.timer.stop()
     #               self.ButtonPause.click()
            else:
                if (self.sim==(5*math.ceil(-2.0*self.horizontalSlider_4.value()/float(self.horizontalSlider_5.value())))):
                    self.timer.stop()
     #               self.ButtonPause.click()
        
    def plotsim2(self):
        self.sim=self.sim-1
        self.slider_simulation.setValue(self.sim)
        
        if (self.sim==0):
            self.timer.stop()
     #       self.ButtonPause.click()
            
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
            "first sight, let's see how to understand it: \n \n"+r"\t    $ \vect{p_{i,1}} + \vect{p_{i,2}} = \vect{p_{f,1}} $"+
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
