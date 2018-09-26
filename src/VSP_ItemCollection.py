import os
import traceback
from public import *




class CStatus():
    Failed = "Failed123124"

from PyQt5.QtGui import QColor

class VSP_Item():
    def __init__(self,vsp,item_key):
        # item key 用来显示和索引item
        self.item_key = item_key
        self.vsp = vsp

    def offer_property_for_GUI(self):
        raise NotImplementedError



class XSD_VASP_item(VSP_Item):


    # 这个用于存储xsd 项目的状态，未投job，已投，运行中，运行完成等
    # 简称XVI

    def __init__(self,vsp,relative_xsd_file_name):
        super(XSD_VASP_item, self).__init__(vsp,relative_xsd_file_name)
        self.vsp = vsp
        self.submit_job = None

        self.local_vasp_dir = None
        self.energy = ""
        self.final_RMS = ""

        self.mark_color = QColor(255,255,255)

        self.type = Type.Origin


        #assert isinstance(vsp, VASPStuProject)
        self.vsp.xsd_items[self.item_key] = self
        self.relative_xsd_file_name = relative_xsd_file_name
        self.status = XVI_Status.NotSubmitted

        self.result_vasp_dir = None

        self.nodel = None

        self.note = ""

    @property
    def remote_run_path(self):
        return self.vsp.remote_project_dir + "/" + self.relative_xsd_file_name + "_" + self.submit_job.project_type

    def offer_property_for_GUI(self):
        return [self.relative_xsd_file_name,self.status,self.nodel]

    @property
    def local_xsd_path(self):
        return self.vsp.local_project_dir + "/" + self.relative_xsd_file_name



class KeyItem(VSP_Item):
    def __init__(self,vsp,name,key,value):
        super(KeyItem, self).__init__(vsp,name)
        self.vsp = vsp
        self.name = name
        self.key = key
        self.value = value
        self.vsp.key_items[self.item_key] = self


class TF_Condition_item(VSP_Item):
    def __init__(self,vsp,name,string):
        super(TF_Condition_item, self).__init__(vsp,name)
        self.vsp = vsp
        self.name = name
        self.vsp.tf_function_items[self.item_key] = self
        self.string = string
        self.TF_condition_func = TF_Condition_item.make_condition_func(string)
    @staticmethod
    def make_condition_func(string):
        TF_condition_func = string
        TF_condition_func = "def condition_func(x,y,z):return True if " + TF_condition_func
        TF_condition_func = TF_condition_func + " else False"
        return TF_condition_func
    @staticmethod
    def test_TF_condition_function(condition_func_,xyz=None):
        if xyz == None: xyz="0,0,0.2"
        try:
            x,y,z = xyz.split(",")
            x=float(x)
            y= float(y)
            z=float(z)

            exec(condition_func_, globals())

            a = condition_func(x, y, z)
            return a
        except:
            traceback.print_exc()
            return CStatus.Failed

    def offer_property_for_GUI(self):
        return self.TF_condition_func




class Text_File_item(VSP_Item):

    def __init__(self,vsp,name,string,file_name):
        super(Text_File_item, self).__init__(vsp,name)
        self.vsp = vsp
        self.name=name
        self.file_name = file_name
        self.vsp.text_file_items[self.item_key] = self
        self.string = string

    def offer_property_for_GUI(self):
        return self.string

class Script_item(VSP_Item):
    def __init__(self,vsp,name,content,additional_keys):
        super(Script_item, self).__init__(vsp,name)
        # TODO 将脚本转化为一个item
        pass


class File_item(VSP_Item):
    def __init__(self,vsp,name,path):
        super(File_item, self).__init__(vsp,name)
        self.name = name
        self.vsp = vsp
        self.vsp.file_items[self.item_key] = self
        self.path = path

    def offer_property_for_GUI(self):
        return self.path

