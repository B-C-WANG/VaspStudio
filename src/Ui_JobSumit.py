# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wang\Documents\GitHub\DFT_Calc\pyqt5program\pyqtProject\JobSumit.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateProject(object):
    def setupUi(self, CreateProject):
        CreateProject.setObjectName("CreateProject")
        CreateProject.resize(831, 517)
        CreateProject.setSizeGripEnabled(True)
        self.layoutWidget = QtWidgets.QWidget(CreateProject)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 420, 191, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.submitJobOk = QtWidgets.QPushButton(self.layoutWidget)
        self.submitJobOk.setObjectName("submitJobOk")
        self.hboxlayout.addWidget(self.submitJobOk)
        self.submitJobCancel = QtWidgets.QPushButton(self.layoutWidget)
        self.submitJobCancel.setObjectName("submitJobCancel")
        self.hboxlayout.addWidget(self.submitJobCancel)
        self.gridLayoutWidget = QtWidgets.QWidget(CreateProject)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 50, 481, 221))
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
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.remoteProjectPathEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.remoteProjectPathEdit.setFont(font)
        self.remoteProjectPathEdit.setInputMask("")
        self.remoteProjectPathEdit.setText("")
        self.remoteProjectPathEdit.setReadOnly(False)
        self.remoteProjectPathEdit.setObjectName("remoteProjectPathEdit")
        self.gridLayout.addWidget(self.remoteProjectPathEdit, 5, 1, 1, 1)
        self.portLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.portLineEdit.setFont(font)
        self.portLineEdit.setText("")
        self.portLineEdit.setObjectName("portLineEdit")
        self.gridLayout.addWidget(self.portLineEdit, 2, 1, 1, 1)
        self.remoteProjectPath = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.remoteProjectPath.setFont(font)
        self.remoteProjectPath.setObjectName("remoteProjectPath")
        self.gridLayout.addWidget(self.remoteProjectPath, 5, 0, 1, 1)
        self.hostLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.hostLineEdit.setFont(font)
        self.hostLineEdit.setText("")
        self.hostLineEdit.setObjectName("hostLineEdit")
        self.gridLayout.addWidget(self.hostLineEdit, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.projectTypeChoose = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.projectTypeChoose.setObjectName("projectTypeChoose")
        self.verticalLayout.addWidget(self.projectTypeChoose)
        self.gridLayout.addLayout(self.verticalLayout, 6, 1, 1, 1)
        self.localProjectPath_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.localProjectPath_2.setFont(font)
        self.localProjectPath_2.setObjectName("localProjectPath_2")
        self.gridLayout.addWidget(self.localProjectPath_2, 6, 0, 1, 1)
        self.usernameLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.usernameLineEdit.setFont(font)
        self.usernameLineEdit.setText("")
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.gridLayout.addWidget(self.usernameLineEdit, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.passwordLineEdit.setFont(font)
        self.passwordLineEdit.setText("")
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.gridLayout.addWidget(self.passwordLineEdit, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.nameEdit = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.nameEdit.setFont(font)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 0, 1, 1)
        self.name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.name.setFont(font)
        self.name.setText("")
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(CreateProject)
        self.label_5.setGeometry(QtCore.QRect(30, 330, 461, 16))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.textBrowser = QtWidgets.QTextBrowser(CreateProject)
        self.textBrowser.setGeometry(QtCore.QRect(30, 290, 481, 111))
        self.textBrowser.setObjectName("textBrowser")
        self.groupBox = QtWidgets.QGroupBox(CreateProject)
        self.groupBox.setGeometry(QtCore.QRect(530, 40, 271, 321))
        self.groupBox.setObjectName("groupBox")
        self.contentWidget = QtWidgets.QListWidget(self.groupBox)
        self.contentWidget.setGeometry(QtCore.QRect(10, 20, 251, 291))
        self.contentWidget.setDragEnabled(True)
        self.contentWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.contentWidget.setObjectName("contentWidget")
        self.submitJobRemove = QtWidgets.QPushButton(CreateProject)
        self.submitJobRemove.setGeometry(QtCore.QRect(540, 370, 92, 23))
        self.submitJobRemove.setObjectName("submitJobRemove")
        self.gridLayoutWidget.raise_()
        self.layoutWidget.raise_()
        self.label_5.raise_()
        self.textBrowser.raise_()
        self.groupBox.raise_()
        self.submitJobRemove.raise_()

        self.retranslateUi(CreateProject)
        self.submitJobCancel.clicked.connect(CreateProject.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateProject)

    def retranslateUi(self, CreateProject):
        _translate = QtCore.QCoreApplication.translate
        CreateProject.setWindowTitle(_translate("CreateProject", "Create Project"))
        self.submitJobOk.setText(_translate("CreateProject", "&OK"))
        self.submitJobCancel.setText(_translate("CreateProject", "&Cancel"))
        self.label_2.setText(_translate("CreateProject", "Port"))
        self.label.setText(_translate("CreateProject", "Username"))
        self.remoteProjectPath.setText(_translate("CreateProject", "Remote Project Path"))
        self.localProjectPath_2.setText(_translate("CreateProject", "Project Type"))
        self.label_3.setText(_translate("CreateProject", "Host"))
        self.label_4.setText(_translate("CreateProject", "Password"))
        self.nameEdit.setText(_translate("CreateProject", "Name"))
        self.textBrowser.setHtml(_translate("CreateProject", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">normal：</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. xsd文件的信息转到POSCAR中，需要POSCAR模板，自动生成POTCAR</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. 其他文件，包括INCAR，KPOINT等</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">ts_fort_188：</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. xsd文件信息转到POSCAR和fort.188中，<span style=\" color:#ff0004;\">xsd文件需要标出两个原子的distance</span>，需要POSCAR和fort.188模板，自动生成POTCAR</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. 其他文件，包括INCAR，KPOINT等</p></body></html>"))
        self.groupBox.setTitle(_translate("CreateProject", "Content"))
        self.submitJobRemove.setText(_translate("CreateProject", "Remove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateProject = QtWidgets.QDialog()
    ui = Ui_CreateProject()
    ui.setupUi(CreateProject)
    CreateProject.show()
    sys.exit(app.exec_())

