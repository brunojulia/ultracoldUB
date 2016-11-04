# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:14:44 2016

@author: ivan
"""
from DS_interfaz import *
from BS_interfaz import *
from WD_interfaz import *
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
import math
Ui_MainWindow,QMainWindow=loadUiType('Main.ui')

import time
from datetime import datetime
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
        
        self.file = open('output.txt','w')
        self.file.close()
        self.file = open('output.txt','a')
        self.file.write('Bienvenido a UltracoldUB. Estamos a: %s \n' %(str(datetime.now())))
        
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
        self.file = open('output.txt','a')
        self.file.write('#################')
        self.file.write('Interfaz seleccionada: Dark Solitons')
        self.file.write('#################\n\n')
        self.file.close()
        self.hide()
        self.dark_window = DS(self)
        self.dark_window.show()
        self.dark_window.raise_()
    
    def brightbutton(self):
        self.file = open('output.txt','a')
        self.file.write('#################')
        self.file.write('Interfaz seleccionada: Bright Solitons')
        self.file.write('#################\n\n')
        self.hide()
        self.bright_window = BS(self)
        self.bright_window.show()
        self.bright_window.raise_()   
        
    def dispersionbutton(self):
        self.file = open('output.txt','a')
        self.file.write('#################')
        self.file.write('Interfaz seleccionada: Wave Pack Dispersions')
        self.file.write('#################\n\n')
        self.file.close()
        self.hide()
        self.dispersion_window = WD(self)
        self.dispersion_window.show()
        self.dispersion_window.raise_()  
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'EXIT',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.file.close()
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
            
if __name__=='__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np
    
    
    app=QtGui.QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec_())