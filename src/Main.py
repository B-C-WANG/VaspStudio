# -*- coding: UTF-8 -*-

import os
#print(ETSConfig.toolkit)



#os.environ['QT_API'] = 'pyqt5'
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = "wx"
os.environ['ETS_TOOLKIT'] = 'wx'


# 在Runtime时会遇上这个问题：找不到wx的toolkit！
# 关于这个测试查看 "关于Build.md"
#from pyface import base_toolkit
#base_toolkit.import_toolkit("wx")
#exit()



import sys
sys.setrecursionlimit(50000)
from VASPStuEnergyManager import *

from PySide2.QtCore import QCoreApplication,QThread
from PySide2.QtWidgets import QTableWidgetItem,QTreeWidgetItem,QInputDialog,QComboBox,QDialog,QColorDialog,QMenu
from PySide2.QtGui import QBrush,QColor,QCursor,QIcon
from SFTP_SSH_Utils import *
from utils import *
from VASPStuProject import *
import sys
#import traceback
from ItemWindow import *
#from VASPStu3DPlot import *

#import json
from VASPStuStructureManager import *
from VASPStuFileLinker import *
from VASPStuMoleculeViewSubmit import *
#import threading

from Ui_about import *
from Ui_CreateProject import *
from Ui_VMainWindow import *
#from Ui_JobSumit import Ui_CreateProject as Ui_JobSubmit
from Ui_SubmitJob import *
from projectTypeAndChecker import *
import traceback





