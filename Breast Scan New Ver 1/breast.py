from __future__ import unicode_literals
import os
os.environ['ETS_TOOLKIT'] = 'qt4'

from pyface.qt import QtGui, QtCore
from traits.api import HasTraits,Button, Instance, on_trait_change, \
    Int, Dict
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor

import sys, os, random
from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#import library dari tkinter/GUI added 8/10/2013

import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Pmw
import time
#####
import tables
import numpy as np
from outputEcvt import *
#from bTesKalibrasi import Ve, Vf
from math import *
from mayavi.mlab import *
import matplotlib.pyplot as plt
from tables import *
from CONVERTNSM import *
from rekonstruksi import *
import tkFileDialog 
import matplotlib.gridspec as gridspec

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    button1 = Button('Redraw')
    
    def ambil_data_scan(self):
        ant3d=np.zeros(6255920)
        an3d=np.zeros(6255920)
        
        f=tables.openFile("ant3d.h5")
        g=tables.openFile("an3d.h5")
        h=tables.openFile("Ve.h5")
        j=tables.openFile("Vf.h5")
        
        ant3d= f.root.detector.readout.cols.matNsm[:]
        an3d= g.root.detector.readout.cols.matNsm[:]
        Ve= h.root.detector.readout.cols.matNsm[:]
        Vf= j.root.detector.readout.cols.matNsm[:]
        Vr = Vf-100

        ant3d=ant3d.reshape(32768, 190)
        an3d=an3d.reshape(190, 32768)
        
        CH=20
        m=CH*(CH-1)/2
        SETi=10
        b=0
        frames=0
        Frame=SETi
        urut =1
        urut=0
        dec=np.zeros((1,m))
        dataArbai=np.zeros((SETi,1))
        ADC=np.zeros((1,2*m))
        DataRec=np.zeros((SETi,m))
        dt=0
        Avg=8
        iAvg=0
        datAvg=0
        datValid=0
        Ve1=Ve/Vf
        Vf1=np.ones((1, m))
        dtValid=0
        datValid=[]
        Vr=[]
        ncp=[]
        cp=[]
        image1=[]

        for i in range(Frame):
            #[datValid[i:], dtValid] = full_ecvt_get_data(CH,dtValid)    
            #[a, b]=shape(datValid)
            #Vr=datValid[a-1]
            Vr=Vf
            frames=frames+1
            Vr1=Vr/Vf
            Vr1=Vr1.reshape(1, m)
            #dataArbai=Vr
            dn = (Vr1-Ve1)/(Vf1-Ve1)
            dn[nonzero(dn>=1)]=1
            dn[nonzero(dn<=0)]=0
            y1=dn.T
            y1=konvertnan(y1)
            ncp[i:]=np.array([y1])
            Vrr=Vr1.T
            Vrr=konvertnan(Vrr)
            cp[i:]=Vrr
            iter=2                                                                                                                                      
            alpha0=0.1
            t=0
            v0=dot(ant3d, y1)
            eval=1
            t1=1
            serr=0
            v=v0
            while (t1<=iter):
                phi1=y1-dot(ant3d.T, v0)
                v=v0+alpha0*dot(an3d.T, phi1)
                err=abs(v-v0)
                serr=serr+sum(err**2)
                v[nonzero(v>=1)]=1
                v[nonzero(v<=0)]=0
                v0=v
                t1=t1+1
            image1=v.reshape((32, 32, 32))   
    
        x, y, z = np.ogrid[0:31:31j, 0:31:31j, 0:31:31j]
        
        start_time = time.clock()
        self.s = image1
        return(self.s)
        
    @on_trait_change('scene.activated')
    def update_plot(self):       
        s = self.ambil_data_scan()
        src = mlab.pipeline.scalar_field(s, 
                                         scaling=(1, 1, 1), 
                                         origin=(1,1,1))
        
        src.spacing = [0.75, 1, 1]
        
        #iso surface
        m=mlab.pipeline.iso_surface(src, 
                                    contours=[s.min()+0.01*s.ptp(), ],
                                    opacity=0.3
                                    )
        
        #imageplane X
        mlab.pipeline.image_plane_widget(src,plane_orientation='y_axes',slice_index=16,)
        
	#imageplane X
        mlab.pipeline.image_plane_widget(src,plane_orientation='x_axes',slice_index=16,)        
        
        
        #volume 
        mlab.pipeline.volume(
                src, 
                vmin=s.min(), 
                vmax=0.2
        )       
        
        m.module_manager.scalar_lut_manager.show_scalar_bar = True
        mlab.colorbar(orientation='vertical')  
	f = mlab.gcf()
	camera = f.scene.camera
	camera.yaw(60)	
        # LUT means "Look-Up Table", it give the mapping between scalar value and color
        mlab.view(15, 15, 15, (20, 20, 20))
        mlab.show() 
     
    #@on_trait_change('button1')   
    def update_plot_2(self):       
        s = self.ambil_data_scan()
    
        src = mlab.pipeline.scalar_field(s, 
                                         scaling=(1, 1, 1), 
                                         origin=(1,1,1))
        
        src.spacing = [0.75, 1, 1]
        
        #iso surface
        m=mlab.pipeline.iso_surface(src, 
                                    contours=[s.min()+0.01*s.ptp(), ],
                                    opacity=0.3
                                    )
        
        #imageplane
        mlab.pipeline.image_plane_widget(src,plane_orientation='y_axes',slice_index=1,)
        
        
        #volume 
        mlab.pipeline.volume(
                src, 
                vmin=s.min(), 
                vmax=0.2
        )       
        
        m.module_manager.scalar_lut_manager.show_scalar_bar = True
        mlab.colorbar(orientation='horizontal')      
        # LUT means "Look-Up Table", it give the mapping between scalar value and color
        mlab.view(15, 15, 15, (20, 20, 20))
        mlab.show()           
        
    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),'button1',
                resizable=True # We need this to resize with the parent widget
                )


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)
        self.visualization = Visualization()
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)
	
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = plt.plot()
	self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class KalibrasiEmpty(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
	h=tables.openFile("Ve.h5")
	j=tables.openFile("Vf.h5")        
        Ve= h.root.detector.readout.cols.matNsm[:]
        Vf= j.root.detector.readout.cols.matNsm[:]  
	
	self.line_kalibrasi_empty, = self.axes.plot(Ve,'r', label="Ve")
	
class KalibrasiFull(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def __init__(self, *args, **kwargs):
	  self.h=tables.openFile("Ve.h5")	
	  self.Ve= self.h.root.detector.readout.cols.matNsm[:]
	  
	  
	  MyMplCanvas.__init__(self, *args, **kwargs)
	  timer = QtCore.QTimer(self)
	  #QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.update_kalibrasi_full)
	  #QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.update_kalibrasi_full)   
	  timer.start(1000)    

    def compute_initial_figure(self):
	h=tables.openFile("Ve.h5")
	j=tables.openFile("Vf.h5")        
        Ve= h.root.detector.readout.cols.matNsm[:]
        Vf= j.root.detector.readout.cols.matNsm[:]  
	
	self.axes.plot(Vf,'b', label="Ve")	

    def update_kalibrasi_full(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [ random.randint(2500, 3000) for i in range(190) ]
        self.axes.plot(l, 'b')
        self.draw()
	
class DynamicKalibrasi(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
	self.h=tables.openFile("Ve.h5")	
	self.Ve= self.h.root.detector.readout.cols.matNsm[:]
	
	
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
         self.axes.plot(self.Ve, 'g')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [ random.randint(2500, 3000) for i in range(190) ]

        self.axes.plot(l, 'g')
        self.draw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1520, 884)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ECVT Breast Cancer Scanner", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/User/Favorites/Downloads/logo-c.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip(QtGui.QApplication.translate("MainWindow", "Run Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 10, 1471, 771))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 1111, 701))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "3D Visualisation", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
