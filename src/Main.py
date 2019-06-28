# -*- coding: UTF-8 -*-

# 全局设置

# 添加分子三维展示功能
ADD_MOLECULE_SHOW = True

'''
关于项目目录设置：
    因为编译需要，所以不能使用from src.VaspXXX import 
    而是直接from VaspXXX import
    因此pycharm ide会出现找不到的情况，而实际上又能够顺利运行
解决方法：
    ide中project interpreter-下拉-show all 然后
    在右边侧边栏文件夹一样的图标中点开添加上当前的src目录

树形列表中的UI读取模型的设计：
    标题是字符串，
    xvi试图去获取这些字符串的attr，获取不到就是None
    扩展一个新功能：
        使用xvi传参，修改xvi参数，
        然后在self.xsd_file_contents中加上这个标题栏即可，
        之后update_xsd_file_information自己会根据标题栏的这些字符串去获取attr显示
    所有与UI显示相关的信息，全部存储在XVI实例中
    每次pickle保存这些信息

关于投job：
    将一个job需要的文件和xvi相关的信息写入的json文件，以及投job的python脚本上传到云端
    然后运行python命令     

'''

# TODO: 增加自动下载功能
# TODO： 虚频的英文单词有误，不能为virtual_freq，而应该是imaginary freq


import os

# 检查投job的文件是不是在根目录下
if not os.path.exists("submit_job_onserver.py"):
    raise ValueError("You need submit job on server file in v0.22")

if ADD_MOLECULE_SHOW:
    # print(ETSConfig.toolkit)
    # os.environ['QT_API'] = 'pyqt5'
    from traits.etsconfig.api import ETSConfig

    ETSConfig.toolkit = "wx"
    os.environ['ETS_TOOLKIT'] = 'wx'
    from VASPStuMoleculeViewSubmit import submit_plot

import copy
import shutil
import sys
from VSP_ItemCollection import XSD_VASP_item
from SFTP_SSH_Utils import SFTP_SSH_Utils

sys.setrecursionlimit(50000)
from VASPStuEnergyManager import VASPFreqExtract, VASP_RMS_Extract, VASPEnergyExtract
from PySide2.QtCore import QCoreApplication, QThread
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QTableWidgetItem, QTreeWidgetItem, QInputDialog, \
    QDialog, QColorDialog, QMenu, QMessageBox, QFileDialog
from PySide2.QtGui import QBrush, QColor, QCursor
from VASPStuProject import VASPStuProject
import sys
from ItemWindow import File_Item_Window, Text_File_Item_Window, TF_Window, Key_Item_Window, SubmitJob_Window
from VASPStuStructureManager import VASPStuStructureManager
from VASPStuFileLinker import VASPStuFileLinker
from Ui_about import Ui_about
from Ui_CreateProject import Ui_CreateProject
from Ui_VMainWindow import Ui_VASPStudio
from Ui_SubmitJob import Ui_submitJob
from public import Status, Type, Type_Color, STATUS_COLOR, Checker, XVI_Status
import traceback

# 默认的分子绘图设置
default_molecule_view_setting_text = \
    '''
    # the radius of atom when plot 
    atom_radius_config={
    "H": 0.8,
    "C": 1,
    "O": 1,
    "Pt": 2,
    "Au":2,
    }
    # the rgb of atom when plot
    atom_color_config={
    "H": (255, 255, 255),
    "C": (130, 130, 130),
    "O": (255, 0, 0),
    "Pt": (93, 123, 195),
    "Au":(0,255,255),
    }
    # e,g. ("H", "C"): 1.8 means we make bond C-H when H and C distance is lower than 1.8
    bond_config={
    ("H", "C"): 1.8,  
    ("Pt", "C"): 3,
    ("Pt", "O"): 3,
    ("Pt", "H"): 2,
    ("C", "O"): 1.8,
    ("H", "O"): 1.8,
    ("C", "C"): 1.8,
    }
    bond_radius=0.2
    # for period structure XYZ e.g. 1,1,0 means 3x3x1; 0,0,0 means 1x1x1; 2,2,1 means 5x5x3           
    repeat_config=(0, 0, 0)
    background_color=(255, 255, 255)
    # initial window size
    window_sizeX= 1280            
    window_sizeY=960
    # resolution, important for graph and speed
    circle_resolution=40
    tube_resolution=20
    '''


