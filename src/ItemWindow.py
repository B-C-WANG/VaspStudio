from PySide2.QtWidgets import QListWidgetItem,QListWidget
from VSP_ItemCollection import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFileDialog,QMessageBox
from JobSubmitItem import JobSubmit_item
from projectTypeAndChecker import ProjectType,ProjectType_dict

class SubmitJobCreateWindow(object):
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
        self.portLineEdit.setText(_translate("CreateProject", ""))
        self.remoteProjectPath.setText(_translate("CreateProject", "Remote Project Path"))
        self.hostLineEdit.setText(_translate("CreateProject", ""))
        self.localProjectPath_2.setText(_translate("CreateProject", "Project Type"))
        self.usernameLineEdit.setText(_translate("CreateProject", ""))
        self.label_3.setText(_translate("CreateProject", "Host"))
        self.label_4.setText(_translate("CreateProject", "Password"))
        self.nameEdit.setText(_translate("CreateProject", "Name"))
        self.textBrowser.setHtml(_translate("CreateProject",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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

class KeyItemCreateWindow(object):
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
        self.cancel = QtWidgets.QPushButton(Create)
        self.cancel.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.cancel.setObjectName("cancel")
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
        self.cancel.setText(_translate("Create", "cancel"))
        self.label_2.setText(_translate("Create", "Key"))
        self.label_3.setText(_translate("Create", "Value"))

class TF_FunctionCreateWindow(object):
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
        self.ok_2.setText(_translate("Dialog", "Cancel"))

class FileCreateWindow(object):
    def setupUi(self, Create):
        Create.setObjectName("Create")
        Create.resize(484, 101)
        Create.setSizeGripEnabled(True)
        self.label = QtWidgets.QLabel(Create)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label.setObjectName("label")
        self.name = QtWidgets.QLineEdit(Create)
        self.name.setGeometry(QtCore.QRect(80, 10, 381, 20))
        self.name.setObjectName("name")
        self.ok = QtWidgets.QPushButton(Create)
        self.ok.setGeometry(QtCore.QRect(20, 70, 75, 23))
        self.ok.setObjectName("ok")
        self.cancel = QtWidgets.QPushButton(Create)
        self.cancel.setGeometry(QtCore.QRect(100, 70, 75, 23))
        self.cancel.setObjectName("cancel")
        self.label_2 = QtWidgets.QLabel(Create)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label_2.setObjectName("label_2")
        self.path = QtWidgets.QLineEdit(Create)
        self.path.setGeometry(QtCore.QRect(80, 40, 321, 20))
        self.path.setReadOnly(True)
        self.path.setObjectName("path")
        self.getFile = QtWidgets.QPushButton(Create)
        self.getFile.setGeometry(QtCore.QRect(410, 40, 51, 23))
        self.getFile.setObjectName("getFile")

        self.retranslateUi(Create)
        QtCore.QMetaObject.connectSlotsByName(Create)

    def retranslateUi(self, Create):
        _translate = QtCore.QCoreApplication.translate
        Create.setWindowTitle(_translate("Create", "CreateTextItem"))
        self.label.setText(_translate("Create", "Name"))
        self.ok.setText(_translate("Create", "OK"))
        self.cancel.setText(_translate("Create", "cancel"))
        self.label_2.setText(_translate("Create", "Path"))
        self.getFile.setText(_translate("Create", "..."))

class TextFileCreateWindow(object):
    def setupUi(self, Create):
        Create.setObjectName("Create")
        Create.resize(484, 353)
        Create.setSizeGripEnabled(True)
        self.label = QtWidgets.QLabel(Create)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(Create)
        self.groupBox.setGeometry(QtCore.QRect(10, 70, 461, 251))
        self.groupBox.setObjectName("groupBox")
        self.content = QtWidgets.QPlainTextEdit(self.groupBox)
        self.content.setGeometry(QtCore.QRect(10, 20, 441, 221))
        self.content.setObjectName("content")
        self.name = QtWidgets.QLineEdit(Create)
        self.name.setGeometry(QtCore.QRect(80, 10, 381, 20))
        self.name.setObjectName("name")
        self.ok = QtWidgets.QPushButton(Create)
        self.ok.setGeometry(QtCore.QRect(20, 320, 75, 23))
        self.ok.setObjectName("ok")
        self.cancel = QtWidgets.QPushButton(Create)
        self.cancel.setGeometry(QtCore.QRect(100, 320, 75, 23))
        self.cancel.setObjectName("cancel")
        self.label_2 = QtWidgets.QLabel(Create)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label_2.setObjectName("label_2")
        self.fileName = QtWidgets.QLineEdit(Create)
        self.fileName.setGeometry(QtCore.QRect(80, 40, 381, 20))
        self.fileName.setObjectName("fileName")

        self.retranslateUi(Create)
        QtCore.QMetaObject.connectSlotsByName(Create)

    def retranslateUi(self, Create):
        _translate = QtCore.QCoreApplication.translate
        Create.setWindowTitle(_translate("Create", "CreateTextItem"))
        self.label.setText(_translate("Create", "Name"))
        self.groupBox.setTitle(_translate("Create", "Content"))
        self.ok.setText(_translate("Create", "OK"))
        self.cancel.setText(_translate("Create", "cancel"))
        self.label_2.setText(_translate("Create", "File Name"))

class ItemWindow():
    # 用于容纳各个item的窗口的类，有new Edit remove 和 check四个
    def __init__(self,
                 main_window,
                 vsp,
                 new_button,
                 edit_button,
                 remove_button,
                 check_button,
                 list_widget):
        self.remove_ = None
        self.vsp = vsp
        self.main_window = main_window
        self.new_button = new_button

        self.remove_button = remove_button
        self.edit_button = edit_button
        self.check_button = check_button
        self.list_widget =list_widget

        self.new_button.clicked.connect(self.new_one)
        self.edit_button.clicked.connect(self.edit_one)
        self.remove_button.clicked.connect(self.remove_one)
        self.check_button.clicked.connect(self.check_one)
        self.widget = []

    def new_one(self):
        pass

    def edit_one(self):
        pass
    def remove_one(self):
        pass
    def check_one(self):
        pass


    def update(self):
        self.widget = []
        self.list_widget.clear()
        keys = list(self.vsp_items.keys())
        vsp_n = len(keys)
        for i in range(vsp_n):
            newItem = QListWidgetItem(self.vsp_items[keys[i]].item_key)
            self.widget.append(newItem)
            self.list_widget.addItem(newItem)

class Text_File_Item_Window(ItemWindow):
    # 这是主要的类，方法是，创建时给出相应的button 和widget，以及vsp项目即可
    def __init__(self,
                 main_window,
                 vsp,
                 new_button,
                 edit_button,
                 remove_button,
                 check_button,
                 list_widget
                 ):
        super(Text_File_Item_Window, self).__init__(
            main_window,
            vsp,
            new_button,
            edit_button,
            remove_button,
            check_button,
            list_widget)
        self.vsp_items = self.vsp.text_file_items

    def show(self,window_source):

        self.window = QtWidgets.QDialog()
        self.window_ui = window_source()
        self.window_ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.window_ui.cancel.clicked.connect(self.window.reject)
        self.window.show()

    def create(self):
        if self.remove_:
            del self.vsp.text_file_items[self.remove_.text()]
            self.widget.remove(self.remove_)
            self.remove_ = None
            self.update()
        filename = self.window_ui.fileName.text()
        content = self.window_ui.content.toPlainText()
        name = self.window_ui.name.text()

        if self.vsp.check_if_same_key(name) == True:
            QMessageBox.critical(self.window, "Error", "Name Exists, Abort.")
            return
        print("create text item",content)
        if filename != "" and content != "":
            Text_File_item(
                name=name,
                vsp=self.vsp,
                file_name=filename,
                string=content
            )
            self.window.close()
        self.update()


    def new_one(self):
        # 这里建议在designer中设计界面，然后把代码copy到一开始的类中，然后在这里实例化
        self.show(TextFileCreateWindow)
        self.window_ui.ok.clicked.connect(self.create)
        self.window_ui.cancel.clicked.connect(self.window.reject)

    def edit_one(self):
        for i in self.widget:
            if i.isSelected():

                self.show(TextFileCreateWindow)

                print(self.vsp.text_file_items)
                self.window_ui.fileName.setText(self.vsp.text_file_items[i.text()].file_name)
                self.window_ui.content.setPlainText(self.vsp.text_file_items[i.text()].string)
                self.window_ui.name.setText(self.vsp.text_file_items[i.text()].name)
                self.window_ui.ok.clicked.connect(self.create)
                self.remove_ = i

                # reject 之后记住删除要remove的，否则edit之后new就会丢失
                def clear():
                    self.remove_ = None

                self.window.rejected.connect(clear)

    def remove_one(self):

        for i in self.widget:
            if i.isSelected():
                del self.vsp.text_file_items[i.text()]
                self.widget.remove(i)
                self.update()

class File_Item_Window(ItemWindow):
    # 这是主要的类，方法是，创建时给出相应的button 和widget，以及vsp项目即可
    def __init__(self,
                 main_window,
                 vsp,
                 new_button,
                 edit_button,
                 remove_button,
                 check_button,
                 list_widget
                 ):
        super(File_Item_Window, self).__init__(
            main_window,
            vsp,
            new_button,
            edit_button,
            remove_button,
            check_button,
            list_widget)
        self.vsp_items = self.vsp.file_items

    def show(self,window_source):


        def get_file():
            self.window_ui.path.setText(
                QFileDialog.getOpenFileName(
                    self.window,
                    "Choose file",
                )[0])
        self.window = QtWidgets.QDialog()
        self.window_ui = window_source()
        self.window_ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.window_ui.cancel.clicked.connect(self.window.reject)

        self.window.show()
        self.window_ui.getFile.clicked.connect(
            get_file)

    def create(self):
        if self.remove_:
            del self.vsp.file_items[self.remove_.text()]
            self.widget.remove(self.remove_)
            self.remove_ = None
            self.update()
        name = self.window_ui.name.text()
        path = self.window_ui.path.text()

        if self.vsp.check_if_same_key(name) == True:
            QMessageBox.critical(self.window, "Error", "Name Exists, Abort")
            return

        if name != "" and path != "":
            File_item(
                name=name,
                vsp=self.vsp,
                path=path
            )
            self.window.close()
        self.update()


    def new_one(self):
        # 这里建议在designer中设计界面，然后把代码copy到一开始的类中，然后在这里实例化
        self.show(FileCreateWindow)
        self.window_ui.ok.clicked.connect(self.create)
        self.window_ui.cancel.clicked.connect(self.window.reject)

    def edit_one(self):
        for i in self.widget:
            if i.isSelected():
                # 先删除，再create
                self.show(FileCreateWindow)
                # 不允许cancel，OK直接创建
                self.window_ui.cancel.destroy()
                print(self.vsp.file_items)
                self.window_ui.name.setText(self.vsp.file_items[i.text()].name)
                self.window_ui.path.setText(self.vsp.file_items[i.text()].path)


                self.window_ui.ok.clicked.connect(self.create)
                self.remove_ = i

                # reject 之后记住删除要remove的，否则edit之后new就会丢失
                def clear():
                    self.remove_ = None

                self.window.rejected.connect(clear)


    def remove_one(self):

        for i in self.widget:
            if i.isSelected():
                del self.vsp.file_items[i.text()]
                self.widget.remove(i)
                self.update()

class TF_Window(ItemWindow):
    # 这是主要的类，方法是，创建时给出相应的button 和widget，以及vsp项目即可
    def __init__(self,
                 main_window,
                 vsp,
                 new_button,
                 edit_button,
                 remove_button,
                 check_button,
                 list_widget
                 ):
        super(TF_Window, self).__init__(
            main_window,
            vsp,
            new_button,
            edit_button,
            remove_button,
            check_button,
            list_widget)
        self.vsp_items = self.vsp.tf_function_items

    def show(self,window_source):


        self.window = QtWidgets.QDialog()
        self.window_ui = window_source()
        self.window_ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.window.show()

    def tfTest(self):
        function = self.window_ui.function.text()
        xyz = self.window_ui.xyz.text()

        function = TF_Condition_item.make_condition_func(function)
        status = TF_Condition_item.test_TF_condition_function(function, xyz=xyz)

        if status == CStatus.Failed:
            QMessageBox.critical(self.window, "Error", "函数或XYZ输入错误，请按照python语法设置")
            return False
        else:

            QMessageBox.information(self.window,
                                    "提示",
                                    "创建函数成功，函数\n%s\n对于\n%s的结果为\n%s" % (function, xyz, status))
            return True


    def create(self):
        if self.remove_:
            del self.vsp.tf_function_items[self.remove_.text()]
            self.widget.remove(self.remove_)
            self.remove_ = None
            self.update()
        name = self.window_ui.name.text()
        function = self.window_ui.function.text()
        xyz = self.window_ui.xyz.text()
        if name == "":return
        if self.vsp.check_if_same_key(name) == True:
            QMessageBox.critical(self.window, "Error", "Name Exists, Abort")
            return

        if self.tfTest() == False: return


        TF_Condition_item(
                name=name,
                vsp=self.vsp,
                string=function
            )
        self.window.close()
        self.update()


    def new_one(self):
        # 这里建议在designer中设计界面，然后把代码copy到一开始的类中，然后在这里实例化
        self.show(TF_FunctionCreateWindow)
        self.window_ui.ok.clicked.connect(self.create)
        self.window_ui.test.clicked.connect(self.tfTest)

    def edit_one(self):
        for i in self.widget:
            if i.isSelected():
                # 先删除，再create
                self.show(TF_FunctionCreateWindow)
                # 不允许cancel，OK直接创建
                self.window_ui.test.clicked.connect(self.tfTest)

                self.window_ui.name.setText(self.vsp.tf_function_items[i.text()].name)

                self.window_ui.function.setText(self.vsp.tf_function_items[i.text()].string)

                self.window_ui.ok.clicked.connect(self.create)
                self.remove_ = i

                # reject 之后记住删除要remove的，否则edit之后new就会丢失
                def clear():
                    self.remove_ = None

                self.window.rejected.connect(clear)

    def remove_one(self):

        for i in self.widget:
            if i.isSelected():
                del self.vsp.tf_function_items[i.text()]
                self.widget.remove(i)
                self.update()

class Key_Item_Window(ItemWindow):
    # 这是主要的类，方法是，创建时给出相应的button 和widget，以及vsp项目即可
    def __init__(self,
                 main_window,
                 vsp,
                 new_button,
                 edit_button,
                 remove_button,
                 check_button,
                 list_widget
                 ):
        super(Key_Item_Window, self).__init__(
            main_window,
            vsp,
            new_button,
            edit_button,
            remove_button,
            check_button,
            list_widget)
        self.vsp_items = self.vsp.key_items

    def show(self,window_source):

        self.window = QtWidgets.QDialog()
        self.window_ui = window_source()
        self.window_ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.window_ui.cancel.clicked.connect(self.window.reject)
        self.window.show()

    def create(self):
        if self.remove_:
            del self.vsp.key_items[self.remove_.text()]
            self.widget.remove(self.remove_)
            self.remove_ = None
            self.update()
        name = self.window_ui.name.text()
        key = self.window_ui.key.text()
        value = self.window_ui.value.text()

        if self.vsp.check_if_same_key(name) == True:
            QMessageBox.critical(self.window, "Error", "Name Exists, Abort")
            return

        if name != "" and key != "":
            KeyItem(
                name=name,
                vsp=self.vsp,
                key=key,
                value=value
            )
            self.window.close()
        self.update()


    def new_one(self):
        # 这里建议在designer中设计界面，然后把代码copy到一开始的类中，然后在这里实例化
        self.show(KeyItemCreateWindow)
        self.window_ui.ok.clicked.connect(self.create)
        self.window_ui.cancel.clicked.connect(self.window.reject)

    def edit_one(self):
        for i in self.widget:
            if i.isSelected():
                # 先删除，再create
                self.show(KeyItemCreateWindow)
                # 不允许cancel，OK直接创建
                self.window_ui.cancel.destroy()
                print(self.vsp.key_items)
                self.window_ui.key.setText(self.vsp.key_items[i.text()].key)
                self.window_ui.value.setText(self.vsp.key_items[i.text()].value)
                self.window_ui.name.setText(self.vsp.key_items[i.text()].name)
                self.window_ui.ok.clicked.connect(self.create)
                self.remove_ = i
                # reject 之后记住删除要remove的，否则edit之后new就会丢失
                def clear():
                    self.remove_ = None
                self.window.rejected.connect(clear)


    def remove_one(self):

        for i in self.widget:
            if i.isSelected():
                del self.vsp.key_items[i.text()]
                self.widget.remove(i)
                self.update()

class SubmitJob_Window(ItemWindow):
    # 这是主要的类，方法是，创建时给出相应的button 和widget，以及vsp项目即可
    def __init__(self,
                 main_window,
                 vsp,
                 new_button,
                 edit_button,
                 remove_button,
                 check_button,
                 list_widget
                 ):
        super(SubmitJob_Window, self).__init__(
            main_window,
            vsp,
            new_button,
            edit_button,
            remove_button,
            check_button,
            list_widget)
        self.vsp_items = self.vsp.job_submit_items
        self.window = QtWidgets.QDialog()



    def show(self,window_source):

        self.window_ui = window_source()
        self.window_ui.setupUi(self.window)
        #self.window.setWindowFlags()
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


        self.window_ui.contentWidget.itemChanged.connect(self.avoid_repeat)
        for i in ProjectType_dict:
            self.window_ui.projectTypeChoose.addItem(i)
        self.window.show()

    def avoid_repeat(self):
        # 用set
        len_c = len(self.window_ui.contentWidget)
        content_items = set([self.window_ui.contentWidget.item(i).text() for i in range(len_c)])
        self.window_ui.contentWidget.clear()
        for i in content_items:
            self.window_ui.contentWidget.addItem(i)

    def create(self):
        # 删除现有的然后重新创建（用于edit）
        if self.remove_:
            del self.vsp.job_submit_items[self.remove_.text()]
            self.widget.remove(self.remove_)
            self.remove_ = None
            self.update()
        name = self.window_ui.name.text()
        if self.vsp.check_if_same_key(name) == True:
            QMessageBox.critical(self.window, "Error", "Name Exists, Abort")
            return
        host = self.window_ui.hostLineEdit.text()
        port = self.window_ui.portLineEdit.text()
        username = self.window_ui.usernameLineEdit.text()
        password = self.window_ui.passwordLineEdit.text()
        remote_project_path = self.window_ui.remoteProjectPathEdit.text()


        projectType = ProjectType_dict[self.window_ui.projectTypeChoose.currentText()]
        len_c = len(self.window_ui.contentWidget)
        content_items = [self.window_ui.contentWidget.item(i) for i in range(len_c)]

        for i in [name, host, port, username, password, remote_project_path, projectType, content_items]:
            if len(i) == 0:
                QMessageBox.critical(self.window, "Error", "Not Complete")
                return


        content_item_keys = [i.text() for i in content_items]


        JobSubmit_item(
            name=name,
            vsp=self.vsp,
            item_keys=content_item_keys,
            project_type=projectType,
            remote_project_dir=remote_project_path,
            host=host,
            port=port,
            username=username,
            password=password
        )
        self.window.close()
        self.update()


    def new_one(self):
        # 这里建议在designer中设计界面，然后把代码copy到一开始的类中，然后在这里实例化
        self.show(SubmitJobCreateWindow)
        self.window_ui.submitJobOk.clicked.connect(self.create)
        self.window_ui.submitJobCancel.clicked.connect(self.window.close)
        self.window_ui.submitJobRemove.clicked.connect(self.remove_one_content)

    def remove_one_content(self):
        n = len(self.window_ui.contentWidget)
        print(n)
        if n==0:return
        new_items = []
        # remove采用的是把没有selected的append，然后清空再重新创建
        for i in range(n):
            if self.window_ui.contentWidget.item(i).isSelected() == False:
                new_items.append(self.window_ui.contentWidget.item(i).text())
        self.window_ui.contentWidget.clear()
        for i in new_items:
            self.window_ui.contentWidget.addItem(i)

    def check_one(self):
        # 这里已经改成了copy，但是函数名称暂时不变
        for i in self.widget:
            if i.isSelected():

                name = i.text()
                the_item = self.vsp.job_submit_items[name]
                total_item_names = list(self.vsp.job_submit_items.keys())
                base_name = name
                index = 1
                new_name = base_name + str(index)
                while new_name in total_item_names:
                    index += 1
                    new_name = base_name + str(index)

                print(self.vsp.job_submit_items)

                JobSubmit_item(
                    name=new_name,
                    vsp=self.vsp,
                    item_keys=the_item.item_keys,
                    project_type=the_item.project_type,
                    remote_project_dir=the_item.remote_project_dir,
                    host=the_item.host,
                    port=the_item.port,
                    username=the_item.username,
                    password=the_item.password
                )
        self.update()



        return

        for i in self.widget:
            if i.isSelected():
                tmp = self.vsp.job_submit_items[i.text()]
        for file in tmp.file_items:
            print(file.name)
            print(file.path)
        for text_file in tmp.text_items:
            print(text_file.name)
            print(text_file.string)

    def edit_one(self):
        for i in self.widget:
            if i.isSelected():
                self.show(SubmitJobCreateWindow)

                self.window_ui.submitJobCancel.clicked.connect(self.window.close)
                self.window_ui.submitJobRemove.clicked.connect(self.remove_one_content)
                # 不允许cancel，OK直接创建
                self.window_ui.hostLineEdit.setText(self.vsp.job_submit_items[i.text()].host)
                self.window_ui.portLineEdit.setText(self.vsp.job_submit_items[i.text()].port)
                self.window_ui.name.setText(self.vsp.job_submit_items[i.text()].name)

                self.window_ui.usernameLineEdit.setText(self.vsp.job_submit_items[i.text()].username)
                self.window_ui.passwordLineEdit.setText(self.vsp.job_submit_items[i.text()].password)
                self.window_ui.remoteProjectPathEdit.setText(self.vsp.job_submit_items[i.text()].remote_project_dir)

                for z in self.vsp.job_submit_items[i.text()].total_items:
                    self.window_ui.contentWidget.addItem(z)

                # 先创建和当前submit job相同的item，然后创建其他item
                self.window_ui.projectTypeChoose.clear()

                self.window_ui.projectTypeChoose.addItem(self.vsp.job_submit_items[i.text()].project_type)
                for j in ProjectType_dict:
                    if j !=self.vsp.job_submit_items[i.text()].project_type:
                        self.window_ui.projectTypeChoose.addItem(j)
                self.window_ui.projectTypeChoose.setCurrentIndex(0)

                self.window_ui.submitJobOk.clicked.connect(self.create)
                # 先删除，再重新create，点击OK后会删除remove_的，然后重新创建
                self.remove_ = i

                # reject 之后记住删除要remove的，否则edit之后new就会丢失
                def clear():
                    self.remove_ = None
                self.window.rejected.connect(clear)



    def remove_one(self):

        for i in self.widget:
            if i.isSelected():
                del self.vsp.job_submit_items[i.text()]
                self.widget.remove(i)
                self.update()



