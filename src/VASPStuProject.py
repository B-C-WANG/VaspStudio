# -*- coding: utf-8 -*-
try:
    from .utils import *
    from .submit_job_onserver import *
    from .SFTP_SSH_Utils import *
except:
    from utils import *
    from SFTP_SSH_Utils import *
import json
from pickleCrypto import *
from JobSubmitItem import *
from VSP_ItemCollection import *
import traceback
from public import *
from projectTypeAndChecker import *

VERSION = "0.2"


def trans_all_path(path_string):
    return path_string.replace("\\", "/", 99).replace("\\\\", "/", 99)


class VASPStuProject(object):
    @staticmethod
    def after_load(VASPStuProject):
        VASPStuProject.version = VERSION

    '''
    这个类是沟通pyqt5的主要类，用于总结VaspStudio项目，然后给出信息到pyqt5
    '''

    @staticmethod
    def read_existing_project(path, key):
        try:
            a = pickle_decrypt_from_file(path, key)
            VASPStuProject.after_load(a)
            return Checker(Status.PASS, output=a)
        except:
            traceback.print_exc()
            return Checker(Status.FAILED, None, Status.ERROR,
                           "Read .vsp file failed. Please check the file or your input key.")

    def __init__(self,
                 local_project_dir,  # 工程路径
                 project_key="",  # 项目加密信息
                 debug_mode=True
                 ):

        # TODO :这里把所有items用一个字典存储，最后根据类型分开
        self.xsd_items = {}
        self.file_items = {}
        self.text_file_items = {}
        self.job_submit_items = {}
        self.tf_function_items = {}
        self.key_items = {}
        self.version = VERSION
        self.class_data_save_path = None

        self.local_project_dir = trans_all_path(local_project_dir)
        self.project_key = project_key
        self.debug_mode = debug_mode

        self.xsd_tree_widget_param = {}

        # self.relative_xsd_files = get_all_xsd_files_in_dir(local_project_dir,relative=True,linux_format=True)

        self.class_data_save_path = None  # 如果为None，要求Main打开窗口存储一个项目文件，如果不为None，则直接调用保存，除非另存为

        self.project_data = {}
        self.relative_path_XVI_dict = {}

        self.submit_job_function = "submitJob"  # 提示远端应该执行怎样的任务，之后可能是能量提取什么的

        self.running_submit = []  # 正在进行的submit，用于调用同步文件信息

        self.xsd_header = []
        self.xsd_header_content = []

    def update_old_version(self):
        if hasattr(self, "xsd_tree_widget_param") == False:
            self.xsd_tree_widget_param = {}
        for i in self.relative_path_XVI_dict.values():
            if hasattr(i, "local_vasp_dir") == False:
                i.local_vasp_dir = None

        if hasattr(self, "xsd_header") == False:
            self.xsd_header = []
        if hasattr(self, "xsd_header_content") == False:
            self.xsd_header_content = []

    def check_if_same_key(self, new_key):
        key = []
        for i in [self.xsd_items,
                  self.text_file_items,
                  self.file_items,
                  self.job_submit_items,
                  self.tf_function_items,
                  self.key_items]:
            key.extend(list(i.keys()))
        if new_key in key:
            return True
        return False

    def get_item_from_key(self, key):
        for i in [self.xsd_items,
                  self.text_file_items,
                  self.file_items,
                  self.job_submit_items,
                  self.tf_function_items,
                  self.key_items]:
            try:
                return i[key]
            except:
                continue

    def get_all_xsd_item(self):
        # 注意这里不用append，创建后自动会加上
        pass

    # 由于线程锁定，所以只能用return的方式来得到相应的信息
    def update_xvi_item_info(self, ):
        '''

        example:
        dict{
        "1.xsd":{"nodel":123}
        }


        :param dict_:
        :return:

        '''
        with open(self.local_project_dir + "/" + "temp", "r") as f:
            dict_ = json.load(f)
        for name in dict_:
            for key in dict_[name]:
                # 给对应的每个XVi加上attr
                setattr(self.relative_path_XVI_dict[name], key, dict_[name][key])

    @property
    def local_basefile_dir(self):
        return self.local_project_dir + "/" + "base_file"

    def check_and_add_new_xsd_files_and_generate_XVI(self):
        '''
        检测新文件同时以文件名作为key，xvi item作为value创建
        如果删除文件就删去相应的xvi item
        '''
        xsd_files = get_all_xsd_files_in_dir(self.local_project_dir, relative=True, linux_format=True)
        if xsd_files == []: return False, "没有找到xsd文件"
        if xsd_files[0] == False:
            return xsd_files
        new_files = []
        deleted_files = []
        if len(self.relative_path_XVI_dict) >= 1:
            new_files = list(set(xsd_files) - set(self.relative_path_XVI_dict.keys()))
            deleted_files = list(set(self.relative_path_XVI_dict.keys()) - set(xsd_files))
        else:
            new_files = list(set(xsd_files))

        if len(new_files) >= 1:
            for i in new_files:
                self.relative_path_XVI_dict[i] = XSD_VASP_item(self, i)
                name = i.split(".xsd")[0]

                # TODO: 这里和之后另存为的结构一致
                if name.endswith("%s" % XVI_Status.NotConvergence):
                    self.relative_path_XVI_dict[i].type = Type.NotConvergence
                elif name.endswith("%s" % XVI_Status.Convergence):
                    self.relative_path_XVI_dict[i].type = Type.Convergence
                else:
                    self.relative_path_XVI_dict[i].type = Type.Origin
        if len(deleted_files) >= 1:
            for i in deleted_files:
                del self.relative_path_XVI_dict[i]
        return new_files, deleted_files

    def save_project_info(self, path):

        # 用字符串dumps的pickle对象
        # 固定加密密码

        pickle_encrypt_to_file(path, "123", self)
        # 如果保存过一次，那么加密密码就是123了，老版本就可以不用再次输入了

        self.class_data_save_path = path

    def get_XVI_from_relative_xsd_files(self, relative_xsd_files):
        xvis = []
        for i in relative_xsd_files:
            xvis.append(self.relative_path_XVI_dict[i])
        return xvis
