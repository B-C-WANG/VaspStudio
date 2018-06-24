# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wang\Documents\GitHub\DFT_Calc\pyqt5program\pyqtProject\item_create.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Create(object):
    def setupUi(self, Create):
        Create.setObjectName("Create")
        Create.resize(367, 133)
        Create.setSizeGripEnabled(True)
        self.label = QtWidgets.QLabel(Create)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label.setObjectName("label")
        self.name = QtWidgets.QLineEdit(Create)
        self.name.setGeometry(QtCore.QRect(80, 10, 271, 20))
        self.name.setObjectName("name")
        self.ok = QtWidgets.QPushButton(Create)
        self.ok.setGeometry(QtCore.QRect(20, 100, 75, 23))
        self.ok.setObjectName("ok")
        self.cancle = QtWidgets.QPushButton(Create)
        self.cancle.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.cancle.setObjectName("cancle")
        self.label_2 = QtWidgets.QLabel(Create)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label_2.setObjectName("label_2")
        self.key = QtWidgets.QLineEdit(Create)
        self.key.setGeometry(QtCore.QRect(80, 40, 271, 20))
        self.key.setReadOnly(False)
        self.key.setObjectName("key")
        self.label_3 = QtWidgets.QLabel(Create)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 61, 16))
        self.label_3.setObjectName("label_3")
        self.value = QtWidgets.QLineEdit(Create)
        self.value.setGeometry(QtCore.QRect(80, 70, 271, 20))
        self.value.setReadOnly(False)
        self.value.setObjectName("value")

        self.retranslateUi(Create)
        QtCore.QMetaObject.connectSlotsByName(Create)

    def retranslateUi(self, Create):
        _translate = QtCore.QCoreApplication.translate
        Create.setWindowTitle(_translate("Create", "CreateTextItem"))
        self.label.setText(_translate("Create", "Name"))
        self.ok.setText(_translate("Create", "OK"))
        self.cancle.setText(_translate("Create", "Cancle"))
        self.label_2.setText(_translate("Create", "Key"))
        self.label_3.setText(_translate("Create", "Value"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Create = QtWidgets.QDialog()
    ui = Ui_Create()
    ui.setupUi(Create)
    Create.show()
    sys.exit(app.exec_())