'''
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

# 默认的分子绘图设置
default_molecule_view_setting_text= \
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


# TODO：增加频率字典形式导出

# TODO 添加右键菜单，转移所有功能到右键菜单中，增加打开VASP目录功能
# TODO 优化多线程，增加远端执行linux命令的功能
# TODO：用openGl等库展示优化过程
# TODO: 增加自动下载功能
# TODO：和wxDragon联动展示频率震动，或者自行使用openGL等
# TODO: 目前nodel状态自动更新功能需要手动确定一个配置然后连接更新，之后尝试自动根据每个任务的配置来连接和更新
# TODO： 虚频的英文单词有误，不能为virtual_freq


class Main():
    def __init__(self,debug_mode=False):




        self.debug_mode = debug_mode

        self.xsd_files_item = []

        self.main_window = QtWidgets.QMainWindow()
        self.main_window_ui = Ui_VASPStudio()
        self.main_window_ui.setupUi(self.main_window)

        self.create_project = QtWidgets.QDialog()
        self.create_project_ui = Ui_CreateProject()
        self.create_project_ui.setupUi(self.create_project)

        self.about_window = QtWidgets.QDialog()
        self.about_window_ui = Ui_about()
        self.about_window_ui.setupUi(self.about_window)

        #self.main_window.setWindowFlags()
        self.main_window.setFixedSize(self.main_window.width(), self.main_window.height())


        self.last_save_path = None
        self.vsp = None

        self.command_output = "" # 控制台输出，等同于GUI界面的控制台输出结果，用于分析


        self.binding_main_window()
        self.binding_create_project_window()



        # 注意header要多一行
        self.xsd_file_headers = ["File","Status","Type","Mark","Energy","Final RMS", "Work Node","Job","Match State","备注"]
        self.xsd_file_contents = ["status","type","mark_text","energy","final_RMS","nodel","submit_job","match_state","note"]



    def main_window_error(self,string):
        QMessageBox.critical(self.main_window,"Error",string)
    def main_window_info(self,string):
        QMessageBox.information(self.main_window,"Information",string)
    def main_window_warn(self,string):
        QMessageBox.warning(self.main_window,"Warning",string)




    def generate_item_window(self):
        # item的设定,item自动与vsp同步

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
        # 不只是更新，还要检测新文件
        self.check_file_change_and_update_file()
        self.update_xsd_files_information()


    def binding_main_window(self):
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
        #self.main_window_ui.xsdFileTreeWidget.doubleClicked.connect(self.open_xsd_file)
        #self.main_window_ui.xsdFileTreeWidget.doubleClicked.connect(self.show_3d_coordinate)
        # self.main_window_ui.xsdFileExportFinalStructure.clicked.connect(self.submit_structure_export)
        # self.main_window_ui.xsdFileMark.clicked.connect(self.submit_mark)
        # self.main_window_ui.xsdFileButtonChangeToNotSubmit.clicked.connect(self.change_to_not_submit)
        # self.main_window_ui.runQstatButton.clicked.connect(self.run_qstat_command)
        # 选中的item显示所有信息

        self.main_window_ui.xsdFileRunQstat.clicked.connect(self.run_qstat_command)
        self.main_window_ui.xsdFileTreeWidget.itemSelectionChanged.connect(self.update_item_information)
        self.add_right_memu_to_xsdFileTreeWidget()


    def show_xsdFile_right_menu(self):
        self.xsdFileRightMenu.exec_(QCursor.pos())

    def add_right_memu_to_xsdFileTreeWidget(self):
        self.xsdFileRightMenu = QMenu(self.main_window_ui.xsdFileTreeWidget)
        self.a_view_action = self.xsdFileRightMenu.addAction("View Molecule")
        self.a_view_action.triggered.connect(self.submit_view_molecule)
        self.xsdFileRightMenu.addSeparator()
        # mark
        self.a_mark_action = self.xsdFileRightMenu.addAction("Mark")
        self.a_mark_action.triggered.connect(self.submit_mark)
        self.xsdFileRightMenu.addSeparator()
        # submit job
        self.a_submit_job = self.xsdFileRightMenu.addAction("Submit Job")
        self.a_submit_job.triggered.connect(self.submit_job)
        self.xsdFileRightMenu.addSeparator()
        # status control
        self.m_status_control = self.xsdFileRightMenu.addMenu("Status")
        self.a_turn_not_submit = self.m_status_control.addAction("Turn Not Submit")
        self.a_turn_not_submit.triggered.connect(self.change_to_not_submit)
        # task control
        # TODO:增加stop 命令
        pass

        # download TODO：
        pass
        # local link
        self.m_local_link = self.xsdFileRightMenu.addMenu("Local Link")
        self.a_by_path = self.m_local_link.addAction("By Path")
        self.a_by_name = self.m_local_link.addAction("By Name")
        self.a_by_name.triggered.connect(self.submit_file_link_by_name)
        self.a_by_path.triggered.connect(self.submit_file_link_by_path)
        # information
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
        # structure
        self.m_structure = self.xsdFileRightMenu.addMenu("Structure")
        self.a_structure_export = self.m_structure.addAction("Export Final Structure")
        self.a_structure_export.triggered.connect(self.submit_structure_export)

        # file control
        self.m_file_control = self.xsdFileRightMenu.addMenu("File")
        self.a_outcar_export = self.m_file_control.addAction("Export OUTCAR in dir")
        self.a_outcar_export.triggered.connect(self.submit_outcar_export)
        self.a_delete_file = self.m_file_control.addAction("Delete")
        self.a_delete_file.triggered.connect(self.xsd_file_delete)

        self.main_window_ui.xsdFileTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.main_window_ui.xsdFileTreeWidget.customContextMenuRequested.connect(self.show_xsdFile_right_menu)

        self.main_window_ui.xsdFileTreeWidget.doubleClicked.connect(self.submit_view_molecule)







    def open_xsd_file(self):
        for i in self.xsd_files_item:
            if i.isSelected():
                print(i.file_path)
                try:
                    os.startfile(self.vsp.local_project_dir + "/"+i.file_path)
                except:
                    traceback.print_exc()
                break










    def binding_create_project_window(self):

        # 将文件对话框函数绑定并获得相应值到类成员变量中
        #self.create_project_ui.localBaseFilePathButton.\
        #    clicked.connect(self.file_dialog_local_base_file)

        self.create_project_ui.localProjectPathButton.clicked.connect(
            self.file_dialog_local_project_path)

        # 直接将ok按钮绑定创建project，如果不合理会弹出警告，合理会创建然后close
        self.create_project_ui.projectOkButton.clicked.connect(self.create_vs_project)
        pass

    def load_vs_project(self):

        vsp_file = self.file_dialog_vsp_file()[0]
        if len(vsp_file) == 0:return
        # 先尝试默认密码123
        vs = self.check(self.main_window, VASPStuProject.read_existing_project(vsp_file, "123"))
        if vs == Status.FAILED :
            key = \
            QInputDialog(self.main_window).getText(self.main_window, "Please insert the project key", "Project Key")[0]
            vs = self.check(self.main_window, VASPStuProject.read_existing_project(vsp_file,key))
            self.vsp = vs

        elif isinstance(vs, VASPStuProject):
            self.vsp = vs
            #QMessageBox.information(self.main_window, "Information", "Success.")
        self.after_open_or_load()

    def create_vs_project(self):
        try:


            self.local_project_path = self.create_project_ui.localProjectPathEdit.text()
        except :
            QMessageBox.critical(self.create_project,"Error","Not complete")
            # return是必要的，否则会直接执行下一个语句，报错会直接关掉程序
            return

        self.vsp = VASPStuProject(local_project_dir=self.local_project_path,
                                 project_key="123")

        with open(self.vsp.local_project_dir+"/"+"temp", "w") as f:
            f.write("")

        # 是否覆盖已有文件，如果是就写入，否则不关闭窗口
        if self.save_project() == False: return



        # 进行检查，否则要求重新输入
        #if self.project_check() == False: return

        self.create_project.close()



        self.after_open_or_load()
        #QMessageBox.information(self.main_window,"提示","项目建立完成，请重新打开并载入\ndue to thread lock error of deepcopy(vs_dc)")
        #app.quit()
    def after_open_or_load(self):
        # 旧版本vsp文件更新
        self.vsp.update_old_version()
        self.update_molecule_view_plot_settings()
        self.check_file_change_and_update_file()
        self.update_project_information()
        self.update_xsd_files_information()
        self.generate_item_window()

    def update_molecule_view_plot_settings(self):
        try:
            self.main_window_ui.moleculeViewSettingsText.setPlainText(self.vsp.molecule_view_setting_text)
        except:
            self.main_window_ui.moleculeViewSettingsText.setPlainText(default_molecule_view_setting_text)
            traceback.print_exc()



    def save_project(self):

        if self.vsp == None:return

        if  self.vsp.class_data_save_path == None:
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
        # 存储是否expanded,注意需要使用node去获取信息
        # 新创建的文件会有问题，尝试这一个
        try:
            for key in self.tree_node_widget_item_info:
                expand_state_dict[key] = self.tree_node_widget_item_info[key].isExpanded()
        except:pass
        self.vsp.xsd_tree_widget_param["expanded_status"] = expand_state_dict
        self.vsp.xsd_tree_widget_param["column_status"] = n
        self.vsp.molecule_view_setting_text = self.main_window_ui.moleculeViewSettingsText.toPlainText()
        # 如果保存了一次，变为new save，因为新保存的密码固定了
        self.vsp.new_save = True
        self.vsp.save_project_info(path)
        QMessageBox.information(self.main_window,"提示","已保存")
        return True



    def check_file_change_and_update_file(self):
        new_files, deleted_files = self.vsp.check_and_add_new_xsd_files_and_generate_XVI()
        if new_files == False:# 这个是由底层传来的，不只是文件，还有status以及错误信息
            # 这里newFiles是错误时传来的status，deletedFiles是信息
            QMessageBox.critical(self.main_window,"Error",deleted_files)
            return

        # 之所以需要self.vs.new_files，是因为希望在一开始创建项目时就保存项目
        if len(new_files) == 0 and len(deleted_files) == 0 :return
        string = ""
        if len(new_files) >= 1:
            string += "检测到新增%s个以下文件:"%len(new_files)
            string += "\n".join(new_files)
        if len(deleted_files) >= 1:
            string += "检测到删除%s个以下文件"%len(deleted_files)
            string += "\n".join(deleted_files)
        QMessageBox.information(self.create_project,
                                "File changes",
                                string)

    def project_check(self):
        if self.check(self.create_project,self.vsp.submit_job_file_check) == False:return False
        if self.check(self.create_project,self.vsp.base_file_check) == False:  return False
        if self.check(self.create_project,self.vsp.connect_remote_project_dir_check)== False:return False
        QMessageBox.information(self.create_project,"Information","Success. 为确保顺利运行，请检查：\n服务器端是否有新创建的checkFile文件")


    def update_item_information(self):
        # 选中后增加具体的信息
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                xvis = self.vsp.get_XVI_from_relative_xsd_files([str(i.file_path)])[0]
                content = ""
                for key in xvis.__dict__:
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

                        content += "<b><font size=4 >%s</font><br></b>"%key
                        content += "<font size=4>%s</font><br>" % getattr(xvis,key,"")

                        self.main_window_ui.xsdFileInformation.setText(content)





    def update_xsd_files_information(self):
        '''
        update 函数直接与vs类关联，得到所有的文件类，这样只用update就能更新最新
        :return:
        '''

        if self.vsp == None:
            QMessageBox.information(self.main_window,"提示","没有加载项目，无法获得xsd文件")
            return
        self.xsd_files_item = []


        try:
            filenames = list(self.vsp.relative_path_XVI_dict.keys())
            filenames = sorted(filenames)
            tw = self.main_window_ui.xsdFileTreeWidget

            index = 0
            tw.clear()
            # TODO :这里让用户自选显示的顺序和内容
            tw.setHeaderLabels(self.xsd_file_headers)
            tw.setColumnCount(len(self.xsd_file_headers))
            file_name_item_dict = {}
            root = QTreeWidgetItem(tw)
            root.setText(0,self.vsp.local_project_dir)

            for file in filenames:


                l = [root]
                trees = file.split("/")[1:]# 第一个元素是“”，是root

                # 按照文件目录树进行，如果能够获取到子集就开始增加内容，否则增加child
                for i in range(len(trees)+1):# 对于剩下的child
                    node_name = "/".join(trees[:i])
                    try:# 尝试找到这个node，如果没有就创建
                        node = file_name_item_dict[node_name]

                    except:
                        # 创建child node，加入到字典中
                        node = QTreeWidgetItem(l[-1])
                        index += 1
                        node.setText(0, node_name.split("/")[-1])
                        file_name_item_dict[node_name] = node
                        try:
                            # 这里面的每个显示都是直接从xvi信息中获取，然后设置
                            # 这里如果node能够获取到文件，就开始加上文件信息，否则就是空的只作为有内容的node的parent
                            xvi_item = self.vsp.relative_path_XVI_dict["/"+node_name]
                            for i in range(len(self.xsd_file_contents)):
                                #if getattr(xvi_item,"type","") == "":xvi_item.type = Type.Origin
                                node.setText(i+1,getattr(xvi_item,self.xsd_file_contents[i],"None"))
                                if self.xsd_file_contents[i] == "status":
                                    # 这些set使用index进行的，所以先判断是不是在相应的列，也可改成名称为key，value为index
                                    node.setBackground(i+1,QBrush(STATUS_COLOR[xvi_item.status]))
                                if self.xsd_file_contents[i] == "type":
                                    try:
                                        node.setBackground(i+1,QBrush(Type_Color[xvi_item.type]))
                                    except:# 这个是应对之前没有这个attr的项目，之后可以删除此
                                        node.setBackground(i+1, QBrush(Type_Color[Type.Origin]))
                                if self.xsd_file_contents[i] == "mark_text":
                                        node.setText(i + 1, getattr(xvi_item, self.xsd_file_contents[i], "None"))
                                        try:
                                            node.setBackground(i+1,QBrush(QColor(xvi_item.mark_color)))

                                        except:
                                            traceback.print_exc()
                                            node.setBackground(i + 1, QBrush(QColor(255,255,255)))

                            node.file_path = "/"+node_name # 这里强行给这个实例增加了属性，之后直接调用，这里相当于继承
                            self.xsd_files_item.append(node)
                        except KeyError:
                            pass
                        except:
                            traceback.print_exc()
                    l.append(node)

                    l[-2].addChild(l[-1])

            def load_column_status():
                # 这里设置列的长度，首先用一个变量去存储这些列，存储在save project中
                try:
                    info = self.vsp.xsd_tree_widget_param["column_status"]
                    for i in range(tw.columnCount()):
                        tw.setColumnWidth(i,info[i])
                except:
                    return
            load_column_status()
            # 把node的信息存储一下！用于接下来搞node的扩展
            self.tree_node_widget_item_info = file_name_item_dict
            # 这里我们用一个与tree node widget 。。key一模一样的字典去存储node的expand信息，之后
            # 用这个key去获取node以及node的expand信息然后修改！
            def expand():# 存储各个列的expand情况
                try:
                    info = self.vsp.xsd_tree_widget_param["expanded_status"]
                    tw.expandAll()
                    for key in self.tree_node_widget_item_info.keys():
                        try:
                            self.tree_node_widget_item_info[key].setExpanded(info[key])
                        except:
                            continue
                except:
                    pass
            expand()
            print(tw.rootIndex())
            return

        except:
            QMessageBox.information(self.main_window,"提示","No xsd files.")
            traceback.print_exc()
            return

    def update_project_information(self):

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
                tw.setItem(i,0,newItem)
                newItem = QTableWidgetItem(info_y[i])
                tw.setItem(i,1,newItem)
        except:
            QMessageBox.information(self.main_window,"提示",
                       "No project information, please create New or Open one.")

    def check(self,window,checker):
        # 专门用于相应check函数的
        # 如果为False，需要有error msg
        # 如果单为True，pass
        # 如果为True且有附加信息，返回它们
        assert  isinstance(checker,Checker)
        if checker.window_status == Status.INFO:
            QMessageBox.information(window,"Information",checker.window_string)
        elif checker.window_status == Status.WARN:
            QMessageBox.warning(window,"Warning",checker.window_string)
        elif checker.window_status == Status.ERROR:
            QMessageBox.critical(window,"Error",checker.window_string)
        if checker.status == Status.FAILED:
            return Status.FAILED
        elif checker.status == Status.PASS:
            return checker.output_

    def file_dialog_vsp_file(self):
        return QFileDialog.getOpenFileName(
            self.main_window,
            "Open .vsp file",
            "C:/",
            "VASP Studio Project File (*.vsp)"
        )


    def file_dialog_local_project_path(self):
        self.local_project_path = QFileDialog.getExistingDirectory()
        self.create_project_ui.localProjectPathEdit.setText(self.local_project_path)

    # TODO ：下面是根据选定的item进行提交job的操作，代码有很大冗余，可以精简
    #  思路：按钮联系，提供文件，然后更新VASP Item的属性

    def submit_update(self):
        raise NotImplementedError
        self.run_command(["qstat -a"])
        if self.command_output is None or len(self.command_output) ==0:
            return

    def submit_grep_command(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
                xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)[0]
                a = getattr(xvis,"local_vasp_dir","")
                if a == "" or a==None:return
                a += "/OUTCAR"
                a = a.replace("/","\\",99)
                command =  str(QInputDialog.getText(self.main_window,"输入grep内容","grep")[0])

                if command == "": return
                try:
                    command_ = "findstr %s %s"%(command,a)
                    print(command_)
                    return_ = os.popen(command_).read()
                    print(return_)
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

    def run_command(self,command_list):
        try:
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
                    a.close()
                    def command_run(*args):

                        sf = SFTP_SSH_Utils(
                            host=job_submit.host,
                            port=job_submit.port,
                            username=job_submit.username,
                            password=job_submit.password
                        )
                        a,b,c = sf.ssh_run_command(args)
                        print(a)
                        print(b)
                        print(c)
                        return a,b,c,1
                    class SJT(QThread):
                        def __init__(self, job_submit_confg, *args):
                            super().__init__()
                            self.status = None
                            self.jc = job_submit_confg
                            self.args = args

                        def run(self):
                            print(self.args)
                            self.output = command_run(self.args[0])
                            self.status = self.output[3]
                            self.output = self.output[:3]
                        def get_output(self):
                            return self.output

                    try:
                        thread = SJT(job_submit, command_list)
                        thread.start()

                        while True:

                            q = thread.status
                            if q == None:
                                QCoreApplication.processEvents()
                                continue

                            elif q == 1:
                                try:
                                    string = ""
                                    for i in thread.output[1]:
                                        string += str(i,encoding="utf-8") + "\n"
                                    # 提交成功才更新节点信息
                                    self.main_window_ui.commandOutput.setText(string)
                                    self.command_output = string
                                    return

                                except:
                                    traceback.print_exc()

                                    QMessageBox.information(self.main_window, '提示', "command运行失败")
                                    return

                    except:
                        traceback.print_exc()

            a = QDialog()
            ui = Ui_submitJob()
            ui.setupUi(a)
            for i in self.vsp.job_submit_items:
                ui.chooseJobSubmit.addItem(i)
            a.show()
            ui.submitJobOK.clicked.connect(ok)

        except:
            traceback.print_exc()

    # TODO: 编写逻辑架构，对于所有选中item，设定allow status和allow type，设定之后进行的参数，设定是否多线程等等


    def submit_freq_extract(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        freq = QInputDialog(self.main_window)
        freq = freq.getText(self.main_window, "输入虚频允许的数目", "虚频数目")[0]
        VASPFreqExtract().freq_extract(xvis,int(freq))
        self.update_xsd_files_information()

    def submit_view_molecule(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                # 只显示选中的第一个的结构
                self.selected_items.append(str(i.file_path))

                xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)[0]

                # 不管多不多线程，现在的问题是，显示之后会退出
                #s = threading.Thread(target=thread_submit_plot)
                #s.start()
                #thread_submit_plot()
                try:
                    #s = threading.Thread(target=thread_submit_plot)
                    #s.start()

                    submit_plot(xvis,config_string=self.main_window_ui.moleculeViewSettingsText.toPlainText())
                except:
                    traceback.print_exc()
                return



    def submit_mark(self):
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        # TODO： 一定要记住，Dialog返回的是一个元组！！！
        col = QColorDialog.getColor(parent=self.main_window,title="选择一个mark颜色")

        text = QInputDialog.getText(self.main_window,"输入mark内容","标注")[0]
        if text == "":return
        print(123123)
        print(col.value())

        print(text)

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
                if not os.path.exists(self.vsp.local_project_dir+"/"+"trash"):
                    os.mkdir(self.vsp.local_project_dir+"/"+"trash")
                shutil.move(i.local_xsd_path,self.vsp.local_project_dir+"/"+"trash"+"/"+i.local_xsd_path.split("/")[-1])
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
                _from = i.local_vasp_dir+"/OUTCAR"
                _to = directory+"/"+i.item_key.split("\\")[-1].split("/")[-1]+"_OUTCAR"
                print("Copy from %s to %s" % (_from,_to))
                shutil.copyfile(_from,_to)
            except:
                traceback.print_exc()
                fail.append(i.item_key)
        if len(fail) > 0 :
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

        with open(path,"w") as f:
            f.write(string)

    # 不建议导出csv然后excel打开，因为软件本身定位就是取代这个功能
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
        attr_list = ["relative_xsd_file_name","energy","final_RMS","real_freq","virtual_freq"]
        string = ",".join(attr_list) + "\n"
        for xvi in xvis:

            for attr in attr_list:
                string += str(getattr(xvi,attr,"")).replace(","," ",999) + "," # 避免数据的空格导致划分错误
            string += "\n"

        with open(path,"w") as f:
            f.write(string)



    def submit_structure_export(self):
        # TODO： 没有收敛状态的，不允许导出
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
        thushold =  thushold.getText(self.main_window,"输入RMS收敛阈值","RMS收敛阈值")[0]
        try:
            thushold = float(thushold)
        except:
            self.main_window_info("Invalid Input")
            return
        #QMessageBox.information(self.main_window,"提示","提取时间可能较长，程序可能未响应。") # TODO：使用多线程解决这个问题，
        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)

        VASP_RMS_Extract().final_RMS_extract(xvis,thushold)
        self.update_xsd_files_information()
        self.save_project()

    def submit_energy_collect(self):

        #QMessageBox.information(self.main_window,"提示","提取时间可能较长，程序可能未响应。")

        if self.xsd_files_item == []: return
        self.selected_items = []
        for i in self.xsd_files_item:
            if i.isSelected():
                self.selected_items.append(str(i.file_path))
        xvis = self.vsp.get_XVI_from_relative_xsd_files(self.selected_items)
        VASPEnergyExtract().energy_extract(xvis)
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
            VASPStuFileLinker().link_file_and_vsp_dir_by_path(xvis,directory)
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
            VASPStuFileLinker().link_file_and_vsp_dir_by_name(xvis,directory)
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
            #QMessageBox.information(self.main_window, "提示", "任务提交中......")
            error_msg = "任务提交失败，请检查\n1:服务器路径设置是否正确\n2:各文件路径是否有效\n3:Key Library是否按照说明书要求设置"
            while True:
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
