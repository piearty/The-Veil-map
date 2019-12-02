# this creates the gui to interface with the graph.py function

# lets app accept command line arguments
import sys

# imports the gui aspect of pyqt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# imports allowing you to access current directory
import os.path

# to make temporary files so program doesn't crash on mac
import tempfile

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

      # makes a fileChosen variable set to None
      # so no error is produced when write_to_files checks whether it exists
      self.fileChosen = None

      self.tempFolder = tempfile.gettempdir()
      self.tempDotFileName = tempfile.gettempprefix() + 'map.dot'
      self.tempDotFilePath = os.path.join(self.tempFolder, self.tempDotFileName)
      self.tempPngFileName = tempfile.gettempprefix() + 'map.png'
      self.tempPngFilePath = os.path.join(self.tempFolder, self.tempPngFileName)

      print(self.tempDotFilePath)


      # creates the grid where the widgets will be placed
      grid = QGridLayout()

      # makes a fileChosen variable set to None
      # so no error is produced when write_to_files checks whether it exists
     # self.fileChosen = None

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
      # creates button labeled saveConnection Connection
      saveConnectionButton = QPushButton("\nSave\nConnection\n")
      saveConnectionButton.setCheckable(True)

      # box containing saveConnection button
      saveConnectionButtonBox = QDialogButtonBox()
      saveConnectionButtonBox.addButton(saveConnectionButton, QDialogButtonBox.ActionRole)

      # when clicked, run the saveConnection_button_clicked method respectively
      saveConnectionButton.clicked.connect(self.save_connection_button_clicked)

      return saveConnectionButtonBox

   def edgeButtonsGroup(self):
      # creates buttons labeled edit, clear, and delete, but makes it so they can't be clicked on yet
      # edit and delete button don't work yet
     # self.editingButton = QPushButton("Edit")
      #self.editingButton.setCheckable(True)
      #self.editingButton.setEnabled(False)


      self.openingButton = QPushButton("Open")
      self.openingButton.setCheckable(True)

     # self.deletingButton = QPushButton("Delete")
     # self.deletingButton.setCheckable(True)
     # self.deletingButton.setEnabled(False)

      self.clearingButton = QPushButton("Clear")
      self.clearingButton.setCheckable(True)
      self.clearingButton.setEnabled(False)

      self.savingButton = QPushButton("Save file")
      self.savingButton.setCheckable(True)
      self.savingButton.setEnabled(False)

      # box containing save, edit, open, clear, and delete buttons (these modify the edges)
      edgeButtonsBox = QDialogButtonBox()
     # edgeButtonsBox.addButton(self.editingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(self.openingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(self.clearingButton, QDialogButtonBox.ActionRole)
   #   edgeButtonsBox.addButton(self.deletingButton, QDialogButtonBox.ActionRole)
      edgeButtonsBox.addButton(self.savingButton, QDialogButtonBox.ActionRole)
      

      # below is code that's not implemented yet
      # self.editingButton.clicked.connect(self.edit_button_clicked)

      # when delete button is clicked, run the delete button method
      # also run buttons_enabled method
      self.openingButton.clicked.connect(self.open_button_clicked)
  #    self.deletingButton.clicked.connect(self.del_button_clicked)
      self.clearingButton.clicked.connect(self.clear_button_clicked)
      self.savingButton.clicked.connect(self.save_button_clicked)

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
      # creates empty entry
      self.edgeCombo.addItem('')
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
      mapPic = QGraphicsScene()
      mapView = QGraphicsView()
      mapView.setScene(mapPic)

      mapView.setSceneRect(0,0,600,600)
      #sets the pixmap (the thing that displays the png) as the desired png
   #   pic = QPixmap("map.dot.png")

      self.mapItem = QGraphicsPixmapItem()
      mapPic.addItem(self.mapItem)
      #creates the group and labels it
      mapBox = QGroupBox('Map')
      #vertical layout
      mapBoxLayout = QVBoxLayout()
      #adds label to layout
      mapBoxLayout.addWidget(mapView)      
      # sets box as layout
      mapBox.setLayout(mapBoxLayout)

      return mapBox
   
