# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wang\Documents\GitHub\DFT_Calc\pyqt5program\pyqtProject\VMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VASPStudio(object):
    def setupUi(self, VASPStudio):
        VASPStudio.setObjectName("VASPStudio")
        VASPStudio.resize(1657, 871)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VASPStudio.sizePolicy().hasHeightForWidth())
        VASPStudio.setSizePolicy(sizePolicy)
        VASPStudio.setAccessibleName("")
        self.centralWidget = QtWidgets.QWidget(VASPStudio)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMaximumSize(QtCore.QSize(1657, 826))
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.leftTab = QtWidgets.QTabWidget(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.leftTab.setFont(font)
        self.leftTab.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.leftTab.setAutoFillBackground(False)
        self.leftTab.setTabPosition(QtWidgets.QTabWidget.West)
        self.leftTab.setObjectName("leftTab")
        self.tabProjectInformation = QtWidgets.QWidget()
        self.tabProjectInformation.setAccessibleName("")
        self.tabProjectInformation.setObjectName("tabProjectInformation")
        self.tableWidgetProjectInformation = QtWidgets.QTableWidget(self.tabProjectInformation)
        self.tableWidgetProjectInformation.setGeometry(QtCore.QRect(10, 30, 951, 71))
        self.tableWidgetProjectInformation.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidgetProjectInformation.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidgetProjectInformation.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidgetProjectInformation.setAutoScroll(True)
        self.tableWidgetProjectInformation.setAutoScrollMargin(20)
        self.tableWidgetProjectInformation.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableWidgetProjectInformation.setTabKeyNavigation(True)
        self.tableWidgetProjectInformation.setAlternatingRowColors(True)
        self.tableWidgetProjectInformation.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetProjectInformation.setShowGrid(True)
        self.tableWidgetProjectInformation.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidgetProjectInformation.setCornerButtonEnabled(True)
        self.tableWidgetProjectInformation.setRowCount(0)
        self.tableWidgetProjectInformation.setColumnCount(0)
        self.tableWidgetProjectInformation.setObjectName("tableWidgetProjectInformation")
        self.tableWidgetProjectInformation.horizontalHeader().setVisible(False)
        self.tableWidgetProjectInformation.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetProjectInformation.horizontalHeader().setDefaultSectionSize(179)
        self.tableWidgetProjectInformation.horizontalHeader().setHighlightSections(False)
        self.tableWidgetProjectInformation.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidgetProjectInformation.verticalHeader().setVisible(False)
        self.tableWidgetProjectInformation.verticalHeader().setHighlightSections(True)
        self.tabProjectInformationRefreshButton = QtWidgets.QPushButton(self.tabProjectInformation)
        self.tabProjectInformationRefreshButton.setGeometry(QtCore.QRect(10, 0, 75, 23))
        self.tabProjectInformationRefreshButton.setObjectName("tabProjectInformationRefreshButton")
        self.moleculeViewSettingsText = QtWidgets.QPlainTextEdit(self.tabProjectInformation)
        self.moleculeViewSettingsText.setGeometry(QtCore.QRect(10, 150, 951, 611))
        self.moleculeViewSettingsText.setObjectName("moleculeViewSettingsText")
        self.label = QtWidgets.QLabel(self.tabProjectInformation)
        self.label.setGeometry(QtCore.QRect(10, 110, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Fira Code")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.leftTab.addTab(self.tabProjectInformation, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_5.setGeometry(QtCore.QRect(370, 150, 251, 321))
        self.groupBox_5.setObjectName("groupBox_5")
        self.jobSubmitListWidget = QtWidgets.QListWidget(self.groupBox_5)
        self.jobSubmitListWidget.setGeometry(QtCore.QRect(10, 20, 231, 261))
        self.jobSubmitListWidget.setDragEnabled(True)
        self.jobSubmitListWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.jobSubmitListWidget.setObjectName("jobSubmitListWidget")
        self.submitJobNew = QtWidgets.QPushButton(self.groupBox_5)
        self.submitJobNew.setGeometry(QtCore.QRect(10, 290, 51, 23))
        self.submitJobNew.setObjectName("submitJobNew")
        self.submitJobRemove = QtWidgets.QPushButton(self.groupBox_5)
        self.submitJobRemove.setGeometry(QtCore.QRect(130, 290, 51, 23))
        self.submitJobRemove.setObjectName("submitJobRemove")
        self.submitJobEdit = QtWidgets.QPushButton(self.groupBox_5)
        self.submitJobEdit.setGeometry(QtCore.QRect(70, 290, 51, 23))
        self.submitJobEdit.setObjectName("submitJobEdit")
        self.submitJobCheck = QtWidgets.QPushButton(self.groupBox_5)
        self.submitJobCheck.setGeometry(QtCore.QRect(190, 290, 51, 23))
        self.submitJobCheck.setObjectName("submitJobCheck")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_6.setGeometry(QtCore.QRect(750, 580, 251, 211))
        self.groupBox_6.setObjectName("groupBox_6")
        self.textItemListWidget = QtWidgets.QListWidget(self.groupBox_6)
        self.textItemListWidget.setGeometry(QtCore.QRect(10, 20, 231, 151))
        self.textItemListWidget.setDragEnabled(True)
        self.textItemListWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.textItemListWidget.setObjectName("textItemListWidget")
        self.textItemNew = QtWidgets.QPushButton(self.groupBox_6)
        self.textItemNew.setGeometry(QtCore.QRect(10, 180, 51, 23))
        self.textItemNew.setObjectName("textItemNew")
        self.textItemRemove = QtWidgets.QPushButton(self.groupBox_6)
        self.textItemRemove.setGeometry(QtCore.QRect(130, 180, 51, 23))
        self.textItemRemove.setObjectName("textItemRemove")
        self.textItemEdit = QtWidgets.QPushButton(self.groupBox_6)
        self.textItemEdit.setGeometry(QtCore.QRect(70, 180, 51, 23))
        self.textItemEdit.setObjectName("textItemEdit")
        self.textItemCheck = QtWidgets.QPushButton(self.groupBox_6)
        self.textItemCheck.setGeometry(QtCore.QRect(190, 180, 51, 23))
        self.textItemCheck.setObjectName("textItemCheck")
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_7.setGeometry(QtCore.QRect(0, 580, 251, 211))
        self.groupBox_7.setObjectName("groupBox_7")
        self.fileWidget = QtWidgets.QListWidget(self.groupBox_7)
        self.fileWidget.setGeometry(QtCore.QRect(10, 20, 231, 151))
        self.fileWidget.setDragEnabled(True)
        self.fileWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.fileWidget.setObjectName("fileWidget")
        self.newFile = QtWidgets.QPushButton(self.groupBox_7)
        self.newFile.setGeometry(QtCore.QRect(10, 180, 51, 23))
        self.newFile.setObjectName("newFile")
        self.removeFile = QtWidgets.QPushButton(self.groupBox_7)
        self.removeFile.setGeometry(QtCore.QRect(130, 180, 51, 23))
        self.removeFile.setObjectName("removeFile")
        self.editFile = QtWidgets.QPushButton(self.groupBox_7)
        self.editFile.setGeometry(QtCore.QRect(70, 180, 51, 23))
        self.editFile.setObjectName("editFile")
        self.checkFile = QtWidgets.QPushButton(self.groupBox_7)
        self.checkFile.setGeometry(QtCore.QRect(190, 180, 51, 23))
        self.checkFile.setObjectName("checkFile")
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_8.setGeometry(QtCore.QRect(250, 580, 251, 211))
        self.groupBox_8.setObjectName("groupBox_8")
        self.functionListWidget = QtWidgets.QListWidget(self.groupBox_8)
        self.functionListWidget.setGeometry(QtCore.QRect(10, 20, 231, 151))
        self.functionListWidget.setDragEnabled(True)
        self.functionListWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.functionListWidget.setObjectName("functionListWidget")
        self.newFunction = QtWidgets.QPushButton(self.groupBox_8)
        self.newFunction.setGeometry(QtCore.QRect(10, 180, 51, 23))
        self.newFunction.setObjectName("newFunction")
        self.removeFunction = QtWidgets.QPushButton(self.groupBox_8)
        self.removeFunction.setGeometry(QtCore.QRect(130, 180, 51, 23))
        self.removeFunction.setObjectName("removeFunction")
        self.editFunction = QtWidgets.QPushButton(self.groupBox_8)
        self.editFunction.setGeometry(QtCore.QRect(70, 180, 51, 23))
        self.editFunction.setObjectName("editFunction")
        self.checkFunction = QtWidgets.QPushButton(self.groupBox_8)
        self.checkFunction.setGeometry(QtCore.QRect(190, 180, 51, 23))
        self.checkFunction.setObjectName("checkFunction")
        self.groupBox_9 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_9.setGeometry(QtCore.QRect(500, 580, 251, 211))
        self.groupBox_9.setObjectName("groupBox_9")
        self.keyListWidget = QtWidgets.QListWidget(self.groupBox_9)
        self.keyListWidget.setGeometry(QtCore.QRect(10, 20, 231, 151))
        self.keyListWidget.setDragEnabled(True)
        self.keyListWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.keyListWidget.setObjectName("keyListWidget")
        self.keyNew = QtWidgets.QPushButton(self.groupBox_9)
        self.keyNew.setGeometry(QtCore.QRect(10, 180, 51, 23))
        self.keyNew.setObjectName("keyNew")
        self.keyRemove = QtWidgets.QPushButton(self.groupBox_9)
        self.keyRemove.setGeometry(QtCore.QRect(130, 180, 51, 23))
        self.keyRemove.setObjectName("keyRemove")
        self.keyEdit = QtWidgets.QPushButton(self.groupBox_9)
        self.keyEdit.setGeometry(QtCore.QRect(70, 180, 51, 23))
        self.keyEdit.setObjectName("keyEdit")
        self.keyCheck = QtWidgets.QPushButton(self.groupBox_9)
        self.keyCheck.setGeometry(QtCore.QRect(190, 180, 51, 23))
        self.keyCheck.setObjectName("keyCheck")
        self.leftTab.addTab(self.tab, "")
        self.tabXSDFiles = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.tabXSDFiles.setFont(font)
        self.tabXSDFiles.setObjectName("tabXSDFiles")
        self.xsdFilesRefreshButton = QtWidgets.QPushButton(self.tabXSDFiles)
        self.xsdFilesRefreshButton.setGeometry(QtCore.QRect(0, 770, 75, 23))
        self.xsdFilesRefreshButton.setObjectName("xsdFilesRefreshButton")
        self.xsdFileTreeWidget = QtWidgets.QTreeWidget(self.tabXSDFiles)
        self.xsdFileTreeWidget.setGeometry(QtCore.QRect(0, 0, 1261, 761))
        self.xsdFileTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.xsdFileTreeWidget.setStyleSheet("")
        self.xsdFileTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.xsdFileTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.xsdFileTreeWidget.setDragEnabled(True)
        self.xsdFileTreeWidget.setDragDropOverwriteMode(True)
        self.xsdFileTreeWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.xsdFileTreeWidget.setAlternatingRowColors(True)
        self.xsdFileTreeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.xsdFileTreeWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.xsdFileTreeWidget.setIndentation(15)
        self.xsdFileTreeWidget.setObjectName("xsdFileTreeWidget")
        self.xsdFileTreeWidget.headerItem().setText(0, "1")
        item_0 = QtWidgets.QTreeWidgetItem(self.xsdFileTreeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        self.xsdFileTreeWidget.header().setDefaultSectionSize(200)
        self.xsdFileTreeWidget.header().setHighlightSections(True)
        self.xsdFileTreeWidget.header().setSortIndicatorShown(True)
        self.commandOutput = QtWidgets.QTextBrowser(self.tabXSDFiles)
        self.commandOutput.setGeometry(QtCore.QRect(1260, 500, 351, 261))
        self.commandOutput.setObjectName("commandOutput")
        self.xsdFileRunQstat = QtWidgets.QPushButton(self.tabXSDFiles)
        self.xsdFileRunQstat.setGeometry(QtCore.QRect(1260, 770, 75, 23))
        self.xsdFileRunQstat.setObjectName("xsdFileRunQstat")
        self.xsdFileInformation = QtWidgets.QTextEdit(self.tabXSDFiles)
        self.xsdFileInformation.setGeometry(QtCore.QRect(1260, 0, 351, 501))
        self.xsdFileInformation.setReadOnly(True)
        self.xsdFileInformation.setObjectName("xsdFileInformation")
        self.leftTab.addTab(self.tabXSDFiles, "")
        self.horizontalLayout_2.addWidget(self.leftTab)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        VASPStudio.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(VASPStudio)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1657, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuProject = QtWidgets.QMenu(self.menuBar)
        self.menuProject.setObjectName("menuProject")
        self.menuOpenWindows = QtWidgets.QMenu(self.menuBar)
        self.menuOpenWindows.setObjectName("menuOpenWindows")
        VASPStudio.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(VASPStudio)
        self.statusBar.setObjectName("statusBar")
        VASPStudio.setStatusBar(self.statusBar)
        self.actionNewProject = QtWidgets.QAction(VASPStudio)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionOpenProject = QtWidgets.QAction(VASPStudio)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionClose = QtWidgets.QAction(VASPStudio)
        self.actionClose.setObjectName("actionClose")
        self.actionSaveProject = QtWidgets.QAction(VASPStudio)
        self.actionSaveProject.setObjectName("actionSaveProject")
        self.about = QtWidgets.QAction(VASPStudio)
        self.about.setObjectName("about")
        self.menuProject.addAction(self.actionNewProject)
        self.menuProject.addAction(self.actionOpenProject)
        self.menuProject.addAction(self.actionSaveProject)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionClose)
        self.menuOpenWindows.addAction(self.about)
        self.menuBar.addAction(self.menuProject.menuAction())
        self.menuBar.addAction(self.menuOpenWindows.menuAction())

        self.retranslateUi(VASPStudio)
        self.leftTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VASPStudio)

    def retranslateUi(self, VASPStudio):
        _translate = QtCore.QCoreApplication.translate
        VASPStudio.setWindowTitle(_translate("VASPStudio", "VASP Studio"))
        self.tableWidgetProjectInformation.setSortingEnabled(False)
        self.tabProjectInformationRefreshButton.setText(_translate("VASPStudio", "Refresh"))
        self.label.setText(_translate("VASPStudio", "Molecule View Settings"))
        self.leftTab.setTabText(self.leftTab.indexOf(self.tabProjectInformation), _translate("VASPStudio", "Settings"))
        self.groupBox_5.setTitle(_translate("VASPStudio", "Job Submit"))
        self.submitJobNew.setText(_translate("VASPStudio", "New"))
        self.submitJobRemove.setText(_translate("VASPStudio", "Remove"))
        self.submitJobEdit.setText(_translate("VASPStudio", "Edit"))
        self.submitJobCheck.setText(_translate("VASPStudio", "Copy"))
        self.groupBox_6.setTitle(_translate("VASPStudio", "Text File Library"))
        self.textItemNew.setText(_translate("VASPStudio", "New"))
        self.textItemRemove.setText(_translate("VASPStudio", "Remove"))
        self.textItemEdit.setText(_translate("VASPStudio", "Edit"))
        self.textItemCheck.setText(_translate("VASPStudio", "Check"))
        self.groupBox_7.setTitle(_translate("VASPStudio", "File Library"))
        self.newFile.setText(_translate("VASPStudio", "New"))
        self.removeFile.setText(_translate("VASPStudio", "Remove"))
        self.editFile.setText(_translate("VASPStudio", "Edit"))
        self.checkFile.setText(_translate("VASPStudio", "Check"))
        self.groupBox_8.setTitle(_translate("VASPStudio", "TF Function Library"))
        self.newFunction.setText(_translate("VASPStudio", "New"))
        self.removeFunction.setText(_translate("VASPStudio", "Remove"))
        self.editFunction.setText(_translate("VASPStudio", "Edit"))
        self.checkFunction.setText(_translate("VASPStudio", "Check"))
        self.groupBox_9.setTitle(_translate("VASPStudio", "Key Value Library"))
        self.keyNew.setText(_translate("VASPStudio", "New"))
        self.keyRemove.setText(_translate("VASPStudio", "Remove"))
        self.keyEdit.setText(_translate("VASPStudio", "Edit"))
        self.keyCheck.setText(_translate("VASPStudio", "Check"))
        self.leftTab.setTabText(self.leftTab.indexOf(self.tab), _translate("VASPStudio", "File Library"))
        self.xsdFilesRefreshButton.setText(_translate("VASPStudio", "Refresh"))
        self.xsdFileTreeWidget.setSortingEnabled(True)
        self.xsdFileTreeWidget.headerItem().setText(1, _translate("VASPStudio", "New Column"))
        self.xsdFileTreeWidget.headerItem().setText(2, _translate("VASPStudio", "New Column"))
        self.xsdFileTreeWidget.headerItem().setText(3, _translate("VASPStudio", "New Column"))
        self.xsdFileTreeWidget.headerItem().setText(4, _translate("VASPStudio", "2"))
        __sortingEnabled = self.xsdFileTreeWidget.isSortingEnabled()
        self.xsdFileTreeWidget.setSortingEnabled(False)
        self.xsdFileTreeWidget.topLevelItem(0).setText(0, _translate("VASPStudio", "New Item"))
        self.xsdFileTreeWidget.topLevelItem(0).child(0).setText(0, _translate("VASPStudio", "New Subitem"))
        self.xsdFileTreeWidget.topLevelItem(0).child(0).child(0).setText(0, _translate("VASPStudio", "New Subitem"))
        self.xsdFileTreeWidget.topLevelItem(0).child(0).child(0).child(0).setText(0, _translate("VASPStudio", "New Subitem"))
        self.xsdFileTreeWidget.topLevelItem(0).child(0).child(0).child(1).setText(0, _translate("VASPStudio", "New Item"))
        self.xsdFileTreeWidget.topLevelItem(0).child(0).child(0).child(2).setText(0, _translate("VASPStudio", "New Item"))
        self.xsdFileTreeWidget.setSortingEnabled(__sortingEnabled)
        self.commandOutput.setHtml(_translate("VASPStudio", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.xsdFileRunQstat.setText(_translate("VASPStudio", "Run qstat"))
        self.leftTab.setTabText(self.leftTab.indexOf(self.tabXSDFiles), _translate("VASPStudio", "XSD File And Job Submit"))
        self.menuProject.setTitle(_translate("VASPStudio", "Project"))
        self.menuOpenWindows.setTitle(_translate("VASPStudio", "Help"))
        self.actionNewProject.setText(_translate("VASPStudio", "New Project"))
        self.actionOpenProject.setText(_translate("VASPStudio", "Open Project ..."))
        self.actionClose.setText(_translate("VASPStudio", "Close"))
        self.actionSaveProject.setText(_translate("VASPStudio", "Save"))
        self.actionSaveProject.setShortcut(_translate("VASPStudio", "Ctrl+S"))
        self.about.setText(_translate("VASPStudio", "About"))
        self.moleculeViewSettingsText.toPlainText()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VASPStudio = QtWidgets.QMainWindow()
    ui = Ui_VASPStudio()
    ui.setupUi(VASPStudio)
    VASPStudio.show()
    sys.exit(app.exec_())

