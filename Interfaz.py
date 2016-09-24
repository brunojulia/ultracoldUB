# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:14:44 2016

@author: ivan
"""

from PyQt4.uic import loadUiType
Ui_MainWindow,QMainWindow=loadUiType('window.ui')
import os
import subprocess
import time

from PyQt4 import QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self)
        self.mplfigs.hide()
        self.mplwindow.hide()
        self.interact.hide()
        self.button=QtGui.QPushButton('DARK SOLITONS',self)
        self.button.clicked.connect(self.darksoliton)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)
        self.start.clicked.connect(self.start1)
        
        self.fig_dict={}
        
        self.mplfigs.itemClicked.connect(self.changefig)
        
        fig=Figure()
        self.addmpl(fig)
        
        
    
    def changefig(self,item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[str(text)])
        
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
   
    def darksoliton(self):
        self.interact.show()
        self.button.hide()
        
    def start1(self):
        prevdir = os.getcwd()
        try:
            os.chdir(os.path.expanduser('./darksolitons'))
            file=open('input.txt','w')  
            file.write ('%s\t%s' %(self.horizontalSlider.value(),self.spinBox.value()))
            file.close()
            subprocess.Popen('python gpe_fft_ts_DS_v1.py',shell=True)
            print os.getcwd()
            time.sleep(15.0*self.spinBox.value())
            print "READY"
        
            file = open('energies.txt', 'r')
            lines = file.readlines()
            file.close()
            file2=open('phase.txt','r')
            lines2=file2.readlines()
            file2.close()
            file3=open('min.txt','r')
            lines3=file3.readlines()
            file3.close()
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
        fig1=Figure()
        ax1f1=fig1.add_subplot(111)
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
        ax1f2.plot(xv,yv, 'b.-')
        ax1f2.set_title('Medium Energy')
        
        ax2f2=fig2.add_subplot(122)
        ax2f2.plot(xv,zv, 'r.-')
        ax2f2.set_title('Chemical Potential')
        
        x3 = []
        y3 = []
        for line in lines3:
            p3 = line.split()
            x3.append(float(p3[0]))
            y3.append(float(p3[1]))
        xv3 = np.array(x3)
        yv3 = np.array(y3)
        
        fig3=Figure()
        ax1f3=fig3.add_subplot(111)
        ax1f3.plot(xv3,yv3,'b.-')
        ax1f3.set_title('Soliton Position')
        
        self.delfig()
        self.delfig()
        self.delfig()
        self.addfig('PHASE',fig1)
        self.addfig('ENERGY',fig2)
        self.addfig('MINUS',fig3)
                
        
    def rmmpl(self):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.canvas.close()
                
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