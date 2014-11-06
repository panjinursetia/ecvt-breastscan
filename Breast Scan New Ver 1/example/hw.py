# -*- coding: utf-8 -*- hw.py

# Form implementation generated from reading ui file 'hw.ui'
#
# Created: Sat Aug 11 14:06:40 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(368, 319)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdClear = QtGui.QPushButton(Dialog)
        self.cmdClear.setGeometry(QtCore.QRect(140, 10, 75, 23))
        self.cmdClear.setText(QtGui.QApplication.translate("Dialog", "Clear!", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdClear.setObjectName(_fromUtf8("cmdClear"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(60, 100, 258, 213))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtEdit = QtGui.QTextEdit(self.widget)
        self.txtEdit.setObjectName(_fromUtf8("txtEdit"))
        self.verticalLayout.addWidget(self.txtEdit)
        self.lblShow = QtGui.QLabel(self.widget)
        self.lblShow.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblShow.setObjectName(_fromUtf8("lblShow"))
        self.verticalLayout.addWidget(self.lblShow)
        self.widget1 = QtGui.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(80, 50, 216, 25))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtLine = QtGui.QLineEdit(self.widget1)
        self.txtLine.setObjectName(_fromUtf8("txtLine"))
        self.horizontalLayout.addWidget(self.txtLine)
        self.cmdWrite = QtGui.QPushButton(self.widget1)
        self.cmdWrite.setText(QtGui.QApplication.translate("Dialog", "Write!", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdWrite.setObjectName(_fromUtf8("cmdWrite"))
        self.horizontalLayout.addWidget(self.cmdWrite)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cmdClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.txtLine.clear)
        QtCore.QObject.connect(self.cmdClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.txtEdit.clear)
        QtCore.QObject.connect(self.cmdClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lblShow.clear)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())