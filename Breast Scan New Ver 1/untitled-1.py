from __future__ import unicode_literals
import os
os.environ['ETS_TOOLKIT'] = 'qt4'

#from pyface.qt import QtGui, QtCore
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
from CONVERTNSM import *
import matplotlib.gridspec as gridspec
from appLib import *
from ecvtlib import *
import h5py
from mayavi import *

#progname = os.path.basename(sys.argv[0])
#progversion = "0.1"

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    button = Button('Plot')
  
	    
    def ambil_data_scan(self):
        sm_data=h5py.File('sm32.h5')
	v_data = h5py.File('Data/mam-dex_Siti-azizah_11656_8september2014.h5')
	
	an3d=array(sm_data['an3d'])    
	ant3d=array(sm_data['ant3d'])
	Ve=array(v_data['Ve'])
	Vf=array(v_data['Vf'])
	Vr=array(v_data['Vr'])	
	
        s = ecvt_mat(Ve,Vf,Vr,an3d,ant3d)
	return s
    
    def vessel(self):
	sm_data=h5py.File('sm32.h5')
	v_data = h5py.File('Data/mam-dex_Siti-azizah_11656_8september2014.h5')
	
	an3d=array(sm_data['an3d'])    
	ant3d=array(sm_data['ant3d'])
	Ve=array(v_data['Ve'])
	Vf=array(v_data['Vf'])
	Vr=array(v_data['Vr'])	
	
	s = ecvt_mat(Ve,Vf,Vf,an3d,ant3d)
	return s   
	
     
    
    @on_trait_change('scene.activated')    
    def update_plot(self):   
	
        self.s = self.ambil_data_scan()
	self.s1 = self.vessel()
        self.src = mlab.pipeline.scalar_field(self.s, 
                                         scaling=(1, 1, 1), 
                                         origin=(1,1,1))
        
        self.src.spacing = [1, 1, 0.75]
        
        #iso surface
        self.m=mlab.pipeline.iso_surface(self.src,contours=10,opacity=0.3)          
        #m.module_manager.scalar_lut_manager.show_scalar_bar = True
	self.src1 = mlab.pipeline.scalar_field(self.s1,scaling=(1, 1, 1),origin=(1,1,1))
	self.src1.spacing = [1, 1, 0.75] 
	self.m1=mlab.pipeline.iso_surface(self.src1,contours=[self.s1.min()+0.01*self.s1.ptp(), ],opacity=0.1) 
        
        
        self.mlab.colorbar(orientation='horizontal') 
        self.mlab.show() 
    

    
    # the layout of the dialog screated
    view = View(Item('scene',editor=SceneEditor(scene_class=MayaviScene),
                     height=100, width=200, show_label=False),
                'button',
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
    def clearPlt(self):
	self.visualization.update_plot()
	
	
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=2, height=2, dpi=100):
	fig = Figure(figsize=(width, height), dpi=dpi)	
	self.axes = fig.add_subplot(111)
	#self.axes2 = fig.add_subplot(112)
	
	
	
	for label in (self.axes.get_xticklabels() + self.axes.get_yticklabels()):
		label.set_fontname('Arial')
		label.set_fontsize(4)  
		
	self.axes.xlim = (0,100)
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
class Kalibrasi(MyMplCanvas):     
    def compute_initial_figure(self):	 
	self.ve = gen_mat(180,0,0)
	self.axes.grid(True)
	self.line_kalibrasi_empty, = self.axes.plot(self.ve,'r', label="Ve")     
    def update_figure(self, calIndex, data):		
	if calIndex == 0:
	    self.ve = data 
	    self.axes.grid(True)
	    self.line_kalibrasi_empty, = self.axes.plot(self.ve,'r', label="Ve") 
	    self.draw()  
	    
	elif calIndex == 1:
	    self.vf = data 
	    self.axes.grid(True)
	    self.line_kalibrasi_empty, = self.axes.plot(self.vf,'b', label="Vf") 
	    self.draw() 
	    
