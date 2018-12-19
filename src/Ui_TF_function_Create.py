# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wang\Documents\GitHub\DFT_Calc\pyqt5program\pyqtProject\TF_function_Create.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(310, 168)
        Dialog.setSizeGripEnabled(True)
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(10, 140, 91, 23))
        self.ok.setObjectName("ok")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 291, 92))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.xyz = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.xyz.setObjectName("xyz")
        self.gridLayout.addWidget(self.xyz, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.function = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.function.setObjectName("function")
        self.gridLayout.addWidget(self.function, 1, 1, 1, 1)
        self.name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 351, 41))
        self.label_3.setObjectName("label_3")
        self.test = QtWidgets.QPushButton(Dialog)
        self.test.setGeometry(QtCore.QRect(110, 140, 91, 23))
        self.test.setObjectName("test")
        self.ok_2 = QtWidgets.QPushButton(Dialog)
        self.ok_2.setGeometry(QtCore.QRect(210, 140, 91, 23))
        self.ok_2.setObjectName("ok_2")

        self.retranslateUi(Dialog)
        self.ok_2.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ok.setText(_translate("Dialog", "Create"))
        self.label.setText(_translate("Dialog", "TF function"))
        self.label_4.setText(_translate("Dialog", "Name"))
        self.xyz.setText(_translate("Dialog", "0,0,0.21"))
        self.label_2.setText(_translate("Dialog", "X,Y,Z      "))
        self.function.setText(_translate("Dialog", "z>0.2"))
        self.label_3.setText(_translate("Dialog", "按照python一行格式输入XYZ条件\n"
"逗号分隔XYZ坐标进行测试"))
        self.test.setText(_translate("Dialog", "Test"))
        self.ok_2.setText(_translate("Dialog", "Cancle"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

