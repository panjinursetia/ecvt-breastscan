"""
@author: Afsar
This is the Implementation logic for Hello World! (hw.py)
"""
from PyQt4 import QtCore,QtGui
import sys
import hw
class hwl(QtGui.QDialog,hw.Ui_Dialog):
    """
    hwl is inherited from both QtGui.QDialog and hw.Ui_Dialog
    """
    def __init__(self,parent=None):
        """
            Initialization of the class. Call the __init__ for the super classes
        """
        super(hwl,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
    def main(self):
        self.show()
    def connectActions(self):
        """
        Connect the user interface controls to the logic
        """
        self.cmdWrite.clicked.connect(self.myprint)      
        
    def myprint(self):
        """
        Even handler for the pushButton click
        """
        self.txtLine.setText('Python -- ')        
        self.txtEdit.setText('This')
        self.lblShow.setText('is a test')
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    hwl1 = hwl()
    hwl1.main()
    sys.exit(app.exec_())