class Kapasitansi(MyMplCanvas):     
    def compute_initial_figure(self):	 
	self.ve = gen_mat(180,0,0)
	self.vf = gen_mat(180,0,0)
	self.axes.grid(True)
	self.line_kalibrasi_empty = self.axes.plot(self.ve,'r',self.vf,'b' )
	#self.line_kalibrasi_full, = self.axes2.plot(self.vf,'b', label="Vf")
	
    def update_figure(self, ve, vf):		
	self.ve = ve
	self.vf = vf
	self.axes.grid(True)
	self.line_kalibrasi_empty = self.axes.plot(self.ve,'r',self.vf,'b' )
	#self.line_kalibrasi_full, = self.axes.plot(self.vf,'b', label="Vf") 
	self.draw()  
	

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1335, 657)
        Dialog.setWindowTitle(QtGui.QApplication.translate("CTX-Breast Scan", "CTX-Breast Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(39, 30, 691, 601))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox.setFont(font)
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "3D View", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.mplwidget_4 = MayaviQWidget(self.groupBox)
        self.mplwidget_4.setGeometry(QtCore.QRect(10, 30, 661, 561))
        self.mplwidget_4.setObjectName(_fromUtf8("mplwidget_4"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(760, 34, 551, 501))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Data Acquisition System", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.tabWidget = QtGui.QTabWidget(self.groupBox_2)
        self.tabWidget.setGeometry(QtCore.QRect(30, 50, 501, 431))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tabWidget.setFont(font)
        self.tabWidget.setWhatsThis(QtGui.QApplication.translate("Dialog", "sdsda", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.mplwidget = Kapasitansi(self.tab)
        self.mplwidget.setGeometry(QtCore.QRect(12, 11, 471, 331))
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.pushButton_7 = QtGui.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(374, 351, 51, 41))
        self.pushButton_7.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384157972_174920.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon)
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(317, 351, 51, 41))
        self.pushButton_8.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384157809_208018.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon1)
        self.pushButton_8.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_9 = QtGui.QPushButton(self.tab)
        self.pushButton_9.setGeometry(QtCore.QRect(430, 350, 51, 41))
        self.pushButton_9.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384349057_103529.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon2)
        self.pushButton_9.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.mplwidget_2 = Kalibrasi(self.tab_2)
        self.mplwidget_2.setGeometry(QtCore.QRect(11, 10, 471, 311))
        self.mplwidget_2.setObjectName(_fromUtf8("mplwidget_2"))
        self.comboBox = QtGui.QComboBox(self.tab_2)
        self.comboBox.setGeometry(QtCore.QRect(370, 330, 111, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Empty Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Full Calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "Warming Das", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16 = QtGui.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(218, 327, 141, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_16.setFont(font)
        self.label_16.setText(QtGui.QApplication.translate("Dialog", "Calibration Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.pushButton_10 = QtGui.QPushButton(self.tab_2)
        self.pushButton_10.setGeometry(QtCore.QRect(373, 360, 51, 41))
        self.pushButton_10.setText(_fromUtf8(""))
        self.pushButton_10.setIcon(icon1)
        self.pushButton_10.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.pushButton_11 = QtGui.QPushButton(self.tab_2)
        self.pushButton_11.setGeometry(QtCore.QRect(430, 360, 51, 41))
        self.pushButton_11.setText(_fromUtf8(""))
        self.pushButton_11.setIcon(icon)
        self.pushButton_11.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setEnabled(False)
        self.tab_7.setObjectName(_fromUtf8("tab_7"))
        self.mplwidget_3 = MatplotlibWidget(self.tab_7)
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
        self.label_4.setGeometry(QtCore.QRect(30, 115, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Mean. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(30, 84, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Max. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(30, 42, 91, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Min. Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(30, 18, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Sensor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(30, 174, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(30, 142, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Gain", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.line = QtGui.QFrame(self.tab_3)
        self.line.setGeometry(QtCore.QRect(29, 38, 451, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(self.tab_3)
        self.line_2.setGeometry(QtCore.QRect(29, 70, 451, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.line_3 = QtGui.QFrame(self.tab_3)
        self.line_3.setGeometry(QtCore.QRect(29, 102, 451, 20))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.line_4 = QtGui.QFrame(self.tab_3)
        self.line_4.setGeometry(QtCore.QRect(29, 133, 451, 20))
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.line_6 = QtGui.QFrame(self.tab_3)
        self.line_6.setGeometry(QtCore.QRect(27, 192, 451, 20))
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.line_7 = QtGui.QFrame(self.tab_3)
        self.line_7.setGeometry(QtCore.QRect(28, 165, 451, 20))
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox.setGeometry(QtCore.QRect(390, 22, 91, 22))
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox.setDecimals(0)
        self.doubleSpinBox.setMinimum(2.0)
        self.doubleSpinBox.setMaximum(128.0)
        self.doubleSpinBox.setSingleStep(2.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(390, 52, 91, 22))
        self.doubleSpinBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_2.setDecimals(0)
        self.doubleSpinBox_2.setMinimum(900.0)
        self.doubleSpinBox_2.setMaximum(1500.0)
        self.doubleSpinBox_2.setSingleStep(100.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(390, 85, 91, 22))
        self.doubleSpinBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_3.setDecimals(0)
        self.doubleSpinBox_3.setMinimum(900.0)
        self.doubleSpinBox_3.setMaximum(1500.0)
        self.doubleSpinBox_3.setSingleStep(100.0)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(390, 116, 91, 22))
        self.doubleSpinBox_4.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_4.setDecimals(0)
        self.doubleSpinBox_4.setMinimum(900.0)
        self.doubleSpinBox_4.setMaximum(1500.0)
        self.doubleSpinBox_4.setSingleStep(100.0)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.doubleSpinBox_5 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_5.setGeometry(QtCore.QRect(390, 145, 91, 22))
        self.doubleSpinBox_5.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_5.setDecimals(0)
        self.doubleSpinBox_5.setMinimum(1.0)
        self.doubleSpinBox_5.setMaximum(5.0)
        self.doubleSpinBox_5.setSingleStep(1.0)
        self.doubleSpinBox_5.setProperty("value", 1.0)
        self.doubleSpinBox_5.setObjectName(_fromUtf8("doubleSpinBox_5"))
        self.doubleSpinBox_6 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_6.setGeometry(QtCore.QRect(390, 178, 91, 20))
        self.doubleSpinBox_6.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_6.setDecimals(0)
        self.doubleSpinBox_6.setMinimum(1.0)
        self.doubleSpinBox_6.setMaximum(5.0)
        self.doubleSpinBox_6.setSingleStep(1.0)
        self.doubleSpinBox_6.setProperty("value", 1.0)
        self.doubleSpinBox_6.setObjectName(_fromUtf8("doubleSpinBox_6"))
        self.pushButton = QtGui.QPushButton(self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(430, 290, 51, 41))
        self.pushButton.setText(_fromUtf8(""))
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.tab_3)
        self.pushButton_2.setGeometry(QtCore.QRect(375, 290, 51, 41))
        self.pushButton_2.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("icon/1384157920_208014.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.tab_3)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 290, 51, 41))
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
        self.label_2.setGeometry(QtCore.QRect(890, 540, 411, 81))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("icon/logo(1).png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.actionOpenFile = QtGui.QAction(Dialog)
        self.actionOpenFile.setText(QtGui.QApplication.translate("Dialog", "OpenFile", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenFile.setToolTip(QtGui.QApplication.translate("Dialog", "Buka Data Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenFile.setObjectName(_fromUtf8("actionOpenFile"))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton_9, QtCore.SIGNAL(_fromUtf8("pressed()")), self.mplwidget_4.show)
        QtCore.QObject.connect(self.pushButton_8, QtCore.SIGNAL(_fromUtf8("pressed()")), self.mplwidget.update)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.comboBox.update)
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
