from __future__ import unicode_literals
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui, QtCore
from outputEcvt import *
import h5py
from numpy import array, sum
import sys
import main
from appLib import *
import h5py
from math import *
import serial
from serial.serialutil import SerialException

from numpy import *
from math import *
import numpy as np
import binascii
import base64
from compiler.ast import Bitxor
import time
from ecvtlib import *
program_dir = "F:/CHPC/Breast Scan New Ver 1"

class mainlogic(QtGui.QWidget,main.Ui_Dialog):
    def __init__(self,parent=None):
            super(mainlogic,self).__init__(parent)            
            self.setupUi(self)
            self.connectActions()
   
    def main(self):
        self.show()
        
    def connectActions(self):
        #push button open connection
        self.pushButton_3.clicked.connect(self.openSerialConnection)
        self.pushButton.clicked.connect(self.saveDeviceSetting)
        #push button close connection
        self.pushButton_2.clicked.connect(self.closeSerialConnection)
        self.pushButton_9.clicked.connect(self.openFile)
        self.pushButton_7.clicked.connect(self.saveFile)
        self.pushButton_10.clicked.connect(self.runCalibration)
        self.pushButton_8.clicked.connect(self.runReconstruction)
       
        
        
    def openFile(self):
        #Open Saved File
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', program_dir)
        fname = unicode(fname)       	
	s = ecvt_matriks(fname) 
        #print np.shape(self.ve)
        #self.mplwidget.update_figure(self.ve, self.vf, self.vr) 
        self.mplwidget_4.plot3d_data(s)
        #print np.shape(self.ve)
    
    def saveFile(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', program_dir)
        fname = unicode(fname)
	a, b = self.getDeviceSetting()
        with h5py.File(fname, 'w') as f:
            f['/Ve'] = self.ve
            f['/Vf'] = self.vf
            f['/Vr'] = self.vr  
            f['/sensor'] = a
            f['/channel'] = b
        self.message("Data Successfully Saved!")
    
    def message(self,txt):
        self.msgBox = QtGui.QMessageBox(self)
        self.msgBox.setText(txt)
        self.msgBox.setWindowTitle("CTX-Breast Scan")
        self.msgBox.exec_()
            
    
    def getCalMode(self):
         self.calIndex = self.comboBox.currentIndex()
    
    def getDeviceSetting(self):
        fname = program_dir+"/database/setting.h5"
        fname = unicode(fname)  
        device_data = h5py.File(fname)          
        sensor=array(device_data['sensor'])
        channel=array(device_data['channel'])
        device_data.close()
        return sensor,channel    
    
    def saveDeviceSetting(self):
        self.setSensor = self.comboBox_2.currentIndex()
        self.setCH = self.comboBox_3.currentIndex()   
        self.portname = self.comboBoxPort.currentText()        
        fname = program_dir+"/database/setting.h5"
        fname = unicode(fname) 
       
        
        with h5py.File(fname, 'w') as f:
                    f['/sensor'] = self.setSensor
                    f['/channel'] = self.setCH   
         
        h5py.File(fname).close()        
        self.message("Setting Successfully Saved!")      
       
    def openSerialConnection(self):        
        self.message("Load Setting!")    
         
         
         #offline mode
	self.portname = self.comboBoxPort.currentText()  
	try:             
	   self.ser = serial.Serial(
	       port=self.portname,
	       baudrate=115200,
	       stopbits=1,
	       timeout=10) 
	   
	   setting_ecvt(self.ser)
	   QMessageBox.information(self, 'Success','Opened %s successfully' % self.portname)
	except SerialException, e:
	   QMessageBox.critical(self, 'Failure','Failed to open %s:\n%s' % (self.portname, e))
   
    def closeSerialConnection(self):
         #print output_ecvt(self.ser)
         self.portname = self.comboBoxPort.currentText()  
         try:             
            self.ser.close()         
            QMessageBox.information(self, 'Success','Closed %s successfully' % self.portname)
         except SerialException, e:
            QMessageBox.critical(self, 'Failure','Failed to open %s:\n%s' % (self.portname, e))  
            
    def runReconstruction(self):
        self.message("Run 3D Image Reconstruction!")
        self.mplwidget_4.clearPlt(self.ve, self.vf, self.vr)
      
    def runCalibration(self):
        calIndex = self.comboBox.currentIndex()          
        if calIndex == 0:            
            self.message("Run Empty Calibration")
            E1,E2,E3,ViDAC = empty_cal(self.ser)
            self.message("Run Full Calibration")
            ve, vf = full_cal(self.ser)
            self.ve, self.vf = ve, vf
            #self.ve = gen_mat(180,900,1000)
            self.mplwidget_2.update_figure(calIndex, self.ve)
            self.mplwidget_2.update_figure(1, self.vf)
            self.mplwidget.update_figure_cal(self.ve, self.vf)
        elif calIndex == 1:
            self.message("Run Empty Calibration")
            E1,E2,E3,ViDAC = empty_cal(self.ser)
            self.message("Run Full Calibration")
            ve, vf = full_cal(self.ser)
            self.vf = vf
            #self.ve = gen_mat(180,900,1000)
            self.mplwidget_2.update_figure(calIndex, self.ve)
            self.mplwidget_2.update_figure(1, self.vf)
            self.mplwidget.update_figure_cal(self.ve, self.vf)
        elif calIndex == 2:
            self.message("Run Capasitance")
            #self.vr = gen_mat(180,1450,1500)
            datValid=0
            dtValid=0
            datValid=[]            
            [datValid[0:], dtValid] = full_ecvt_get_data(dtValid, self.ser)    
            [a, b]=shape(datValid)                            
            Vr=datValid[0] 
            self.vr = Vr            
            self.mplwidget_2.update_figure(calIndex, self.vr)        
            
            
        self.mplwidget.update_figure(self.ve, self.vf, self.vr) 
            #print calIndex     
	    
   
        
from PyQt4.QtCore import *
from PyQt4.QtGui import *               
import time
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)  
    splash_pix = QPixmap('logo.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    # Simulate something that takes time
    time.sleep(0.5)  
    mainlogic1 = mainlogic()
    mainlogic1.main()    
    splash.finish(mainlogic1) 
    app.exec_()
    #sys.exit(app.exec_())    