#this creates the gui to interface with the graph.py function

#lets app accept command line arguments
import sys

#imports the gui aspect of pyqt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#imports graph.py
import graph


#class that is the gui
class VeilGUI(QDialog):

   def __init__(self, parent = None):
      super(VeilGUI, self).__init__(parent)
      
      #names gui window
      self.setWindowTitle('Veil Relationship Map GUI')

      #list to contain edges created later
      self.edgesList = []

      #creates the grid where the widgets will be placed
      grid = QGridLayout()

      #adds widgets
      grid.addWidget(self.namesBoxGroup(), 0, 0)
      grid.addWidget(self.obligationsBoxGroup(), 1,0)
      grid.addWidget(self.statesBoxGroup(), 0, 1)
      grid.addWidget(self.edgeButtonsGroup(), 2, 0)
      grid.addWidget(self.saveButtonGroup(), 3, 1)

      #creates grid
      self.setLayout(grid)

   #
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

   def edgeButtonsGroup(self):
      #creates buttons labeled add, edit, and delete
      addingButton = QPushButton("Add")
      addingButton.setCheckable(True)

      editingButton = QPushButton("Edit")
      editingButton.setCheckable(True)
      editingButton.setEnabled(False)

      deletingButton = QPushButton("Delete")
      deletingButton.setCheckable(True)
      deletingButton.setEnabled(False)

      #box containing add, edit, and delete buttons (these modify the edges)
      edgeButtonsBox = QDialogButtonBox()
      edgeButtonsBox.addButton(addingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(editingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(deletingButton, QDialogButtonBox.ActionRole)      
      
      #when clicked, run the add_button_clicked, edit_button_clicked, and del_button_clicked methods respectively
      #latter two not implemented yet :'(
      addingButton.clicked.connect(self.add_button_clicked)
  #    editingButton.clicked.connect(self.edit_button_clicked)
   #   deletingButton.clicked.connect(self.del_button_clicked)

      return edgeButtonsBox
      

   def saveButtonGroup(self):

      #creates button labeled save
      savingButton = QPushButton("Save")
      savingButton.setCheckable(True)

      #box containing save button
      self.saveButtonBox = QDialogButtonBox()
      self.saveButtonBox.addButton(savingButton, QDialogButtonBox.ActionRole)

      #when clicked, runs the save_button_clicked method
      savingButton.clicked.connect(self.save_button_clicked)

      return self.saveButtonBox

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
         #print(self.edgesList)


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