# ************************ METHODS ************************ #

   # method to enable or disable the edit and delete buttons
   def buttons_enabled(self):
      # if the combo box is not at the default (blank), enable the buttons (make them clickable)
      #if self.edgeCombo.currentIndex() >= 1:
      #   self.editingButton.setEnabled(True)
   #      self.deletingButton.setEnabled(True)
      # if the combo box is at the default (blank), disable the buttons
      # this only disables if you click the delete button twice once it's empty? :(
      # i think it's bc it only calls/checks when the delete button is pressed so
      #elif self.edgeCombo.currentIndex() == 0:
     #    self.editingButton.setEnabled(False)
     #    self.deletingButton.setEnabled(False)
     #if there's an edge present, enable the save and clear buttons. if the graph is empty, disable them.
      if len(self.edgesList) >= 1:
         self.savingButton.setEnabled(True)
         self.clearingButton.setEnabled(True)
      elif len(self.edgesList) == 0:
         self.savingButton.setEnabled(False)
         self.clearingButton.setEnabled(False)
   # opens a file dialog so you can pick a dot file (default from the current working directory)
   def open_button_clicked(self):
      self.openFileChosen = QFileDialog.getOpenFileName(self, 'Open file', '', "DOT files (*.dot)")
      # if one is chosen, then make it the current graph and run write_to_files()
      if self.openFileChosen[0]:
         self.fileChosen = self.openFileChosen
         print(self.fileChosen[0])
         graph.g = graph.read_dot(self.fileChosen[0])
         self.write_to_files(self.fileChosen[0], self.fileChosen[0]+'.png')
         self.edgesList = []
         self.savedEdgesList = []
         self.edgeCombo.clear()
         self.edgeCombo.addItem('')
         for edge in graph.g.edges():
            self.edgesList.append(edge)
            self.savedEdgesList.append(edge)
            self.edgeCombo.addItem(edge[0] + ' to ' + edge[1])

   # method when you click 'saveConnection connection'
   def save_connection_button_clicked(self):
      # sets variables then clears the text fields when applicable
      source = self.sourceLine.text()
      self.sourceLine.setText('')
      
      target = self.targetLine.text()
      self.targetLine.setText('')
      
      # # # # if the obligations aren't 0 then set obligation (so there's no '0' label)
      if self.obligationSpinBox.value() != 0:
         obligation = self.obligationSpinBox.value()
      else:
         obligation = None

      state = self.radioButtonsDict['stateGroup'].checkedButton().text()

      tenor = self.radioButtonsDict['tenorGroup'].checkedButton().text()
      
      line = self.radioButtonsDict['lineGroup'].checkedButton().text()

      # here's the meat
      # if the person has filled out both source and target (minimum necessary to make a node)
      if source and target:
         # set connectionObject as the object defined by graph.Connection
         # with all this stuff we defined earlier as attributes
         connectionObject = graph.Connection(source, target, state, graph.unique_key(), obligation, tenor, line)
         # add object to a list
         self.edgesList.append(connectionObject)
         # add object to combo box
         # looks like: Ribbon to Calder, joyful
         self.edgeCombo.addItem(source + ' to ' + target)
         # for edge in the list
         for edge in self.edgesList:
            # if it's not in savedEdgesList, add it to savedEdgesList and add the edge to the graph
            # (there's probably a better way to do this but I haven't figured it out)
            if edge and edge not in self.savedEdgesList:
               self.savedEdgesList.append(edge)
               graph.add_an_edge(edge)
               # checks if a file is chosen by open_button_clicked dialog
               # if yes, write to that file
               # if no, write to map.dot and map.dot.png
               # display graph
               if self.fileChosen:
                  self.write_to_files(self.fileChosen[0], self.fileChosen[0]+'.png')
               else:
                  self.write_to_files(self.tempDotFilePath, self.tempPngFilePath)
               self.buttons_enabled()

   #clears entire graph
   def clear_button_clicked(self):
      graph.clear_graph()
      # set all edges in the list to None
      self.edgesList = []
      # removes everything from the combo box
      self.edgeCombo = QComboBox()
         # checks if a file is chosen by open_button_clicked dialog
         # if yes, write to that file
         # if no, write to map.dot and map.dot.png
         # display graph
      if self.fileChosen:
         self.write_to_files(self.fileChosen[0], self.fileChosen[0]+'.png')
      else:
         self.write_to_files(self.tempDotFilePath, self.tempPngFilePath)



   # deletes selected edge
   #doesn't work right now/buggy
  # def del_button_clicked(self):
      # index number is the currently selected entry in the combo box
      # -1 bc the blank default edge exists
   #   refNum = self.edgeCombo.currentIndex() - 1
      # if that exists in the edges list
    #  if self.edgesList[refNum]:
     #    if type(self.edgesList[refNum]) is tuple:
        # remove the edge from the graph
     #       graph.remove_an_edge(None, self.edgesList[refNum])
      #   else:
       #     graph.remove_an_edge(self.edgesList[refNum])
         # set the edge in the list to None
        # self.edgesList.pop(refNum)
         # removes it from the combo box
         #self.edgeCombo.removeItem(refNum + 1)
         # checks if a file is chosen by open_button_clicked dialog
         # if yes, write to that file
         # if no, write to map.dot and map.dot.png
         # display graph
         #if self.fileChosen:
          #  self.write_to_files(self.fileChosen[0], self.fileChosen[0]+'.png')
         #else:
          #  self.write_to_files(self.tempDotFilePath, self.tempPngFilePath)

   def save_button_clicked(self):
      self.saveFileChosen = QFileDialog.getSaveFileName(self, 'Save file', '', "DOT files (*.dot)")
      # if one is chosen, then make it the current graph and run write_to_files()
      if self.saveFileChosen[0]:
         self.fileChosen = self.saveFileChosen
         print(self.fileChosen[0])
         self.write_to_files(self.fileChosen[0], self.fileChosen[0]+'.png')


   # writes graph so it changes before the viewer's eyes
   # chosenDot is a dot file and chosenPng is a png file
   def write_to_files(self, chosenDot, chosenPng):
      print(chosenDot, chosenPng)
      # turns networkx graph to pydot graph
      p = graph.to_pydot(graph.g)
      if chosenDot:
         p.write_dot(chosenDot, prog = 'dot')
      if chosenPng:
         p.write_png(chosenPng, prog='dot')
         self.mapItem.setPixmap(QPixmap(chosenPng))

def main():

   app = QApplication(sys.argv)
   ex = VeilGUI()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()