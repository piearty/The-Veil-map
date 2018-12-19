#this creates the gui to interface with the graph.py function

#lets app accept command line arguments
import sys

#imports the gui aspect of pyqt
from PyQt5 import QtCore, QtWidgets, Qt
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

      #dict to contain radio boxes created later
      self.radioButtonsDict = {}

      #creates the grid where the widgets will be placed
      grid = QGridLayout()

      #adds widgets
      grid.addWidget(self.namesBoxGroup(), 0, 0)
      grid.addWidget(self.obligationsBoxGroup(), 1,0)
      grid.addWidget(self.statesBoxGroup(), 0, 1)
      grid.addWidget(self.tenorBoxGroup(), 1, 1)
      grid.addWidget(self.lineBoxGroup(), 2, 0)
      grid.addWidget(self.addButtonGroup(), 2, 1)
      grid.addWidget(self.edgeComboBoxGroup(), 3, 0, 1, 2)
      grid.addWidget(self.edgeButtonsGroup(), 4,0)
      grid.addWidget(self.saveButtonGroup(), 4, 1)


      #creates grid
      self.setLayout(grid)

   #
   def radioMaker(self, group, label, buttonsList):
      radioBox = QGroupBox(label)
      radioLayout = QVBoxLayout()
      radioButtons = [QRadioButton(b) for b in buttonsList]
      radioButtons[0].setChecked(True)
      self.radioButtonsDict.update({group:QButtonGroup()})
      for i, self.button in enumerate(radioButtons):
         radioLayout.addWidget(self.button)
         self.radioButtonsDict[group].addButton(radioButtons[i])

      radioBox.setLayout(radioLayout)

      return radioBox

   def addButtonGroup(self):
      #creates button labeled add
      addingButton = QPushButton("Add Connection")
      addingButton.setCheckable(True)

      #box containing add button
      addingButtonBox = QDialogButtonBox()
      addingButtonBox.addButton(addingButton, QDialogButtonBox.ActionRole)

      #when clicked, run the add_button_clicked, edit_button_clicked, and del_button_clicked methods respectively
      addingButton.clicked.connect(self.add_button_clicked)

      return addingButtonBox

   def edgeButtonsGroup(self):
      #creates buttons labeled edit, and delete
      self.editingButton = QPushButton("Edit")
      self.editingButton.setCheckable(True)
      self.editingButton.setEnabled(False)

      self.deletingButton = QPushButton("Delete")
      self.deletingButton.setCheckable(True)
      self.deletingButton.setEnabled(False)

      #box containing edit, and delete buttons (these modify the edges)
      edgeButtonsBox = QDialogButtonBox()
      edgeButtonsBox.addButton(self.editingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(self.deletingButton, QDialogButtonBox.ActionRole)      
      
  #    self.editingButton.clicked.connect(self.edit_button_clicked)
      self.deletingButton.clicked.connect(self.del_button_clicked)

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

   #box for the names of the source and target
   def namesBoxGroup(self):
      #labels box
      namesBox = QGroupBox('Names')
      #creates source line field and labels it
      sourceLabel = QLabel('Starting Person')
      self.sourceLine = QLineEdit()
      #creates target source line field and labels it
      targetLabel = QLabel('Ending Person')
      self.targetLine = QLineEdit()
      #creates layout
      namesLayout = QVBoxLayout()
      #adds line fields and labels to layout
      namesLayout.addWidget(sourceLabel)
      namesLayout.addWidget(self.sourceLine)
      namesLayout.addWidget(targetLabel)
      namesLayout.addWidget(self.targetLine)
      
      #sets box as layout
      namesBox.setLayout(namesLayout)

      return namesBox

   def statesBoxGroup(self):
      states = ['joyful', 'angry', 'powerful', 'peaceful', 'sad', 'scared']
      
      return self.radioMaker('stateGroup', 'State', states) 

   def tenorBoxGroup(self):
      tenors = ['toward', 'for']

      return self.radioMaker('tenorGroup', 'Tenor of state', tenors)

   def lineBoxGroup(self):
      lines = ['strong', 'tenuous']

      return self.radioMaker('lineGroup', 'Strength of relationship', lines)

   def obligationsBoxGroup(self):
      obligationBox = QGroupBox('Obligations owed')
      self.obligationLabel = QLabel('Enter integer:')
      self.obligationSpinBox = QSpinBox()
      obligationBoxLayout = QVBoxLayout()
      obligationBoxLayout.addWidget(self.obligationSpinBox)
      
      obligationBox.setLayout(obligationBoxLayout)

      return obligationBox

   def edgeComboBoxGroup(self):
      edgeComboBox = QGroupBox('List of connections')
      self.edgeCombo = QComboBox()
      edgeComboBoxLayout = QHBoxLayout()
      edgeComboBoxLayout.addWidget(self.edgeCombo)
      edgeComboBox.setLayout(edgeComboBoxLayout)

      self.edgeCombo.currentIndexChanged.connect(self.buttons_enabled)

      return edgeComboBox
   
   #### METHODS ####


   def buttons_enabled(self):
      if self.edgesList:
         self.editingButton.setEnabled(True)
         self.deletingButton.setEnabled(True)


   def add_button_clicked(self):
      #sets variables then clears the text fields when applicable
      source = self.sourceLine.text()
      self.sourceLine.setText('')
      
      target = self.targetLine.text()
      self.targetLine.setText('')
      
      if self.obligationSpinBox.value() != 0:
         obligation = self.obligationSpinBox.value()
      else:
         obligation = None

      state = self.radioButtonsDict['stateGroup'].checkedButton().text()

      tenor = self.radioButtonsDict['tenorGroup'].checkedButton().text()
      
      line = self.radioButtonsDict['lineGroup'].checkedButton().text()

      if source and target:
         connectionObject = graph.Connection(source, target, state, obligation, tenor, line)
         self.edgesList.append(connectionObject)
         connectionsList = graph.listConnection(connectionObject)
         self.edgeCombo.addItem(connectionsList[0]+' to '+connectionsList[1])

   def del_button_clicked(self):
      refNum = self.edgeCombo.currentIndex()
      graph.removeEdge(self.edgesList[refNum])
      self.edgesList.pop(refNum)
      self.edgeCombo.removeItem(refNum)

   
   def save_button_clicked(self):
      for edge in self.edgesList:
         graph.addEdge(edge)
         p = graph.to_pydot(graph.g)
         p.write_png('test.png', prog='dot')



def main():

   app = QApplication(sys.argv)
   ex = VeilGUI()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()