class Main():
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.xsd_files_item = []
        # UI 创建，UI使用qt designer设计得到.ui文件，使用pyuic或者ide(pycharm亦可)导出py，构造后引用
        self.main_window = QtWidgets.QMainWindow()
        self.main_window_ui = Ui_VASPStudio()
        self.main_window_ui.setupUi(self.main_window)
        self.create_project = QtWidgets.QDialog()
        self.create_project_ui = Ui_CreateProject()
        self.create_project_ui.setupUi(self.create_project)
        self.about_window = QtWidgets.QDialog()
        self.about_window_ui = Ui_about()
        self.about_window_ui.setupUi(self.about_window)
        # 固定大小
        self.main_window.setFixedSize(self.main_window.width(), self.main_window.height())

        self.last_save_path = None
        self.vsp = None

        # 控制台输出，等同于GUI界面的控制台输出结果，用于分析
        self.command_output = ""

        # 绑定ui中的按钮和函数
        self.binding_main_window()
        self.binding_create_project_window()

        # 注意header要多一行，header的string会用getattr来获得xvi items中的内容
        self.xsd_file_headers = ["File", "Status", "Type", "Mark", "Energy", "Final RMS", "Work Node", "Job",
                                 "Match State", "备注"]
        self.xsd_file_contents = ["status", "type", "mark_text", "energy", "final_RMS", "nodel", "submit_job",
                                  "match_state", "note"]

    def main_window_error(self, string):
        QMessageBox.critical(self.main_window, "Error", string)

    def main_window_info(self, string):
        QMessageBox.information(self.main_window, "Information", string)

    def main_window_warn(self, string):
        QMessageBox.warning(self.main_window, "Warning", string)

    def generate_item_window(self):
        '''
        main window中已经创建了UI，现在把里面的子window的ui组件(按钮为主)分配到ItemWindow中，用于添加函数增加控制行为
        同时将vsp中保存的item更新到UI界面，Model -> View
        '''
        self.text_item_window = Text_File_Item_Window(
            main_window=self.main_window,
            vsp=self.vsp,
            new_button=self.main_window_ui.textItemNew,
            edit_button=self.main_window_ui.textItemEdit,
            remove_button=self.main_window_ui.textItemRemove,
            check_button=self.main_window_ui.textItemCheck,
            list_widget=self.main_window_ui.textItemListWidget
        )
        self.text_item_window.update()

        self.file_item_window = File_Item_Window(
            main_window=self.main_window,
            vsp=self.vsp,
            new_button=self.main_window_ui.newFile,
            edit_button=self.main_window_ui.editFile,
            remove_button=self.main_window_ui.removeFile,
            check_button=self.main_window_ui.checkFile,
            list_widget=self.main_window_ui.fileWidget
        )
        self.file_item_window.update()

        self.tf_window = TF_Window(
            main_window=self.main_window,
            vsp=self.vsp,
            new_button=self.main_window_ui.newFunction,
            edit_button=self.main_window_ui.editFunction,
            remove_button=self.main_window_ui.removeFunction,
            check_button=self.main_window_ui.checkFunction,
            list_widget=self.main_window_ui.functionListWidget
        )
        self.tf_window.update()

        self.key_item_window = Key_Item_Window(
            main_window=self.main_window,
            vsp=self.vsp,
            new_button=self.main_window_ui.keyNew,
            edit_button=self.main_window_ui.keyEdit,
            remove_button=self.main_window_ui.keyRemove,
            check_button=self.main_window_ui.keyCheck,
            list_widget=self.main_window_ui.keyListWidget
        )
        self.key_item_window.update()

        self.job_submit_window = SubmitJob_Window(
            main_window=self.main_window,
            vsp=self.vsp,
            new_button=self.main_window_ui.submitJobNew,
            edit_button=self.main_window_ui.submitJobEdit,
            remove_button=self.main_window_ui.submitJobRemove,
            check_button=self.main_window_ui.submitJobCheck,
            list_widget=self.main_window_ui.jobSubmitListWidget

        )
        self.job_submit_window.update()

    def refresh(self):
        '''
        检测新文件，更新xsd文件信息
        '''
        self.check_file_change_and_update_file()
        self.update_xsd_files_information()

    def binding_main_window(self):
        '''
        绑定菜单栏的函数
        '''
        # 绑定打开项目对话框
        self.main_window_ui.actionNewProject.triggered.connect(self.create_project.show)
        self.main_window_ui.tabProjectInformationRefreshButton.clicked.connect(self.update_project_information)
        self.main_window_ui.actionOpenProject.triggered.connect(self.load_vs_project)
        self.main_window_ui.xsdFilesRefreshButton.clicked.connect(self.refresh)
        self.main_window_ui.actionSaveProject.triggered.connect(self.save_project)

        # 以下代码是原来按钮控制的，现在改为了右键菜单控制
        # self.main_window_ui.xsdFileSubmitJobButton.clicked.connect(self.submit_job)
        # self.main_window_ui.xsdFileLocalLinkByName.clicked.connect(self.submit_file_link_by_name)
        # self.main_window_ui.xsdFileLocalLinkByPath.clicked.connect(self.submit_file_link_by_path)
        # self.main_window_ui.xsdFileEnergyExtract.clicked.connect(self.submit_energy_collect)
        # self.main_window_ui.about.triggered.connect(self.about_window.show)
        # self.main_window_ui.xsdFileRMSExtract.clicked.connect(self.submit_RMS_extract)
        # self.main_window_ui.xsdFileFreq.clicked.connect(self.submit_freq_extract)
        # self.main_window_ui.xsdFileGrepCommand.clicked.connect(self.submit_grep_command)
        # self.main_window_ui.xsdFileUpdate.clicked.connect(self.submit_update)
        # self.main_window_ui.taskCancel.clicked.connect(self.run_task_cancel_command)
        # self.main_window_ui.xsdFileDelete.clicked.connect(self.xsd_file_delete)
        # self.main_window_ui.xsdFileTreeWidget.doubleClicked.connect(self.open_xsd_file)
        # self.main_window_ui.xsdFileTreeWidget.doubleClicked.connect(self.show_3d_coordinate)
        # self.main_window_ui.xsdFileExportFinalStructure.clicked.connect(self.submit_structure_export)
        # self.main_window_ui.xsdFileMark.clicked.connect(self.submit_mark)
        # self.main_window_ui.xsdFileButtonChangeToNotSubmit.clicked.connect(self.change_to_not_submit)
        # self.main_window_ui.runQstatButton.clicked.connect(self.run_qstat_command)
        # 选中的item显示所有信息

        self.main_window_ui.xsdFileRunQstat.clicked.connect(self.run_qstat_command)
        self.main_window_ui.xsdFileTreeWidget.itemSelectionChanged.connect(self.update_item_information)
        self.add_right_memu_to_xsdFileTreeWidget()

    def show_xsdFile_right_menu(self):
        '''
        右键行为
        '''
        self.xsdFileRightMenu.exec_(QCursor.pos())

    def add_right_memu_to_xsdFileTreeWidget(self):
        '''
        绑定右键按键函数，分类
        '''
        # 右键菜单
        self.xsdFileRightMenu = QMenu(self.main_window_ui.xsdFileTreeWidget)
        # 分子展示
        self.a_view_action = self.xsdFileRightMenu.addAction("View Molecule")
        self.a_view_action.triggered.connect(self.submit_view_molecule)
        self.xsdFileRightMenu.addSeparator()  # 分隔符
        # 任务mark
        self.a_mark_action = self.xsdFileRightMenu.addAction("Mark")
        self.a_mark_action.triggered.connect(self.submit_mark)
        self.xsdFileRightMenu.addSeparator()
        # 提交任务
        self.a_submit_job = self.xsdFileRightMenu.addAction("Submit Job")
        self.a_submit_job.triggered.connect(self.submit_job)
        self.xsdFileRightMenu.addSeparator()
        # 任务状态控制
        self.m_status_control = self.xsdFileRightMenu.addMenu("Status")
        self.a_turn_not_submit = self.m_status_control.addAction("Turn Not Submit")
        self.a_turn_not_submit.triggered.connect(self.change_to_not_submit)
        # task control
        # TODO:增加stop 命令
        pass

        # download TODO：

        pass
        # 本地文件关联
        self.m_local_link = self.xsdFileRightMenu.addMenu("Local Link")
        self.a_by_path = self.m_local_link.addAction("By Path")
        self.a_by_name = self.m_local_link.addAction("By Name")
        self.a_by_name.triggered.connect(self.submit_file_link_by_name)
        self.a_by_path.triggered.connect(self.submit_file_link_by_path)
        # vasp文件的信息提取
        self.m_information = self.xsdFileRightMenu.addMenu("Information")
        self.a_rms = self.m_information.addAction("Final RMS")
        self.a_energy = self.m_information.addAction("Final Energy")
        self.a_freq = self.m_information.addAction("Frequency")
        self.a_grep = self.m_information.addAction("grep ... OUTCAR")
        self.m_information.addSeparator()
        self.a_info_export_csv = self.m_information.addAction("Export information to csv")
        self.a_info_export_csv.triggered.connect(self.submit_information_export)
        self.a_info_export_freq_to_dict = self.m_information.addAction("Export Freq to dict file for catmap")
        self.a_info_export_freq_to_dict.triggered.connect(self.submit_export_freq_to_dict)
        self.a_rms.triggered.connect(self.submit_RMS_extract)
        self.a_energy.triggered.connect(self.submit_energy_collect)
        self.a_freq.triggered.connect(self.submit_freq_extract)
        self.a_grep.triggered.connect(self.submit_grep_command)
        # 结构导出
        self.m_structure = self.xsdFileRightMenu.addMenu("Structure")
        self.a_structure_export = self.m_structure.addAction("Export Final Structure")
        self.a_structure_export.triggered.connect(self.submit_structure_export)
        # 导出信息到文件
        self.m_file_control = self.xsdFileRightMenu.addMenu("File")
        self.a_outcar_export = self.m_file_control.addAction("Export OUTCAR in dir")
        self.a_outcar_export.triggered.connect(self.submit_outcar_export)
        self.a_delete_file = self.m_file_control.addAction("Delete")
        self.a_delete_file.triggered.connect(self.xsd_file_delete)

        self.main_window_ui.xsdFileTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.main_window_ui.xsdFileTreeWidget.customContextMenuRequested.connect(self.show_xsdFile_right_menu)
        # 双击一个item，绘制分子
        self.main_window_ui.xsdFileTreeWidget.doubleClicked.connect(self.submit_view_molecule)

    def open_xsd_file(self):
        '''
        将xsd文件用外部程序，如Material Studio打开
        '''
        for i in self.xsd_files_item:
            if i.isSelected():
                print(i.file_path)
                try:
                    os.startfile(self.vsp.local_project_dir + "/" + i.file_path)
                except:
                    traceback.print_exc()
                break

    def binding_create_project_window(self):
        '''
        project create windows的函数绑定
        '''

        self.create_project_ui.localProjectPathButton.clicked.connect(
            self.file_dialog_local_project_path)
        # 直接将ok按钮绑定创建project，如果不合理会弹出警告，合理会创建然后close
        self.create_project_ui.projectOkButton.clicked.connect(self.create_vs_project)
        pass

    def load_vs_project(self):
        '''
        载入项目文件，原先设计有密码，现在关闭密码，为了兼容设置固定密码为123(用于加密)
        '''

        vsp_file = QFileDialog.getOpenFileName(
            self.main_window,
            "Open .vsp file",
            "C:/",
            "VASP Studio Project File (*.vsp)"
        )[0]

        if len(vsp_file) == 0: return
        # 默认密码123，载入得到vsp实例
        vs = self.check(self.main_window, VASPStuProject.read_existing_project(vsp_file, "123"))
        if vs == Status.FAILED:
            key = \
                QInputDialog(self.main_window).getText(self.main_window, "Please insert the project key",
                                                       "Project Key")[0]
            vs = self.check(self.main_window, VASPStuProject.read_existing_project(vsp_file, key))
            self.vsp = vs
        elif isinstance(vs, VASPStuProject):
            self.vsp = vs
        self.after_open_or_load()

    def create_vs_project(self):
        '''
        创建项目，从文件浏览窗口中获得路径text来创建
        '''
        try:
            self.local_project_path = self.create_project_ui.localProjectPathEdit.text()
        except:
            QMessageBox.critical(self.create_project, "Error", "Not complete")
            return

        self.vsp = VASPStuProject(local_project_dir=self.local_project_path,
                                  project_key="123")

        with open(self.vsp.local_project_dir + "/" + "temp", "w") as f:
            f.write("")

        # 是否覆盖已有文件，如果是就写入，否则不关闭窗口
        if self.save_project() == False: return

        # 进行检查，否则要求重新输入
        # if self.project_check() == False: return

        self.create_project.close()
        self.after_open_or_load()

    def after_open_or_load(self):
        '''
        打开或者载入项目后的行为
        '''
        # 旧版本vsp文件更新
        self.vsp.update_old_version()
        # 更新分子设置
        self.update_molecule_view_plot_settings()
        # 文件改动
        self.check_file_change_and_update_file()
        # ui信息更新
        self.update_project_information()
        self.update_xsd_files_information()
        # 窗口添加
        self.generate_item_window()

    def update_molecule_view_plot_settings(self):
        if ADD_MOLECULE_SHOW == False:
            self.main_window_ui.moleculeViewSettingsText.setPlainText('''分子绘制功能未打开''')
            self.main_window_ui.moleculeViewSettingsText.setReadOnly(True)
            return
        try:
            self.main_window_ui.moleculeViewSettingsText.setPlainText(self.vsp.molecule_view_setting_text)
        except:
            self.main_window_ui.moleculeViewSettingsText.setPlainText(default_molecule_view_setting_text)
            traceback.print_exc()

    def save_project(self):
        '''
        项目文件保存，使用pickle
        '''
        if self.vsp is None:
            return

        if self.vsp.class_data_save_path is None:
            path = QFileDialog.getSaveFileName(
                self.main_window,
                "Save .vsp file",
                "C:/",
                "VASP Studio Project File (*.vsp)"
            )[0]
            if path == "":
                return
            self.vsp.class_data_save_path = path
        else:
            path = self.vsp.class_data_save_path

        tw = self.main_window_ui.xsdFileTreeWidget
        n = []
        # 存储标题栏的宽度
        for i in range(tw.columnCount()):
            n.append(tw.columnWidth(i))
        expand_state_dict = {}
        # 存储文件树展开的情况,注意需要使用node去获取信息
        try:
            for key in self.tree_node_widget_item_info:
                expand_state_dict[key] = self.tree_node_widget_item_info[key].isExpanded()
        except:
            pass
        # 存储展开信息和标题栏宽度
        self.vsp.xsd_tree_widget_param["expanded_status"] = expand_state_dict
        self.vsp.xsd_tree_widget_param["column_status"] = n
        self.vsp.molecule_view_setting_text = self.main_window_ui.moleculeViewSettingsText.toPlainText()
        # 如果保存了一次，变为new save，因为新保存的密码固定了
        self.vsp.new_save = True
        self.vsp.save_project_info(path)
        QMessageBox.information(self.main_window, "提示", "已保存")
        return True

    def check_file_change_and_update_file(self):
        '''
        检测文件改动
        '''
        new_files, deleted_files = self.vsp.check_and_add_new_xsd_files_and_generate_XVI()
        if new_files == False:  # 这个是由底层传来的，不只是文件，还有status以及错误信息
            # 这里newFiles是错误时传来的status，deletedFiles是信息
            QMessageBox.critical(self.main_window, "Error", deleted_files)
            return
        # 之所以需要self.vs.new_files，是因为希望在一开始创建项目时就保存项目
        if len(new_files) == 0 and len(deleted_files) == 0: return
        string = ""
        if len(new_files) >= 1:
            string += "检测到新增%s个以下文件:" % len(new_files)
            string += "\n".join(new_files)
        if len(deleted_files) >= 1:
            string += "检测到删除%s个以下文件" % len(deleted_files)
            string += "\n".join(deleted_files)
        QMessageBox.information(self.create_project,
                                "File changes",
                                string)

    def project_check(self):
        if self.check(self.create_project, self.vsp.submit_job_file_check) == False: return False
        if self.check(self.create_project, self.vsp.base_file_check) == False:  return False
        if self.check(self.create_project, self.vsp.connect_remote_project_dir_check) == False: return False
        QMessageBox.information(self.create_project, "Information", "Success. 为确保顺利运行，请检查：\n服务器端是否有新创建的checkFile文件")

    def update_item_information(self):
        # 选中后增加具体的信息
        if self.xsd_files_item == []:
            return
        self.selected_items = []
        for i in self.xsd_files_item:
            # 选中的对象
            if i.isSelected():
                xvis = self.vsp.get_XVI_from_relative_xsd_files([str(i.file_path)])[0]
                content = ""
                for key in xvis.__dict__:
                    # getattr的字符串
                    if key in ["local_vasp_dir",
                               "energy",
                               "final_RMS",
                               "relative_xsd_file",
                               "status",
                               "nodel",
                               "note",
                               "type",
                               "mark_text",
                               "RMS_array",
                               "submit_job",
                               "real_freq",
                               "virtual_freq",
                               "match_state"
                               ]:
                        content += "<b><font size=4 >%s</font><br></b>" % key
                        content += "<font size=4>%s</font><br>" % getattr(xvis, key, "")

                        self.main_window_ui.xsdFileInformation.setText(content)

    def update_xsd_files_information(self):
        '''
        update 函数直接与vs类关联，得到所有的文件类，这样只用update就能更新最新
        '''
        if self.vsp == None:
            QMessageBox.information(self.main_window, "提示", "没有加载项目，无法获得xsd文件")
            return
        self.xsd_files_item = []
        try:
            filenames = list(self.vsp.relative_path_XVI_dict.keys())
            filenames = sorted(filenames)
            tw = self.main_window_ui.xsdFileTreeWidget
            index = 0
            tw.clear()
            tw.setHeaderLabels(self.xsd_file_headers)
            tw.setColumnCount(len(self.xsd_file_headers))
            file_name_item_dict = {}
            root = QTreeWidgetItem(tw)
            root.setText(0, self.vsp.local_project_dir)
            # 创建文件树
            for file in filenames:
                # 根，也就是项目目录
                l = [root]
                # 之后的文件树相对于项目目录
                trees = file.split("/")[1:]

                # 按照文件目录树进行，如果能够获取到子集就开始增加内容，否则增加child
                for i in range(len(trees) + 1):
                    # 每次+1地获取后面几层的文件，比如这里的node name分别为： a -> a/c -> a/c/d
                    node_name = "/".join(trees[:i])
                    try:  # 尝试找到这个node，如果没有就创建
                        node = file_name_item_dict[node_name]
                    except:
                        # 创建child node，加入到字典中
                        node = QTreeWidgetItem(l[-1])
                        index += 1
                        # 注意text设置为最后一个，比如a/c/d就是d，a/c就是c
                        node.setText(0, node_name.split("/")[-1])
                        file_name_item_dict[node_name] = node
                        try:
                            # 这里面的每个显示都是直接从xvi信息中获取，然后设置
                            # 这里如果node能够获取到文件（没有KeyError），就开始加上文件信息，否则就是空的只作为parent
                            xvi_item = self.vsp.relative_path_XVI_dict["/" + node_name]
                            for i in range(len(self.xsd_file_contents)):
                                # 这里node按照content的顺序，把内容要么getattr拿到然后设置字符串，要么判断content的名称然后拿到内容设置
                                node.setText(i + 1, getattr(xvi_item, self.xsd_file_contents[i], "None"))
                                if self.xsd_file_contents[i] == "status":
                                    # 这些set使用index进行的，所以先判断是不是在相应的列，也可改成名称为key，value为index
                                    node.setBackground(i + 1, QBrush(STATUS_COLOR[xvi_item.status]))
                                if self.xsd_file_contents[i] == "type":
                                    try:
                                        node.setBackground(i + 1, QBrush(Type_Color[xvi_item.type]))
                                    except:  # 这个是应对之前没有这个attr的项目，之后可以删除此
                                        node.setBackground(i + 1, QBrush(Type_Color[Type.Origin]))
                                if self.xsd_file_contents[i] == "mark_text":
                                    node.setText(i + 1, getattr(xvi_item, self.xsd_file_contents[i], "None"))
                                    try:
                                        node.setBackground(i + 1, QBrush(QColor(xvi_item.mark_color)))

                                    except:
                                        traceback.print_exc()
                                        node.setBackground(i + 1, QBrush(QColor(255, 255, 255)))

                            node.file_path = "/" + node_name  # 这里强行给这个实例增加了属性，之后直接调用，这里相当于继承
                            self.xsd_files_item.append(node)
                        except KeyError:
                            pass
                        except:
                            traceback.print_exc()
                    l.append(node)
                    # 采用类似队列的方法遍历，addChild
                    l[-2].addChild(l[-1])

            # 存储node信息，用于接下来进行node的扩展
            self.tree_node_widget_item_info = file_name_item_dict

            def load_column_status():
                '''
                载入save project中保存的标题栏宽度信息
                '''

                try:
                    info = self.vsp.xsd_tree_widget_param["column_status"]
                    for i in range(tw.columnCount()):
                        tw.setColumnWidth(i, info[i])
                except:
                    return

            def load_expand():
                '''
                载入save project中保存的文件树展开信息
                '''
                try:
                    # 使用"expanded_status"作为key去存储widget的信息
                    info = self.vsp.xsd_tree_widget_param["expanded_status"]
                    # 先展开所有，按照按照设置去unexpand
                    tw.expandAll()
                    for key in self.tree_node_widget_item_info.keys():
                        try:
                            self.tree_node_widget_item_info[key].setExpanded(info[key])
                        except:
                            continue
                except:
                    pass

            load_column_status()
            load_expand()
            return

        except:
            QMessageBox.information(self.main_window, "提示", "No xsd files.")
            traceback.print_exc()
            return

    def update_project_information(self):
        '''
        从model中更新信息到UI
        '''
        try:
            tw = self.main_window_ui.tableWidgetProjectInformation
            tw.setHorizontalHeaderLabels(["Property", "Value"])
            info_x = [
                "Local Project Path",
            ]
            info_y = [
                self.vsp.local_project_dir,
            ]
            tw.setRowCount(len(info_x))
            tw.setColumnCount(2)
            for i in range(len(info_x)):
                newItem = QTableWidgetItem(info_x[i])
                tw.setItem(i, 0, newItem)
                newItem = QTableWidgetItem(info_y[i])
                tw.setItem(i, 1, newItem)
        except:
            QMessageBox.information(self.main_window, "提示",
                                    "No project information, please create New or Open one.")

    def check(self, window, checker):
        '''
        专门用于相应check函数的
        如果为False，需要有error msg
        如果单为True，pass
        如果为True且有附加信息，返回它们
        '''
        assert isinstance(checker, Checker)
        if checker.window_status == Status.INFO:
            QMessageBox.information(window, "Information", checker.window_string)
        elif checker.window_status == Status.WARN:
            QMessageBox.warning(window, "Warning", checker.window_string)
        elif checker.window_status == Status.ERROR:
            QMessageBox.critical(window, "Error", checker.window_string)
        if checker.status == Status.FAILED:
            return Status.FAILED
        elif checker.status == Status.PASS:
            return checker.output_

    def file_dialog_local_project_path(self):
        self.local_project_path = QFileDialog.getExistingDirectory()
        self.create_project_ui.localProjectPathEdit.setText(self.local_project_path)

    # ————————从下面开始都是submit操作，具体思路:以xvi item传参，修改xvi item的参数，然后更新UI————————
    # ————————建议所有submit操作都开另一个线程进行

    def submit_grep_command(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
                xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)[0]
                a = getattr(xvis, "local_vasp_dir", "")
                if a == "" or a == None: return
                a += "/OUTCAR"
                a = a.replace("/", "\\", 99)
                command = str(QInputDialog.getText(self.main_window, "输入grep内容", "grep")[0])

                if command == "": return
                try:
                    command_ = "findstr %s %s" % (command, a)
                    return_ = os.popen(command_).read()
                    self.main_window_ui.commandOutput.setText(str(return_))
                    return
                except:
                    traceback.print_exc()

    def run_task_cancel_command(self):
        # TODO: 完成cancel需要重新多线程，建议将多线程写为一个类
        pass
        # if self.xsd_files_item == []: return
        # self.selected_items = []
        # for i in self.xsd_files_item:
        #     if i.isSelected():
        #         self.selected_items.append(str(i.file_path))
        # xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        # try:
        #     command = []
        #     for i in xvis:
        #         if i.status != XVI_Status.Submitted:
        #             QMessageBox.information(self.main_window,"提示","包含没有运行的任务，请重新提交")
        #             return
        #         if i.nodel is not None and len(i.nodel) > 0:
        #             command.append("qdel %s" % i.nodel)
        #     self.run_command(command)
        #     for i in xvis:
        #         i.status = XVI_Status.Canceled
        #         i.nodel = ""
        #     self.update_xsd_files_information()
        # except:
        #     traceback.print_exc()

    def run_qstat_command(self):
        self.run_command(["qstat -a"])

    def run_command(self, command_list):
        try:
            if len(self.vsp.job_submit_items) == 0:
                QMessageBox.information(self.main_window,
                                        "提示",
                                        "没有可用的Job Submit配置")
                return

            def ok():
                # 这里OK函数是后面创建了submit对话框过后调用
                job_submit = ui.chooseJobSubmit.currentText()
                if job_submit == "":
                    QMessageBox.information(a, "提示", "选择一个Job Submit配置")
                    return
                else:
                    job_submit = self.vsp.job_submit_items[job_submit]
                    a.close()

                    def command_run(*args):

                        sf = SFTP_SSH_Utils(
                            host=job_submit.host,
                            port=job_submit.port,
                            username=job_submit.username,
                            password=job_submit.password
                        )
                        a, b, c = sf.ssh_run_command(args)
                        return a, b, c, 1

                    class SJT(QThread):
                        def __init__(self, job_submit_confg, *args):
                            super().__init__()
                            self.status = None
                            self.jc = job_submit_confg
                            self.args = args

                        def run(self):
                            self.output = command_run(self.args[0])
                            self.status = self.output[3]
                            self.output = self.output[:3]

                        def get_output(self):
                            return self.output

                    try:
                        thread = SJT(job_submit, command_list)
                        thread.start()
                        while True:
                            # 一直获取thread对象的参数，注意如果一直都是None的话，那么线程会一直卡在这里，
                            #  但是status是从run command那里过来，因此一定会改变status
                            q = thread.status
                            if q == None:
                                # 没有获取到就一直更新等待UI
                                QCoreApplication.processEvents()
                                continue
                            # 成功获取
                            elif q == 1:
                                try:
                                    string = ""
                                    for i in thread.output[1]:
                                        string += str(i, encoding="utf-8") + "\n"
                                    # 更新信息
                                    self.main_window_ui.commandOutput.setText(string)
                                    self.command_output = string
                                    return

                                except:
                                    traceback.print_exc()
                                    QMessageBox.information(self.main_window, '提示', "command运行失败")
                                    return
                            else:
                                QMessageBox.information(self.main_window, '提示', "command运行失败")
                                return
                    except:
                        traceback.print_exc()

            # 增加job submit的对话框，绑定前面的OK函数
            a = QDialog()
            ui = Ui_submitJob()
            ui.setupUi(a)
            for i in self.vsp.job_submit_items:
                # 增加下拉框的item
                ui.chooseJobSubmit.addItem(i)
            a.show()
            ui.submitJobOK.clicked.connect(ok)

        except:
            traceback.print_exc()

    def submit_freq_extract(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        freq = QInputDialog(self.main_window)
        freq = freq.getText(self.main_window, "输入虚频允许的数目", "虚频数目")[0]
        VASPFreqExtract.freq_extract(xvis, int(freq))
        self.update_xsd_files_information()

    def submit_view_molecule(self):
        if ADD_MOLECULE_SHOW == False:
            return

        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                # 只显示选中的第一个的结构
                self.selected_items.append(str(i.file_path))

                xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)[0]

                # TODO：尝试另一个线程更新
                # s = threading.Thread(target=thread_submit_plot)
                # s.start()
                # thread_submit_plot()
                try:
                    # s = threading.Thread(target=thread_submit_plot)
                    # s.start()

                    submit_plot(xvis, config_string=self.main_window_ui.moleculeViewSettingsText.toPlainText())
                except:
                    traceback.print_exc()
                return

    def submit_mark(self):
        '''
        拿出来xvi item，修改其中的attr，然后update
        '''
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        # Dialog返回的是一个元组
        col = QColorDialog.getColor(parent=self.main_window, title="选择一个mark颜色")

        text = QInputDialog.getText(self.main_window, "输入mark内容", "标注")[0]
        if text == "": return
        for i in xvis:
            i.mark_text = text
            i.mark_color = (col.rgb())
        self.update_xsd_files_information()

    def xsd_file_delete(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)

        reply = QMessageBox.information(self.main_window,
                                        "提示",
                                        "将删除(移动到项目文件下trash文件夹)以下文件，请确认\n" + "\n".join(self.selected_items),
                                        QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No: return
        for i in xvis:
            try:
                if not os.path.exists(self.vsp.local_project_dir + "/" + "trash"):
                    os.mkdir(self.vsp.local_project_dir + "/" + "trash")
                shutil.move(i.local_xsd_path,
                            self.vsp.local_project_dir + "/" + "trash" + "/" + i.local_xsd_path.split("/")[-1])
            except:
                traceback.print_exc()
        self.check_file_change_and_update_file()
        self.update_xsd_files_information()

    def change_to_not_submit(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)

        for i in xvis:
            assert isinstance(i, XSD_VASP_item)
            i.status = XVI_Status.NotSubmitted
            i.type = Type.Origin
            i.energy = ""
            i.final_RMS = ""
            i.nodel = ""
            i.local_vasp_dir = ""
        self.update_xsd_files_information()

    def submit_outcar_export(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        directory = QFileDialog.getExistingDirectory(
            self.main_window,
            "Choose a dir to store OUTCAR"
        )
        fail = []
        for i in xvis:
            try:
                _from = i.local_vasp_dir + "/OUTCAR"
                _to = directory + "/" + i.item_key.split("\\")[-1].split("/")[-1] + "_OUTCAR"
                print("Copy from %s to %s" % (_from, _to))
                shutil.copyfile(_from, _to)
            except:
                traceback.print_exc()
                fail.append(i.item_key)
        if len(fail) > 0:
            string = "Failed to export following OUTCAR: \n"
            string += "\n".join(fail)
            self.main_window_info(string)

    def submit_export_freq_to_dict(self):
        # 这个是专用于catmap对接的，之后根据catmap对接情况修改
        string = "frequency_dict={"
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        for xvi in xvis:
            string += '"' + str(xvi.relative_xsd_file_name) + '"' + ":" + "["
            for i in xvi.real_freq:
                string += str(i) + ","
            string += "]"
            string += ",\n"
        string += "}"

        path = QFileDialog.getSaveFileName(
            self.main_window,
            "Export",
            "C:/",
            "*.txt"
        )[0]

        with open(path, "w") as f:
            f.write(string)

    def submit_information_export(self):
        string = ""
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        path = QFileDialog.getSaveFileName(
            self.main_window,
            "Export to csv file",
            "C:/",
            "*.csv"
        )[0]

        # 导出的信息
        attr_list = ["relative_xsd_file_name", "energy", "final_RMS", "real_freq", "virtual_freq"]
        string = ",".join(attr_list) + "\n"
        for xvi in xvis:

            for attr in attr_list:
                string += str(getattr(xvi, attr, "")).replace(",", " ", 999) + ","  # 避免数据的空格导致划分错误
            string += "\n"

        with open(path, "w") as f:
            f.write(string)

    def submit_structure_export(self):
        QMessageBox.information(self.main_window,
                                "提示",
                                "提取时间可能较长，程序可能未响应。匹配完成后请检查Match State，全部匹配才有效")  # TODO：使用多线程解决这个问题
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        VASPStuStructureManager().final_outani_structure_export(xvi_items=xvis)
        self.check_file_change_and_update_file()
        self.update_xsd_files_information()

    def submit_RMS_extract(self):
        thushold = QInputDialog(self.main_window)
        thushold = thushold.getText(self.main_window, "输入RMS收敛阈值", "RMS收敛阈值")[0]
        try:
            thushold = float(thushold)
        except:
            self.main_window_info("Invalid Input")
            return
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)

        VASP_RMS_Extract.final_RMS_extract(xvis, thushold)
        self.update_xsd_files_information()
        self.save_project()

    def submit_energy_collect(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        VASPEnergyExtract.energy_extract(xvis)
        self.update_xsd_files_information()
        self.save_project()

    def submit_file_link_by_path(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)

        directory = QFileDialog.getExistingDirectory(
            self.main_window,
            "选择一个与当前项目嵌套结构相同的顶端文件夹"
        )
        try:
            VASPStuFileLinker().link_file_and_vsp_dir_by_path(xvis, directory)
        except:
            traceback.print_exc()
        self.update_xsd_files_information()
        self.save_project()

    def submit_file_link_by_name(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)

        directory = QFileDialog.getExistingDirectory(
            self.main_window,
            "选择一个可能与当前所选xsd文件名相同的VASP文件夹"
        )
        try:
            VASPStuFileLinker().link_file_and_vsp_dir_by_name(xvis, directory)
        except:
            traceback.print_exc()
        self.update_xsd_files_information()
        self.save_project()

    def submit_job(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))

        self.tmp_xvis = xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        new_items = []

        for i in xvis:
            if i.status != XVI_Status.NotSubmitted:
                reply = QMessageBox.information(self.main_window,  # 使用information信息框
                                                "提示",
                                                "包含已经提交的项目，确定再次提交？",
                                                QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    new_items = self.selected_items
                    break
                else:
                    return
            elif i.status == XVI_Status.NotSubmitted:
                new_items.append(i.relative_xsd_file_name)

        self.selected_items = new_items

        reply = QMessageBox.information(self.main_window,
                                        "提示",
                                        "将提交以下项目，请确认\n" + "\n".join(self.selected_items),
                                        QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No: return

        if len(self.vsp.job_submit_items) == 0:
            QMessageBox.information(self.main_window,
                                    "提示",
                                    "没有可用的Job Submit配置")
            return

        def ok():
            job_submit = ui.chooseJobSubmit.currentText()
            if job_submit == "":
                QMessageBox.information(a, "提示", "选择一个Job Submit配置")
                return
            else:
                job_submit = self.vsp.job_submit_items[job_submit]
                self.tmp_note = \
                    QInputDialog(self.main_window).getText(self.main_window, "给这批任务添加一个备注", "任务备注")[0]

                self.submit_job_run(job_submit)
                a.close()

        a = QDialog()
        ui = Ui_submitJob()
        ui.setupUi(a)
        for i in self.vsp.job_submit_items:
            ui.chooseJobSubmit.addItem(i)
        a.show()
        ui.submitJobOK.clicked.connect(ok)

    def submit_job_run(self, job_submit_confg):
        # job submit confg 实际上就是Job Submit Item，里面自带投job的方法
        self.job_config = job_submit_confg

        # 多线程: 主线程是UI
        def multiThreadUIMain():
            # 这里采用了一个deepcopy的对象去做另一线程，该线程不涉及任何类的修改操作
            # 这样做很不值得，但是如果在另一线程中使用self.vs会因为线程锁定而无法被pickle存储，即使线程已经关闭
            jc = copy.deepcopy(self.job_config)

            class SJT(QThread):
                def __init__(self, job_submit_confg, *args):
                    super().__init__()
                    self.status = None
                    self.jc = job_submit_confg
                    self.args = args

                def run(self):
                    self.status = self.jc.submit_job(self.args)

            thread = SJT(jc, self.selected_items)
            thread.start()
            # QMessageBox.information(self.main_window, "提示", "任务提交中......")
            error_msg = "任务提交失败，请检查\n1:服务器路径设置是否正确\n2:各文件路径是否有效\n3:Key Library是否按照说明书要求设置"
            while True:
                # 这里会一直等待status，也就是submit job的返回参数修改
                q = thread.status
                if q == None:
                    QCoreApplication.processEvents()
                    continue
                elif q == 1:
                    try:
                        # 提交成功才更新节点信息
                        thread.quit()
                        thread.wait()
                        del thread
                        # ssh阻塞过后，于是当status=1时，一定会有submit job on server执行完毕了，然后获取json信息来更新
                        # 这里下载远端创建的文件，得到信息更新到ui和model
                        info = jc.update_XVI_nodel_info()
                        if info == False: QMessageBox.information(self.main_window, "提示",
                                                                  "节点信息获取失败")
                        self.vsp.update_xvi_item_info()
                        self.update_xsd_files_information()

                        QMessageBox.information(self.main_window, '提示', "任务已提交，若获取到任务节点信息即为提交成功")
                        return
                    except:
                        traceback.print_exc()
                        QMessageBox.critical(self.main_window, "错误", error_msg)
                        return
                elif q == 0:
                    QMessageBox.critical(self.main_window, "错误", error_msg)
                    return

        multiThreadUIMain()
        for i in self.tmp_xvis:
            i.note = self.tmp_note
        self.save_project()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = Main()
    a.main_window.show()
    sys.exit(app.exec_())
