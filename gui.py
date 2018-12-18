#lets app accept command line arguments
import sys

#imports the gui aspect of pyqt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import graph



class VeilGUI(QDialog):

   def __init__(self, parent = None):
      super(VeilGUI, self).__init__(parent)
      self.setWindowTitle('Veil Relationship Map GUI')

      #two buttons, the first one runs the run_button_clicked function and the second one exits the program
      buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
      buttonBox.accepted.connect(self.run_button_clicked)
      buttonBox.rejected.connect(self.reject)

      grid = QGridLayout()
      grid.addWidget(self.namesBoxGroup(), 0, 0)
      grid.addWidget(self.statesBoxGroup(), 0, 1)
      grid.addWidget(buttonBox)

      self.setLayout(grid)

   def radioMaker(self, label, buttonsList):
      radioBox = QGroupBox(label)
      radioLayout = QVBoxLayout()
      radioButtons = [QRadioButton(b) for b in buttonsList]
      self.radioButtonsGroup = QButtonGroup()
      for i, self.button in enumerate(radioButtons):
         radioLayout.addWidget(self.button)
         if i == 0:
            self.button.setChecked(True)
         self.radioButtonsGroup.addButton(radioButtons[i])
            # Add each radio self.button to the self.button group & give it an ID of i
         self.radioButtonsGroup.addButton(radioButtons[i], i)
            # Connect each radio self.button to a method to run when it's clicked
         self.button.clicked.connect(self.radio_button_clicked)
      
      radioBox.setLayout(radioLayout)

      return radioBox

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
      states = ['joyful', 'angry', 'powerful', 'peaceful', 'sad', 'scared']
      return self.radioMaker('State', states) 



   def radio_button_clicked(self):
      self.statePressed = print(self.radioButtonsGroup.checkedButton().text())

   def run_button_clicked(self):
      source = self.sourceLine.text()
      target = self.targetLine.text()
      state = self.statePressed
      return graph.Connection(source, target, state)
      

def main():

   app = QApplication(sys.argv)
   ex = VeilGUI()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()