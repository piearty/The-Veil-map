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

      self.edgesList = []

      #two buttons, the first one runs the add_button_clicked function and the second one exits the program
      addingButton = QPushButton("Add")
      addingButton.setCheckable(True)

      editingButton = QPushButton("Edit")
      editingButton.setCheckable(True)
      editingButton.setEnabled(False)

      deletingButton = QPushButton("Delete")
      deletingButton.setCheckable(True)
      deletingButton.setEnabled(False)
      
      savingButton = QPushButton("Save")
      savingButton.setCheckable(True)

      edgeButtonsBox = QDialogButtonBox()
      edgeButtonsBox.addButton(addingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(editingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(deletingButton, QDialogButtonBox.ActionRole)      
      
      addingButton.clicked.connect(self.add_button_clicked)
  #    editingButton.clicked.connect(self.edit_button_clicked)
   #   deletingButton.clicked.connect(self.del_button_clicked)

      saveButtonBox = QDialogButtonBox()
      saveButtonBox.addButton(savingButton, QDialogButtonBox.ActionRole)

      savingButton.clicked.connect(self.save_button_clicked)

      grid = QGridLayout()
      grid.addWidget(self.namesBoxGroup(), 0, 0)
      grid.addWidget(self.obligationsBoxGroup(), 1,0)
      grid.addWidget(self.statesBoxGroup(), 0, 1)
      grid.addWidget(edgeButtonsBox, 2, 0)
      grid.addWidget(saveButtonBox, 3, 1)

      self.setLayout(grid)

   def radioMaker(self, label, buttonsList):
      radioBox = QGroupBox(label)
      radioLayout = QVBoxLayout()
      radioButtons = [QRadioButton(b) for b in buttonsList]
      radioButtons[0].setChecked(True)   
      self.radioButtonsGroup = QButtonGroup()
      for i, self.button in enumerate(radioButtons):
         radioLayout.addWidget(self.button)
         self.radioButtonsGroup.addButton(radioButtons[i])

      
      radioBox.setLayout(radioLayout)

      return radioBox

   def namesBoxGroup(self):
      namesBox = QGroupBox('Names')
      sourceLabel = QLabel('Starting Person')
      self.sourceLine = QLineEdit()
      targetLabel = QLabel('Ending Person')
      self.targetLine = QLineEdit()
      namesLayout = QVBoxLayout()
      namesLayout.addWidget(sourceLabel)
      namesLayout.addWidget(self.sourceLine)
      namesLayout.addWidget(targetLabel)
      namesLayout.addWidget(self.targetLine)
      
      namesBox.setLayout(namesLayout)

      return namesBox

   def statesBoxGroup(self):
      states = ['joyful', 'angry', 'powerful', 'peaceful', 'sad', 'scared']
      
      return self.radioMaker('State', states) 

   def obligationsBoxGroup(self):
      obligationBox = QGroupBox('Obligations owed to starting person')
      self.obligationLine = QLineEdit()
      obligationBoxLayout = QVBoxLayout()
      obligationBoxLayout.addWidget(self.obligationLine)
      
      obligationBox.setLayout(obligationBoxLayout)

      return obligationBox

   def add_button_clicked(self):
      #sets variables then clears the text fields when applicable
      source = self.sourceLine.text()
      self.sourceLine.setText('')
      target = self.targetLine.text()
      self.targetLine.setText('')
      state = self.radioButtonsGroup.checkedButton().text()
      obligation = self.obligationLine.text()
      self.obligationLine.setText('')
      if source and target:
         connectionObject = graph.Connection(source, target, state, obligation)
         print(graph.listConnection(connectionObject))
         print(self.edgesList)


   def save_button_clicked(self):
      for edge in self.edgesList:
         print(edge)
         graph.addEdge(edge)
         print(graph.g.edges())
         #p = graph.to_pydot(graph.g)
         #p.write_png('test.png', prog='dot')



def main():

   app = QApplication(sys.argv)
   ex = VeilGUI()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()