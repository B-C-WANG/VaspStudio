# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wang\Documents\GitHub\DFT_Calc\pyqt5program\pyqtProject\about.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_about(object):
    def setupUi(self, about):
        about.setObjectName("about")
        about.setWindowModality(QtCore.Qt.NonModal)
        about.resize(360, 71)
        about.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        about.setSizeGripEnabled(True)
        self.textBrowser = QtWidgets.QTextBrowser(about)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 361, 71))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(about)
        QtCore.QMetaObject.connectSlotsByName(about)

    def retranslateUi(self, about):
        _translate = QtCore.QCoreApplication.translate
        about.setWindowTitle(_translate("about", "Dialog"))
        self.textBrowser.setHtml(_translate("about", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Vasp Studio </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">v0.2</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">author: WANG Baochuan</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">github: https://github.com/B-C-WANG</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    about = QtWidgets.QDialog()
    ui = Ui_about()
    ui.setupUi(about)
    about.show()
    sys.exit(app.exec_())

