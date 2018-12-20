# this creates the gui to interface with the graph.py function

# lets app accept command line arguments
import sys

# imports the gui aspect of pyqt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# imports graph.py
import graph

# class that is the gui
class VeilGUI(QDialog):

   def __init__(self, parent = None):
      super(VeilGUI, self).__init__(parent)
      
      # names gui window
      self.setWindowTitle('Veil Relationship Map GUI')

      # list to contain edges created later
      self.edgesList = []

      # dict to contain radio boxes created later
      self.radioButtonsDict = {}

      # list to contain saved edges created later
      self.savedEdgesList = []

      # creates the grid where the widgets will be placed
      grid = QGridLayout()

      # save_buttons widgets
      # names widget (text field for source and target/node names)
      grid.addWidget(self.namesBoxGroup(), 0, 0)
      # obligations widget (integer spin box for obligation/edge label)
      grid.addWidget(self.obligationsBoxGroup(), 1,0)
      # states widget (radio buttons for states/color of label)
      grid.addWidget(self.statesBoxGroup(), 0, 1)
      # tenor widget (radio buttons for tenors/arrowhead shape)
      grid.addWidget(self.tenorBoxGroup(), 1, 1)
      # lines widget (radio buttons for strength of relationship/edge style)
      grid.addWidget(self.lineBoxGroup(), 2, 0)
      # save_button button (for save connection)
      grid.addWidget(self.saveButtonGroup(), 2, 1)
      # map widget (to show png)
      grid.addWidget(self.showMap(), 0, 3, 3, 3)
      # combo box widget (to show edge list)
      grid.addWidget(self.edgeComboBoxGroup(), 3, 0, 1, 2)
      # save button (for writing to png)
    #  grid.addWidget(self.saveButtonGroup(), 4, 1)
      # edge buttons (for editing or deleting edges)
      grid.addWidget(self.edgeButtonsGroup(), 4,0)


      # creates grid layout
      self.setLayout(grid)

   # creates radio buttons automatically instead of having to list them one by one
   # takes the name of the group (so you can reference each radio button group separately),
   # label text that the radio button group will be labeled
   # list of items you want to be made into radio buttons
   def radioMaker(self, group, label, buttonsList):
      # creates group box
      radioBox = QGroupBox(label)
      # makes a vertical layout
      radioLayout = QVBoxLayout()
      # for button in list, make radio button and put it in radioButtons list
      radioButtons = [QRadioButton(b) for b in buttonsList]
      # set the first radio button as the default button checked
      radioButtons[0].setChecked(True)
      # makes a smol (one key) dictionary, radioButtonsDict
      # with a key determined by the argument passed to 'group' parameter
      # and its value being a QButtonGroup
      # effectively naming the QButtonGroup and allowing it to be uniquely referenced outside of this method
      # # # # (QButtonGroup.checkedButton().text() outputs the text of the button that was selected
      # # # # within QButtonGroup
      # # # # instead of treating each button as separate)
      self.radioButtonsDict.update({group:QButtonGroup()})
      # for every button in radioButtons
      for i, self.button in enumerate(radioButtons):
         # put the widget in radioLayout
         radioLayout.addWidget(self.button)
         # and adds a button to the QButtonGroup in the radioButtonsDict
         self.radioButtonsDict[group].addButton(radioButtons[i])

      #set the group box's layout as radioLayout
      radioBox.setLayout(radioLayout)

      #returns the group box
      return radioBox

   def saveButtonGroup(self):
      # creates button labeled Save Connection
      saveButton = QPushButton("Save Connection")
      saveButton.setCheckable(True)

      # box containing save button
      saveButtonBox = QDialogButtonBox()
      saveButtonBox.addButton(saveButton, QDialogButtonBox.ActionRole)

      # when clicked, run the save_button_clicked method respectively
      saveButton.clicked.connect(self.save_button_clicked)

      return saveButtonBox

   def edgeButtonsGroup(self):
      # creates buttons labeled edit, and delete, but makes it so they can't be clicked on yet
      self.editingButton = QPushButton("Edit")
      self.editingButton.setCheckable(True)
      self.editingButton.setEnabled(False)

      self.deletingButton = QPushButton("Delete")
      self.deletingButton.setCheckable(True)
      self.deletingButton.setEnabled(False)

      # box containing edit and delete buttons (these modify the edges)
      edgeButtonsBox = QDialogButtonBox()
      edgeButtonsBox.addButton(self.editingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(self.deletingButton, QDialogButtonBox.ActionRole)      
      
      # below is code that's not implemented yet
      # self.editingButton.clicked.connect(self.edit_button_clicked)

      # when delete button is clicked, run the delete button method
      # also run buttons_enabled method
      self.deletingButton.clicked.connect(self.del_button_clicked)
      #self.deletingButton.clicked.connect(self.buttons_enabled)

      return edgeButtonsBox

   # box for the names of the source and target
   # this determines the names of the first and second node, and creates a default edge/line between them
   def namesBoxGroup(self):
      # labels box
      namesBox = QGroupBox('Names')
      # creates source line field and labels it
      sourceLabel = QLabel('Starting Person')
      self.sourceLine = QLineEdit()
      # creates target source line field and labels it
      targetLabel = QLabel('Ending Person')
      self.targetLine = QLineEdit()
      # creates layout
      namesLayout = QVBoxLayout()
      # save_buttons line fields and labels to layout
      namesLayout.addWidget(sourceLabel)
      namesLayout.addWidget(self.sourceLine)
      namesLayout.addWidget(targetLabel)
      namesLayout.addWidget(self.targetLine)
      
      # sets box as layout
      namesBox.setLayout(namesLayout)

      return namesBox

   # creates a radio button group box labeled State with the listed strings
   # can be referenced with self.radioButtonsDict['stateGroup']
   # this is for the emotional states that a character can feel toward another
   # in practical terms, changes the color of the edges
   # between yellow (joyful), red (angry), purple (powerful), orange (peaceful), blue (sad), and green (scared)
   def statesBoxGroup(self):
      states = ['joyful', 'angry', 'powerful', 'peaceful', 'sad', 'scared']
      
      return self.radioMaker('stateGroup', 'State', states) 

   # creates a radio button group box labeled Tenor of state with the listed strings
   # can be referenced with self.radioButtonsDict['tenorGroup']
   # this is for whether the emotional state is toward or for the second person
   # practically, it changes the arrowhead shape between normal arrow (toward) and empty dot (for)
   def tenorBoxGroup(self):
      tenors = ['toward', 'for']

      return self.radioMaker('tenorGroup', 'Tenor of state', tenors)

   # creates a radio button group box labeled Strength of relationship with the listed strings
   # can be referenced with self.radioButtonsDict['lineGroup']
   # this is for the strength of the relationship
   # practically, it changes the edge style between bold (strong) and dotted (tenuous)
   def lineBoxGroup(self):
      lines = ['strong', 'tenuous']

      return self.radioMaker('lineGroup', 'Strength of relationship', lines)

   # spin box for the obligations owed to first person
   # a spin box has an integer in it with an up arrow and a down arrow
   # this one determines the edge's label
   def obligationsBoxGroup(self):
      #group box label
      obligationBox = QGroupBox('Obligations over ending person')
      #label of actual spin box
      self.obligationLabel = QLabel('Enter integer:')
      #creates spin box
      self.obligationSpinBox = QSpinBox()
      #vertical layout
      obligationBoxLayout = QVBoxLayout()
      #save_buttons spin box to layout
      obligationBoxLayout.addWidget(self.obligationSpinBox)
      #sets group box layout as vertical layout
      obligationBox.setLayout(obligationBoxLayout)

      #returns group box
      return obligationBox

   # combo box to list the edges
   # a combo box is a dropdown that you can select from
   # this one lets you select from different edges to edit or delete as you choose
   def edgeComboBoxGroup(self):
      # creates group box and labels it
      edgeComboBox = QGroupBox('List of connections')
      # creates combo box
      self.edgeCombo = QComboBox()
      # horizontal layout
      edgeComboBoxLayout = QHBoxLayout()
      # save_buttons combo box to layout
      edgeComboBoxLayout.addWidget(self.edgeCombo)
      #sets group box layout to horizontal layout
      edgeComboBox.setLayout(edgeComboBoxLayout)

      # if the index has changed, run self.buttons_enabled
      self.edgeCombo.currentIndexChanged.connect(self.buttons_enabled)

      return edgeComboBox

   # map box to show the updated map
   # displays a PNG
   def showMap(self):
      #creates the group and labels it
      mapBox = QGroupBox('Map')
      #creates a label to put the png in
      self.mapPic = QLabel()
      #sets the pixmap (the thing that displays the png) as the desired png
      self.mapPic.setPixmap(QPixmap("test.png"))
      #vertical layout
      mapBoxLayout = QVBoxLayout()
      #adds label to layout
      mapBoxLayout.addWidget(self.mapPic)      
      # sets box as layout
      mapBox.setLayout(mapBoxLayout)

      return mapBox
   
   # # # #  METHODS # # # #

   # method to enable or disable the edit and delete buttons
   def buttons_enabled(self):
      # if there's 1+ edge present, emable the buttons (make them clickable)
      if self.edgesList:
         self.editingButton.setEnabled(True)
         self.deletingButton.setEnabled(True)
      # if no edges are present, disable the buttons
      # this only disables if you click the delete button twice once it's empty? :(
      # i think it's bc it only calls/checks when the delete button is pressed so
      if not any(self.edgesList):
         self.editingButton.setEnabled(False)
         self.deletingButton.setEnabled(False)


   def save_button_clicked(self):
      # sets variables then clears the text fields when applicable
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
         connectionObject = graph.Connection(source, target, state, graph.uniqueKey(), obligation, tenor, line)
         self.edgesList.append(connectionObject)
         self.edgeCombo.addItem(source + ' to ' + target + ', ' + state)
         for edge in self.edgesList:
            if edge not in self.savedEdgesList:
               self.savedEdgesList.append(edge)
               graph.addEdge(edge)
               p = graph.to_pydot(graph.g)
               p.write_dot('test.dot')
               p.write_png('test.png', prog='dot')
               self.mapPic.setPixmap(QPixmap("test.png"))

   
   # 
   def del_button_clicked(self):
      refNum = self.edgeCombo.currentIndex()
      print(refNum)
      if self.edgesList[refNum]:
         graph.removeEdge(self.edgesList[refNum])
         self.edgesList[refNum] = None
         p = graph.to_pydot(graph.g)
         p.write_png('test.png', prog='dot')
         self.mapPic.setPixmap(QPixmap("test.png"))
      else:
         self.edgesList[refNum] = None
      self.edgeCombo.removeItem(refNum)
      print(self.edgesList)
      self.buttons_enabled()
      


def main():

   app = QApplication(sys.argv)
   ex = VeilGUI()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()