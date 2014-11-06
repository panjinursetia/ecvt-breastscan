from PyQt4 import QtCore,QtGui
import h5py
from numpy import array, sum
import sys
import main
from appLib import *
import h5py



        
class mainlogic(QtGui.QWidget,main.Ui_Dialog):
    def __init__(self,parent=None):
            """
                Initialization of the class. Call the __init__ for the super classes
            """
            super(mainlogic,self).__init__(parent)            
            self.setupUi(self)
            self.connectActions()
   
    def main(self):
        self.show()
        
    def connectActions(self):
        self.pushButton_9.clicked.connect(self.openFile)
        self.pushButton_7.clicked.connect(self.saveFile)
        self.pushButton_10.clicked.connect(self.runCalibration)
        self.pushButton_8.clicked.connect(self.runReconstruction)
       
        
        
    def openFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'F:/')
        fname = unicode(fname)
        v_data = h5py.File(fname)        
        
        self.ve=array(v_data['Ve'])
        self.vf=array(v_data['Vf'])
        self.vr=array(v_data['Vr']) 
        
        print fname, sum(self.ve), sum(self.vf), sum(self.vr) 
    
    def saveFile(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 'F:/')
        fname = unicode(fname)        
       
        with h5py.File(fname, 'w') as f:
            f['/Ve'] = self.ve
            f['/Vf'] = self.vf
            f['/Vr'] = self.vr
        
        self.message("Data Successfully Saved!")
    
    def message(self,txt):
        self.msgBox = QtGui.QMessageBox(self)
        self.msgBox.setText(txt)
        self.msgBox.exec_()
            
    
    def getCalMode(self):
         self.calIndex = self.comboBox.currentIndex()
    
    def runReconstruction(self):
        print sum(self.ve), sum(self.vf), sum(self.vr)
        
        
    def runCalibration(self):
        calIndex = self.comboBox.currentIndex()  
        
        if calIndex == 0:
            #print calIndex
            self.message("Run Empty Calibration")
            self.ve = gen_mat(180,900,1000)
            self.mplwidget_2.update_figure(calIndex, self.ve)
            
            
        
        elif calIndex == 1:
            self.message("Run Full Calibration")
            self.vf = gen_mat(180,1100,1150)
            self.mplwidget_2.update_figure(calIndex, self.vf)
            
            
        self.mplwidget.update_figure(self.ve, self.vf) 
            #print calIndex      
    
        
               
      
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mainlogic1 = mainlogic()
    mainlogic1.main()
    sys.exit(app.exec_())    