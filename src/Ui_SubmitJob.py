# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wang\Documents\GitHub\DFT_Calc\pyqt5program\pyqtProject\SubmitJob.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_submitJob(object):
    def setupUi(self, submitJob):
        submitJob.setObjectName("submitJob")
        submitJob.resize(430, 74)
        submitJob.setSizeGripEnabled(True)
        self.chooseJobSubmit = QtWidgets.QComboBox(submitJob)
        self.chooseJobSubmit.setGeometry(QtCore.QRect(10, 10, 291, 22))
        self.chooseJobSubmit.setObjectName("chooseJobSubmit")
        self.submitJobOK = QtWidgets.QPushButton(submitJob)
        self.submitJobOK.setGeometry(QtCore.QRect(10, 40, 75, 23))
        self.submitJobOK.setObjectName("submitJobOK")
        self.pushButton_2 = QtWidgets.QPushButton(submitJob)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 40, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(submitJob)
        self.pushButton_2.clicked.connect(submitJob.reject)
        QtCore.QMetaObject.connectSlotsByName(submitJob)

    def retranslateUi(self, submitJob):
        _translate = QtCore.QCoreApplication.translate
        submitJob.setWindowTitle(_translate("submitJob", "选择一个配置文件用以提交任务或连接服务器"))
        self.submitJobOK.setText(_translate("submitJob", "OK"))
        self.pushButton_2.setText(_translate("submitJob", "Cancle"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    submitJob = QtWidgets.QDialog()
    ui = Ui_submitJob()
    ui.setupUi(submitJob)
    submitJob.show()
    sys.exit(app.exec_())

