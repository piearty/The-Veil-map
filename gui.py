#lets app accept command line arguments
import sys

#imports the gui aspect of pyqt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class VeilGui(QWidget):

   def __init__(self, parent = None):
      super().__init__(parent)
      self.setWindowTitle('Veil Relationship Map GUI')

      grid = QGridLayout()
      grid.addWidget(self.namesBoxGroup(), 0, 0)
      grid.addWidget(self.statesBoxGroup(), 0, 1)

      self.setLayout(grid)

   def namesBoxGroup(self):
      namesBox = QGroupBox('Names')
      sourceLabel = QLabel('Person')
      sourceLine = QLineEdit()
      targetLabel = QLabel('Target')
      targetLine = QLineEdit()
      namesLayout = QVBoxLayout()
      namesLayout.addWidget(sourceLabel)
      namesLayout.addWidget(sourceLine)
      namesLayout.addWidget(sourceLine)
      namesLayout.addWidget(targetLabel)
      namesLayout.addWidget(targetLine)
      
      namesBox.setLayout(namesLayout)

      return namesBox

   def statesBoxGroup(self):
      statesBox = QGroupBox('State')
      states = ['joyful', 'angry', 'powerful', 'peaceful', 'sad', 'scared']
      statesLayout = QVBoxLayout()
      statesButtons = [QRadioButton(s) for s in states]
      for i, button in enumerate(statesButtons):
         statesLayout.addWidget(button)
         if i == 0:
            button.setChecked(True)
      statesBox.setLayout(statesLayout)

      return statesBox

      

def main():

   app = QApplication(sys.argv)
   ex = VeilGui()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()