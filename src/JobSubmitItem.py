

from VSP_ItemCollection import *
from VASPStuProject import *
from SFTP_SSH_Utils import *
from public import *
import copy
import os
import json
import shutil
import json


class JobSubmit_item(VSP_Item):
    def __init__(self,
                 name,
                 vsp,
                 item_keys,
                 project_type,
                 remote_project_dir,
                 host,
                 port,
                 username,
                 password,
    ):
        super(JobSubmit_item, self).__init__(vsp,name)

        self.name = name
        self.vsp = vsp
        self.local_project_dir = vsp.local_project_dir
        #assert isinstance(vsp,VASPStuProject)

        self.vsp.job_submit_items[self.item_key] = self

        self.remote_project_dir = remote_project_dir



        self.remote_base_file_dir = self.remote_project_dir + "/baseFile"

        self.item_keys = item_keys
        #self.local_submit_job_path = os.path.join(os.getcwd(), "submit_job_onserver.py")

        self.project_type = project_type
        self.remote_project_dir = remote_project_dir
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sftp_tool = SFTP_SSH_Utils(host=host, port=port, username=username, password=password)

        self.base_files = []
    @property
    def total_items(self):
        total_dict = {}
        key_items, text_file_items, file_items, TF_function_items = self.transform_items(self.item_keys)
        for i in [key_items, text_file_items, file_items, TF_function_items]:
            if len(i) > 0:
                for j in i:
                    total_dict[j.item_key]= j
        return total_dict


    def __str__(self):
        return self.item_key

    def transform_items(self,item_keys):
        keys = item_keys
        key_items = []
        text_file_items = []
        file_items = []
        TF_function_items = []

        total_dict = {}

        for i in [self.vsp.file_items,
                      self.vsp.text_file_items,
                      self.vsp.tf_function_items,
                      self.vsp.key_items]:

            total_dict.update(i)



        for i in keys:
            a = total_dict[i]
            if isinstance(a, KeyItem):
                key_items.append(a)
            if isinstance(a, Text_File_item):
                text_file_items.append(a)
            if isinstance(a, File_item):
                file_items.append(a)
            if isinstance(a, TF_Condition_item):
                TF_function_items.append(a)

        return key_items,text_file_items,file_items,TF_function_items


    def submit_job(self,XVI_items):
        # 这个函数只负责运行，不负责反馈，之后update...才会反馈，因为只有成功获取到节点信息，才能算作submit
        try:
            info_dict = None
            key_items, text_file_items, file_items, TF_function_items = self.transform_items(self.item_keys)
            self.XVI_items = XVI_items[0]
            # TODO 这里按照project type进行check
            self.submit_job_file_check()
            self.create_base_files(text_file_items,file_items)
            self.create_remote_project_data(TF_function_items,key_items)
            status = self.upload_all_info_to_remote().status
            if status == Status.PASS:
                #  注意：一旦进行到这一步，debug就可以直接在服务器上运行脚本进行了
                status = self.run_remote_script()
            else:
                status = 0

            return status
        except:
            traceback.print_exc()
            return 0

    def update_XVI_nodel_info(self):

        self.node_info = self.down_load_and_read_nodel_dir_file()
        print(self.node_info)
        if self.node_info == False:return False
        print("NI", len(self.node_info), self.node_info)
        info_dict_ = {}
        for i in self.node_info:
            print("split",i,self.remote_project_dir)
            rela = i.split(self.remote_project_dir)[-1]
            rela = rela.replace("//","/",99).split("_"+self.project_type)[0]

            info_dict_[rela] = {}
            info_dict_[rela]["nodel"] = str(self.node_info[i])
            info_dict_[rela]["status"] = str(XVI_Status.Submitted)
            info_dict_[rela]["submit_job"] = str(self.item_key)


        #self.vsp.save_project_info(path=os.getcwd())
        print("Done")
        # 为了解决线程锁无法获得信息的问题，直接采用json写出信息，然后再导入
        with open(self.vsp.local_project_dir+"/"+"temp", "w") as f:
            json.dump(info_dict_,f)

        return True

    def create_remote_project_data(self,tf_items,key_items):
        self.project_data_path = os.path.join(self.local_project_dir,"data.vsd")
        remote_data = {}
        remote_data["submit_job_function"] = "submitJob"
        remote_data["submit_job_files"] = self.XVI_items
        remote_data["remote_project_dir"] = self.remote_project_dir
        remote_data["remote_base_file_dir"] = self.remote_base_file_dir
        remote_data["project_type"] = self.project_type
        remote_data["TF_condition_func"] = tf_items[0].TF_condition_func
        remote_data["debug_mode"] = False
        for i in key_items:
            remote_data[i.key] = i.value

        data = json.dumps(remote_data)
        with open(self.project_data_path, "w") as f:
            print(data)
            f.write(data)
    def create_base_files(self,text_items,file_items):
        # 所有needed files 会上传到base file
        self.local_base_file_dir = self.vsp.local_basefile_dir
        # 清空目录
        try:
            shutil.rmtree(self.local_base_file_dir)
        except:
            pass
        try:
            os.mkdir(self.local_base_file_dir)
        except:
            traceback.print_exc()
            pass


        for i in text_items:
            with open(self.local_base_file_dir + "/" + i.file_name, "w") as f:
                self.base_files.append(self.local_base_file_dir + "/" + i.file_name)
                f.write(i.string)
        for i in file_items:
            shutil.copy(i.path,self.local_base_file_dir+"/"+os.path.basename(i.path))
            self.base_files.append(self.local_base_file_dir+"/"+os.path.basename(i.path))

    def run_remote_script(self):
        try:
            a,b,c = self.sftp_tool.ssh_run_command([


                "python  %s/submit_job_onserver.py"%self.remote_project_dir

            ])
            print(a)
            print(b)
            print(c)
            return 1
        except:
            traceback.print_exc()
            return 0


    def upload_all_info_to_remote(self):
        # 在提交前获取当前目录下submit 文件
        self.local_submit_job_path = os.path.join(os.getcwd(), "submit_job_onserver.py")

        try:
            self.sftp_tool.upload_all_file_to_one_remote_dir(files=self.local_submit_job_path,
                                                             remote_dir=self.remote_project_dir)
            self.sftp_tool.upload_all_files_to_same_remote_dir(relative_file_list=self.XVI_items,
                                                               local_dir=self.local_project_dir,
                                                               remote_dir=self.remote_project_dir)
            self.sftp_tool.upload_all_file_to_one_remote_dir(files=self.base_files,
                                                             remote_dir=self.remote_base_file_dir)
            self.sftp_tool.upload_all_file_to_one_remote_dir(files=self.project_data_path,
                                                             remote_dir=self.remote_project_dir)
            return Checker(status=Status.PASS)
        except:
            traceback.print_exc()
            return Checker(status=Status.FAILED)



    def connect_remote_project_dir_check(self):
        # TODO：检查远端文件的功能没有实现，尝试让用户自己去检查
        try:
            check_file_path = os.path.join(self.local_project_dir, "checkFile")
            with open(check_file_path, "w") as f:
                f.write("1")
            self.sftp_tool.upload_all_file_to_one_remote_dir(files=[check_file_path], remote_dir=self.remote_project_dir)
            return Checker(status=Status.PASS)
        except:
            traceback.print_exc()
            return Checker(status=Status.FAILED,window_status=Status.ERROR,window_string="Can not connect to server or invalid remote project dir.")


    def submit_job_file_check(self):
            path = os.path.join(os.getcwd(), "submit_job_onserver.py")
            if not os.path.exists(path):
                return Checker(status=Status.FAILED,window_status=Status.ERROR,window_string="No submit job script.")

            with open(path, "rb") as f:
                data = f.readlines()[0]
                print(data)
                if not data.startswith(b'"QTAVASP-SubmitJobOnServer"'):
                    return Checker(status=Status.FAILED, window_status=Status.ERROR,
                                   window_string="Not the right submit_job_onserver.py")
            return Checker(status=Status.PASS,output=Status.PASS)

    def down_load_and_read_nodel_dir_file(self):
        #
        try:
            self.sftp_tool.sftp_download(local_dir=self.local_project_dir,remote_dir=self.remote_project_dir,certain_file="IO")

            with open(os.path.join(self.local_project_dir,"IO"), "r") as f:
                return json.loads(f.read())
        except:
            return False
