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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import time
#####
import tables
import numpy as np
from math import *
from mayavi.mlab import *
import matplotlib.pyplot as plt
from tables import *
import tkFileDialog 
import matplotlib.gridspec as gridspec
from appLib import *
import sys, os, random
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
            dn[np.nonzero(dn>=1)]=1
            dn[np.nonzero(dn<=0)]=0
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
                v[np.nonzero(v>=1)]=1
                v[np.nonzero(v<=0)]=0
                v0=v
                t1=t1+1
            image1=v.reshape((32, 32, 32))   
    
        x, y, z = np.ogrid[0:31:31j, 0:31:31j, 0:31:31j]
        
        start_time = time.clock()
        self.s = image1
	print s
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
	e = self.scene.engine
	e.add_module(Outline())
	e.add_module(Surface())
	
    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )

	#view = View(HSplit(VSplit(Item(name='engine_view',
                                   #style='custom',
                                   #resizable=True,
                                   #show_label=False
                                   #),
                              #Item(name='current_selection',
                                   #editor=InstanceEditor(),
                                   #enabled_when='current_selection is not None',
                                   #style='custom',
                                   #springy=True,
                                   #show_label=False),
                                   #),
                               #Item(name='scene',
                                    #editor=SceneEditor(),
                                    #show_label=False,
                                    #resizable=True,
                                    #height=500,
                                    #width=500),
                        #),
                #resizable=True,
                #scrollable=True
                #)
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
    def __init__(self, parent=None, width=2, height=2, dpi=100):
	fig = Figure(figsize=(width, height), dpi=dpi)
	
	self.axes = fig.add_subplot(111)
	for label in (self.axes.get_xticklabels() + self.axes.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(4)  	
	self.axes.xlim = (0,100)
	#self.axes = plt.subplot(111)
	self.axes.hold(False)    
	self.compute_initial_figure()  
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
	self.ve = gen_mat(180,1000,1100)
	self.vf = gen_mat(180,1300,1400)
	self.axes.grid(True)
	self.line_kalibrasi_empty, = self.axes.plot(self.ve,'r', label="Ve")
	

class Kapasitansi(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):	 
	self.vr = gen_mat(180,1100,1200)		
	self.line_kapasitansi, = self.axes.plot(self.vr,'g', label="Ve")
	self.axes.plot.set_ylim([0,1000])

class DynamicKalibrasi(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
	
	self.Ve = gen_mat(180,1100,1200)	
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
	
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Ctechlabs - ECVT Breast Scan"))
        Dialog.resize(1049, 657)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Ctechlabs - ECVT Breast Scan", "Ctechlabs - ECVT Breast Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(39, 30, 611, 601))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox.setFont(font)
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "3D View", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
	self.mplwidget_4 = MayaviQWidget(self.groupBox)
	self.mplwidget_4.setGeometry(QtCore.QRect(10, 30, 581, 561))
	self.mplwidget_4.setObjectName(_fromUtf8("mplwidget_4"))	
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(670, 34, 351, 411))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Data Acquisition System", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.tabWidget = QtGui.QTabWidget(self.groupBox_2)
        self.tabWidget.setGeometry(QtCore.QRect(30, 50, 291, 331))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tabWidget.setFont(font)
        self.tabWidget.setWhatsThis(QtGui.QApplication.translate("Dialog", "sdsda", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.mplwidget = DynamicKalibrasi(self.tab)
        self.mplwidget.setGeometry(QtCore.QRect(12, 11, 261, 191))
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.pushButton_7 = QtGui.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(168, 221, 51, 41))
        self.pushButton_7.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384157972_174920.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon)
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(111, 221, 51, 41))
        self.pushButton_8.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384157809_208018.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon1)
        self.pushButton_8.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_9 = QtGui.QPushButton(self.tab)
        self.pushButton_9.setGeometry(QtCore.QRect(224, 220, 51, 41))
        self.pushButton_9.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384349057_103529.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon2)
        self.pushButton_9.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.mplwidget_2 = KalibrasiEmpty(self.tab_2)
        self.mplwidget_2.setGeometry(QtCore.QRect(11, 10, 261, 191))
        self.mplwidget_2.setObjectName(_fromUtf8("mplwidget_2"))
        self.comboBox = QtGui.QComboBox(self.tab_2)
        self.comboBox.setGeometry(QtCore.QRect(160, 220, 111, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Empty Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Full Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "Warming Das", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16 = QtGui.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(8, 217, 141, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_16.setFont(font)
        self.label_16.setText(QtGui.QApplication.translate("Dialog", "Calibration Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.pushButton_10 = QtGui.QPushButton(self.tab_2)
        self.pushButton_10.setGeometry(QtCore.QRect(163, 250, 51, 41))
        self.pushButton_10.setText(_fromUtf8(""))
        self.pushButton_10.setIcon(icon1)
        self.pushButton_10.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.pushButton_11 = QtGui.QPushButton(self.tab_2)
        self.pushButton_11.setGeometry(QtCore.QRect(220, 250, 51, 41))
        self.pushButton_11.setText(_fromUtf8(""))
        self.pushButton_11.setIcon(icon)
        self.pushButton_11.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setEnabled(False)
        self.tab_7.setObjectName(_fromUtf8("tab_7"))
        self.mplwidget_3 = MayaviQWidget(self.tab_7)
        self.mplwidget_3.setGeometry(QtCore.QRect(15, 10, 261, 191))
        self.mplwidget_3.setObjectName(_fromUtf8("mplwidget_3"))
        self.seekSlider1 = phonon.Phonon.SeekSlider(self.tab_7)
        self.seekSlider1.setEnabled(False)
        self.seekSlider1.setGeometry(QtCore.QRect(10, 180, 260, 90))
        self.seekSlider1.setAcceptDrops(True)
        self.seekSlider1.setIconVisible(False)
        self.seekSlider1.setObjectName(_fromUtf8("seekSlider1"))
        self.tabWidget.addTab(self.tab_7, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(20, 107, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Mean. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(20, 76, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Max. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(20, 34, 91, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Min. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(20, 10, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Sensor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(20, 166, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(20, 134, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Gain", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.line = QtGui.QFrame(self.tab_3)
        self.line.setGeometry(QtCore.QRect(20, 30, 240, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(self.tab_3)
        self.line_2.setGeometry(QtCore.QRect(20, 62, 240, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.line_3 = QtGui.QFrame(self.tab_3)
        self.line_3.setGeometry(QtCore.QRect(20, 94, 240, 16))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.line_4 = QtGui.QFrame(self.tab_3)
        self.line_4.setGeometry(QtCore.QRect(20, 125, 240, 16))
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.line_6 = QtGui.QFrame(self.tab_3)
        self.line_6.setGeometry(QtCore.QRect(18, 184, 240, 16))
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.line_7 = QtGui.QFrame(self.tab_3)
        self.line_7.setGeometry(QtCore.QRect(19, 157, 240, 10))
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox.setGeometry(QtCore.QRect(170, 14, 91, 22))
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox.setDecimals(0)
        self.doubleSpinBox.setMinimum(2.0)
        self.doubleSpinBox.setMaximum(128.0)
        self.doubleSpinBox.setSingleStep(2.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(170, 44, 91, 22))
        self.doubleSpinBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_2.setDecimals(0)
        self.doubleSpinBox_2.setMinimum(900.0)
        self.doubleSpinBox_2.setMaximum(1500.0)
        self.doubleSpinBox_2.setSingleStep(100.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(170, 77, 91, 22))
        self.doubleSpinBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_3.setDecimals(0)
        self.doubleSpinBox_3.setMinimum(900.0)
        self.doubleSpinBox_3.setMaximum(1500.0)
        self.doubleSpinBox_3.setSingleStep(100.0)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(170, 108, 91, 22))
        self.doubleSpinBox_4.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_4.setDecimals(0)
        self.doubleSpinBox_4.setMinimum(900.0)
        self.doubleSpinBox_4.setMaximum(1500.0)
        self.doubleSpinBox_4.setSingleStep(100.0)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.doubleSpinBox_5 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_5.setGeometry(QtCore.QRect(170, 137, 91, 22))
        self.doubleSpinBox_5.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_5.setDecimals(0)
        self.doubleSpinBox_5.setMinimum(1.0)
        self.doubleSpinBox_5.setMaximum(5.0)
        self.doubleSpinBox_5.setSingleStep(1.0)
        self.doubleSpinBox_5.setProperty("value", 1.0)
        self.doubleSpinBox_5.setObjectName(_fromUtf8("doubleSpinBox_5"))
        self.doubleSpinBox_6 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_6.setGeometry(QtCore.QRect(170, 170, 91, 20))
        self.doubleSpinBox_6.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_6.setDecimals(0)
        self.doubleSpinBox_6.setMinimum(1.0)
        self.doubleSpinBox_6.setMaximum(5.0)
        self.doubleSpinBox_6.setSingleStep(1.0)
        self.doubleSpinBox_6.setProperty("value", 1.0)
        self.doubleSpinBox_6.setObjectName(_fromUtf8("doubleSpinBox_6"))
        self.pushButton = QtGui.QPushButton(self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(210, 212, 51, 41))
        self.pushButton.setText(_fromUtf8(""))
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.tab_3)
        self.pushButton_2.setGeometry(QtCore.QRect(155, 212, 51, 41))
        self.pushButton_2.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384157920_208014.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.tab_3)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 212, 51, 41))
        self.pushButton_3.setText(_fromUtf8(""))
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(710, 510, 46, 13))
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(680, 520, 321, 81))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("icon/logo(1).png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Capasitance", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QtGui.QApplication.translate("Dialog", "Sensitivity", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Dialog", "Setting", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import phonon
from matplotlibwidget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())