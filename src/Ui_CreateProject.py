# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wang\Documents\GitHub\DFT_Calc\pyqt5program\pyqtProject\CreateProject.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CreateProject(object):
    def setupUi(self, CreateProject):
        CreateProject.setObjectName("CreateProject")
        CreateProject.resize(513, 133)
        CreateProject.setSizeGripEnabled(True)
        self.layoutWidget = QtWidgets.QWidget(CreateProject)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 191, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.projectOkButton = QtWidgets.QPushButton(self.layoutWidget)
        self.projectOkButton.setObjectName("projectOkButton")
        self.hboxlayout.addWidget(self.projectOkButton)
        self.projectCancelButton = QtWidgets.QPushButton(self.layoutWidget)
        self.projectCancelButton.setObjectName("projectCancelButton")
        self.hboxlayout.addWidget(self.projectCancelButton)
        self.gridLayoutWidget = QtWidgets.QWidget(CreateProject)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 481, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.gridLayoutWidget.setFont(font)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.projectName = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.projectName.setFont(font)
        self.projectName.setObjectName("projectName")
        self.gridLayout.addWidget(self.projectName, 0, 0, 1, 1)
        self.localProjectPathEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.localProjectPathEdit.setFont(font)
        self.localProjectPathEdit.setInputMask("")
        self.localProjectPathEdit.setText("")
        self.localProjectPathEdit.setReadOnly(True)
        self.localProjectPathEdit.setObjectName("localProjectPathEdit")
        self.gridLayout.addWidget(self.localProjectPathEdit, 0, 1, 1, 1)
        self.localProjectPathButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.localProjectPathButton.setFont(font)
        self.localProjectPathButton.setObjectName("localProjectPathButton")
        self.gridLayout.addWidget(self.localProjectPathButton, 0, 2, 1, 1)
        self.gridLayoutWidget.raise_()
        self.layoutWidget.raise_()

        self.retranslateUi(CreateProject)
        self.projectCancelButton.clicked.connect(CreateProject.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateProject)

    def retranslateUi(self, CreateProject):
        _translate = QtCore.QCoreApplication.translate
        CreateProject.setWindowTitle(_translate("CreateProject", "Create Project"))
        self.projectOkButton.setText(_translate("CreateProject", "&OK"))
        self.projectCancelButton.setText(_translate("CreateProject", "&Cancel"))
        self.projectName.setText(_translate("CreateProject", "Local Project Path\n"
"(.xsd file path)"))
        self.localProjectPathButton.setText(_translate("CreateProject", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateProject = QtWidgets.QDialog()
    ui = Ui_CreateProject()
    ui.setupUi(CreateProject)
    CreateProject.show()
    sys.exit(app.exec_())