#widget mayavi        
        self.mplwidget = MayaviQWidget(self.groupBox)
        self.mplwidget.setGeometry(QtCore.QRect(20, 20, 1071, 671))
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(1150, 10, 311, 701))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.toolBox = QtGui.QToolBox(self.groupBox_2)
        self.toolBox.setGeometry(QtCore.QRect(20, 30, 281, 581))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.toolBox.setFont(font)
        self.toolBox.setFrameShape(QtGui.QFrame.Panel)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 279, 515))
        self.page.setObjectName(_fromUtf8("page"))
        self.pushButton_5 = QtGui.QPushButton(self.page)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 140, 50, 41))
        self.pushButton_5.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/User/Favorites/Downloads/1384157809_208018.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.page)
        self.pushButton_6.setGeometry(QtCore.QRect(140, 140, 50, 41))
        self.pushButton_6.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/User/Favorites/Downloads/1384157972_174920.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon2)
        self.pushButton_6.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.comboBox_9 = QtGui.QComboBox(self.page)
        self.comboBox_9.setGeometry(QtCore.QRect(129, 8, 131, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_9.setFont(font)
        self.comboBox_9.setObjectName(_fromUtf8("comboBox_9"))
        self.comboBox_9.addItem(_fromUtf8(""))
        self.comboBox_9.setItemText(0, QtGui.QApplication.translate("MainWindow", "Image Reconstruction", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_9.addItem(_fromUtf8(""))
        self.comboBox_9.setItemText(1, QtGui.QApplication.translate("MainWindow", "Post-Processing", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12 = QtGui.QLabel(self.page)
        self.label_12.setGeometry(QtCore.QRect(13, 13, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "Operation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.page)
        self.label_13.setGeometry(QtCore.QRect(12, 44, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "Algorithm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.comboBox_10 = QtGui.QComboBox(self.page)
        self.comboBox_10.setGeometry(QtCore.QRect(130, 40, 131, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_10.setFont(font)
        self.comboBox_10.setObjectName(_fromUtf8("comboBox_10"))
        self.comboBox_10.addItem(_fromUtf8(""))
        self.comboBox_10.setItemText(0, QtGui.QApplication.translate("MainWindow", "ILBP", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_10.addItem(_fromUtf8(""))
        self.comboBox_10.setItemText(1, QtGui.QApplication.translate("MainWindow", "NN-MOIRT", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14 = QtGui.QLabel(self.page)
        self.label_14.setGeometry(QtCore.QRect(12, 80, 90, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setText(QtGui.QApplication.translate("MainWindow", "Step", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.comboBox_11 = QtGui.QComboBox(self.page)
        self.comboBox_11.setGeometry(QtCore.QRect(130, 72, 131, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_11.setFont(font)
        self.comboBox_11.setObjectName(_fromUtf8("comboBox_11"))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(1, QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(2, QtGui.QApplication.translate("MainWindow", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(3, QtGui.QApplication.translate("MainWindow", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(4, QtGui.QApplication.translate("MainWindow", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(5, QtGui.QApplication.translate("MainWindow", "6", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(6, QtGui.QApplication.translate("MainWindow", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(7, QtGui.QApplication.translate("MainWindow", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(8, QtGui.QApplication.translate("MainWindow", "9", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_11.addItem(_fromUtf8(""))
        self.comboBox_11.setItemText(9, QtGui.QApplication.translate("MainWindow", "10", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15 = QtGui.QLabel(self.page)
        self.label_15.setGeometry(QtCore.QRect(12, 107, 90, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setText(QtGui.QApplication.translate("MainWindow", "Frame Number", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.comboBox_12 = QtGui.QComboBox(self.page)
        self.comboBox_12.setGeometry(QtCore.QRect(130, 101, 41, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_12.setFont(font)
        self.comboBox_12.setObjectName(_fromUtf8("comboBox_12"))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(1, QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(2, QtGui.QApplication.translate("MainWindow", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(3, QtGui.QApplication.translate("MainWindow", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(4, QtGui.QApplication.translate("MainWindow", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(5, QtGui.QApplication.translate("MainWindow", "6", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(6, QtGui.QApplication.translate("MainWindow", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(7, QtGui.QApplication.translate("MainWindow", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(8, QtGui.QApplication.translate("MainWindow", "9", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_12.addItem(_fromUtf8(""))
        self.comboBox_12.setItemText(9, QtGui.QApplication.translate("MainWindow", "10", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13 = QtGui.QComboBox(self.page)
        self.comboBox_13.setGeometry(QtCore.QRect(220, 100, 41, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_13.setFont(font)
        self.comboBox_13.setObjectName(_fromUtf8("comboBox_13"))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(1, QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(2, QtGui.QApplication.translate("MainWindow", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(3, QtGui.QApplication.translate("MainWindow", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(4, QtGui.QApplication.translate("MainWindow", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(5, QtGui.QApplication.translate("MainWindow", "6", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(6, QtGui.QApplication.translate("MainWindow", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(7, QtGui.QApplication.translate("MainWindow", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(8, QtGui.QApplication.translate("MainWindow", "9", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_13.addItem(_fromUtf8(""))
        self.comboBox_13.setItemText(9, QtGui.QApplication.translate("MainWindow", "10", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16 = QtGui.QLabel(self.page)
        self.label_16.setGeometry(QtCore.QRect(189, 102, 10, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setText(QtGui.QApplication.translate("MainWindow", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.pushButton_7 = QtGui.QPushButton(self.page)
        self.pushButton_7.setGeometry(QtCore.QRect(80, 140, 50, 41))
        self.pushButton_7.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/User/Favorites/Downloads/1384157920_208014.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon3)
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(self.page)
        self.pushButton_8.setGeometry(QtCore.QRect(200, 140, 50, 41))
        self.pushButton_8.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/User/Favorites/Downloads/1384349057_103529.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon4)
        self.pushButton_8.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.label_17 = QtGui.QLabel(self.page)
        self.label_17.setGeometry(QtCore.QRect(36, 180, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setText(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtGui.QLabel(self.page)
        self.label_18.setGeometry(QtCore.QRect(95, 181, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_19 = QtGui.QLabel(self.page)
        self.label_19.setGeometry(QtCore.QRect(153, 181, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.label_20 = QtGui.QLabel(self.page)
        self.label_20.setGeometry(QtCore.QRect(212, 181, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_20.setFont(font)
        self.label_20.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.toolBox.addItem(self.page, _fromUtf8(""))
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 279, 515))
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.toolBox.addItem(self.page_2, _fromUtf8(""))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 20, 331, 321))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setTitle(QtGui.QApplication.translate("MainWindow", "Setting Kalibrasi", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.comboBox = QtGui.QComboBox(self.groupBox_4)
        self.comboBox.setGeometry(QtCore.QRect(209, 50, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Brain", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "Breast", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_2.setGeometry(QtCore.QRect(209, 84, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(0, QtGui.QApplication.translate("MainWindow", "16", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(1, QtGui.QApplication.translate("MainWindow", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(2, QtGui.QApplication.translate("MainWindow", "24", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(3, QtGui.QApplication.translate("MainWindow", "32", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(4, QtGui.QApplication.translate("MainWindow", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Jenis Scanner", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(9, 86, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Jumlah Sensor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.line = QtGui.QFrame(self.groupBox_4)
        self.line.setGeometry(QtCore.QRect(10, 70, 301, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(self.groupBox_4)
        self.line_2.setGeometry(QtCore.QRect(10, 105, 301, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(9, 119, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Min. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.comboBox_3 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_3.setGeometry(QtCore.QRect(209, 119, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("MainWindow", "900", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(1, QtGui.QApplication.translate("MainWindow", "1000", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(2, QtGui.QApplication.translate("MainWindow", "1200", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_4 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_4.setGeometry(QtCore.QRect(210, 150, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_4.setFont(font)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.setItemText(0, QtGui.QApplication.translate("MainWindow", "1500", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.setItemText(1, QtGui.QApplication.translate("MainWindow", "1700", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.setItemText(2, QtGui.QApplication.translate("MainWindow", "1800", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.setItemText(3, QtGui.QApplication.translate("MainWindow", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(10, 150, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Max. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.line_3 = QtGui.QFrame(self.groupBox_4)
        self.line_3.setGeometry(QtCore.QRect(10, 111, 301, 70))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(10, 180, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Mean. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.comboBox_5 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_5.setGeometry(QtCore.QRect(210, 180, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_5.setFont(font)
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.setItemText(0, QtGui.QApplication.translate("MainWindow", "0.5", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.setItemText(1, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.setItemText(2, QtGui.QApplication.translate("MainWindow", "1.5", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.setItemText(3, QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.setItemText(4, QtGui.QApplication.translate("MainWindow", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.line_4 = QtGui.QFrame(self.groupBox_4)
        self.line_4.setGeometry(QtCore.QRect(10, 172, 301, 70))
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.label_9 = QtGui.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(10, 210, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Gain. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.comboBox_6 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_6.setGeometry(QtCore.QRect(210, 210, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_6.setFont(font)
        self.comboBox_6.setObjectName(_fromUtf8("comboBox_6"))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.comboBox_6.setItemText(0, QtGui.QApplication.translate("MainWindow", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.comboBox_6.setItemText(1, QtGui.QApplication.translate("MainWindow", "10", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.comboBox_6.setItemText(2, QtGui.QApplication.translate("MainWindow", "15", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.comboBox_6.setItemText(3, QtGui.QApplication.translate("MainWindow", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.line_5 = QtGui.QFrame(self.groupBox_4)
        self.line_5.setGeometry(QtCore.QRect(10, 142, 301, 70))
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.label_10 = QtGui.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(11, 241, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.comboBox_7 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_7.setGeometry(QtCore.QRect(210, 240, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_7.setFont(font)
        self.comboBox_7.setObjectName(_fromUtf8("comboBox_7"))
        self.comboBox_7.addItem(_fromUtf8(""))
        self.comboBox_7.setItemText(0, QtGui.QApplication.translate("MainWindow", "COM 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_7.addItem(_fromUtf8(""))
        self.comboBox_7.setItemText(1, QtGui.QApplication.translate("MainWindow", "COM 2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_7.addItem(_fromUtf8(""))
        self.comboBox_7.setItemText(2, QtGui.QApplication.translate("MainWindow", "COM 3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11 = QtGui.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(9, 269, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Baudrate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.comboBox_8 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_8.setGeometry(QtCore.QRect(210, 271, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_8.setFont(font)
        self.comboBox_8.setObjectName(_fromUtf8("comboBox_8"))
        self.comboBox_8.addItem(_fromUtf8(""))
        self.comboBox_8.setItemText(0, QtGui.QApplication.translate("MainWindow", "15200", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_8.addItem(_fromUtf8(""))
        self.comboBox_8.setItemText(1, QtGui.QApplication.translate("MainWindow", "13200", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_8.addItem(_fromUtf8(""))
        self.comboBox_8.setItemText(2, QtGui.QApplication.translate("MainWindow", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.line_6 = QtGui.QFrame(self.groupBox_4)
        self.line_6.setGeometry(QtCore.QRect(10, 202, 301, 70))
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.line_7 = QtGui.QFrame(self.groupBox_4)
        self.line_7.setGeometry(QtCore.QRect(11, 232, 301, 70))
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.groupBox_5 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_5.setGeometry(QtCore.QRect(360, 20, 1081, 761))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setTitle(QtGui.QApplication.translate("MainWindow", "Grafik Kalibrasi", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
#widget grafik kalibrasi        
        self.mplwidget_4 = KalibrasiEmpty(self.groupBox_5)
        self.mplwidget_4.setGeometry(QtCore.QRect(20, 50, 961, 200))
        self.mplwidget_4.setObjectName(_fromUtf8("mplwidget_4"))
        self.mplwidget_5 = KalibrasiFull(self.groupBox_5)
        self.mplwidget_5.setGeometry(QtCore.QRect(20, 280, 961, 200))
        self.mplwidget_5.setObjectName(_fromUtf8("mplwidget_5"))
        self.mplwidget_6 = DynamicKalibrasi(self.groupBox_5)
        self.mplwidget_6.setGeometry(QtCore.QRect(20, 509, 961, 200))
        self.mplwidget_6.setObjectName(_fromUtf8("mplwidget_6"))
	
        self.label_22 = QtGui.QLabel(self.groupBox_5)
        self.label_22.setGeometry(QtCore.QRect(420, 30, 141, 16))
        self.label_22.setText(QtGui.QApplication.translate("MainWindow", "Empty Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_23 = QtGui.QLabel(self.groupBox_5)
        self.label_23.setGeometry(QtCore.QRect(421, 259, 141, 16))
        self.label_23.setText(QtGui.QApplication.translate("MainWindow", "Full Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_24 = QtGui.QLabel(self.groupBox_5)
        self.label_24.setGeometry(QtCore.QRect(422, 490, 141, 16))
        self.label_24.setText(QtGui.QApplication.translate("MainWindow", "Run DAS", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.groupBox_6 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 350, 331, 271))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setTitle(QtGui.QApplication.translate("MainWindow", "Mode Kalibrasi", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.radioButton = QtGui.QRadioButton(self.groupBox_6)
        self.radioButton.setGeometry(QtCore.QRect(10, 50, 131, 31))
        self.radioButton.setText(QtGui.QApplication.translate("MainWindow", "Warming Off", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox_6)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 80, 141, 31))
        self.radioButton_2.setText(QtGui.QApplication.translate("MainWindow", "Empty Kalibrasi", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.radioButton_3 = QtGui.QRadioButton(self.groupBox_6)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 110, 141, 31))
        self.radioButton_3.setText(QtGui.QApplication.translate("MainWindow", "Full Kalibrasi", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.radioButton_4 = QtGui.QRadioButton(self.groupBox_6)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 23, 161, 31))
        self.radioButton_4.setText(QtGui.QApplication.translate("MainWindow", "Set Das Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox_6)
        self.pushButton_2.setGeometry(QtCore.QRect(76, 150, 50, 41))
        self.pushButton_2.setText(_fromUtf8(""))
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox_6)
        self.pushButton_3.setGeometry(QtCore.QRect(136, 150, 50, 41))
        self.pushButton_3.setText(_fromUtf8(""))
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox_6)
        self.pushButton_4.setGeometry(QtCore.QRect(196, 150, 50, 41))
        self.pushButton_4.setText(_fromUtf8(""))
        self.pushButton_4.setIcon(icon2)
        self.pushButton_4.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.label_25 = QtGui.QLabel(self.tab_2)
        self.label_25.setGeometry(QtCore.QRect(1094, 650, 161, 20))
        self.label_25.setText(QtGui.QApplication.translate("MainWindow", "Powered By:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1222, 786, 51, 61))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/User/Favorites/Downloads/logo-c.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1261, 797, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label_2.setFont(font)
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "CTECH Laboratories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1261, 817, 241, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Center for Medical Physics and Cancer Research", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.dasdasd = Qwt5.QwtTextLabel(self.centralwidget)
        self.dasdasd.setGeometry(QtCore.QRect(580, 640, 100, 20))
        self.dasdasd.setIndent(1)
        self.dasdasd.setObjectName(_fromUtf8("dasdasd"))
        self.label_21 = QtGui.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(1220, 780, 81, 16))
        self.label_21.setText(QtGui.QApplication.translate("MainWindow", "Powered By:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1520, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSetting = QtGui.QMenu(self.menubar)
        self.menuSetting.setTitle(QtGui.QApplication.translate("MainWindow", "Setting", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSetting.setObjectName(_fromUtf8("menuSetting"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionPrint = QtGui.QAction(MainWindow)
        self.actionPrint.setText(QtGui.QApplication.translate("MainWindow", "Print", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionDAS_Setting = QtGui.QAction(MainWindow)
        self.actionDAS_Setting.setText(QtGui.QApplication.translate("MainWindow", "DAS Setting", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDAS_Setting.setObjectName(_fromUtf8("actionDAS_Setting"))
        self.actionAlgoritma_Setting = QtGui.QAction(MainWindow)
        self.actionAlgoritma_Setting.setText(QtGui.QApplication.translate("MainWindow", "Algoritma Setting", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAlgoritma_Setting.setObjectName(_fromUtf8("actionAlgoritma_Setting"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionClose)
        self.menuSetting.addAction(self.actionDAS_Setting)
        self.menuSetting.addAction(self.actionAlgoritma_Setting)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.mplwidget_4.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("MainWindow", "Rekonstruksi", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("MainWindow", "Post-Processing", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Scanning", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Kalibrasi", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qwt5
from matplotlibwidget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

