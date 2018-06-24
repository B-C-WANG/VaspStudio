# -*- coding: utf-8 -*-


import paramiko
import os
import traceback
import time





class SFTP_SSH_Utils:


    def __init__(self,
                 host="",
                 port=22,
                 username="",
                 password=""):
        self.host = host  # 主机
        self.port = int(port)  # 端口
        self.username = username  # 用户名
        self.password = password  # 密码

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.sf.close()
        except:pass


    def ssh_run_command(self,command_list,time_sleep_between=0.1):
        print("command_list",command_list)
        if type(command_list) == tuple:command_list = command_list[0]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port,self.username, self.password)
        total_stdin = []
        total_stdout = []
        total_stderr = []
        for i in command_list:
            stdin, stdout, stderr = ssh.exec_command(i)
            try:
                stdin = stdin.read()
            except:
                stdin = None
            try:
                stdout = stdout.read()
            except:
                stdout = None
            try:
                stderr = stderr.read()
            except:
                stderr = None
            total_stderr.append(stderr)
            total_stdin.append(stdin)
            total_stdout.append(stdout)
            time.sleep(time_sleep_between)

        return total_stdin, total_stdout, total_stderr

    def upload_all_file_to_one_remote_dir(self,files,remote_dir):
        if not isinstance(files,list):
            files = [files]

        self.sf = paramiko.Transport((self.host, int(self.port)))
        self.sf.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(self.sf)
        try:
            sftp.mkdir(remote_dir)
        except:
            pass
        for file in files:
            file = file.replace("\\","/",99).replace("\\\\","/",99)
            print("remote",file,(remote_dir+"/"+file.split("/")[-1]))
            print("Sftp:",sftp.put(file, (remote_dir+"/"+file.split("/")[-1])))


    def upload_all_files_to_same_remote_dir(self,relative_file_list,local_dir,remote_dir):

        self.sf = paramiko.Transport((self.host, int(self.port)))
        self.sf.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(self.sf)
        trans_dict = {}

        for file in relative_file_list:
            trans_dict[local_dir+file] =(remote_dir+file).replace("\\", "/",99)

        new_dir = []

        # 根据文件名得到需要创建的文件夹，排序能够保证嵌套在先的先创建
        for file in list(trans_dict.values()):
            new_dir.append("/".join(file.split("/")[:-1]))
        new_dir = sorted(list(set(new_dir)))
        print(new_dir)

        for i in new_dir:
            try:
                sftp.mkdir(i)
            except:
                pass

        for file in trans_dict:
                file_paths = trans_dict[file].split("/")
                for i in range(len(file_paths)):
                    try:
                        dir = "/".join(file_paths[:i])
                        print("making dir",dir)
                        sftp.mkdir(dir)
                    except:

                        continue
                print(file,">>>>>>>>>>>>>>>",trans_dict[file])
                sftp.put(file,trans_dict[file])  # 上传目录中的文件





    def sftp_upload(self,local_dir,remote_dir):
        self.sf = paramiko.Transport((self.host,int(self.port)))
        self.sf.connect(username = self.username,password = self.password)
        sftp = paramiko.SFTPClient.from_transport(self.sf)


        if os.path.isdir(local_dir):  # 判断本地参数是目录还是文件
                for f in os.listdir(local_dir):  # 遍历本地目录

                    sftp.put(os.path.join(local_dir , f), os.path.join(remote_dir , f).replace("\\","/"))  # 上传目录中的文件
        else:
                sftp.put(local_dir, remote_dir)  # 上传文件



    def sftp_download(self,local_dir,remote_dir,certain_file=None):
        sf = paramiko.Transport((self.host,int(self.port)))
        sf.connect(username = self.username,password = self.password)
        sftp = paramiko.SFTPClient.from_transport(sf)
        try:

            if os.path.isdir(local_dir):#判断本地参数是目录还是文件
                remote_dir = remote_dir.replace("\\","/")

                for f in sftp.listdir(remote_dir):#遍历远程目录

                    if certain_file:
                        if f == certain_file:
                            sftp.get(os.path.join(remote_dir, f).replace("\\", "/", 2), os.path.join(local_dir, f))
                    else:

                        sftp.get(os.path.join(remote_dir,f).replace("\\","/",2),os.path.join(local_dir,f))#下载目录中文件
            else:
                sftp.get(remote_dir,local_dir)#下载文件
        except Exception as e:
            traceback.print_exc()
        sf.close()
    # 除了遍历sftp下的文件，还遍历里面的文件夹
    def sftp_download_second_dir(self,local_dir,remote_dir,certain_file=None):
        sf = paramiko.Transport((self.host, int(self.port)))
        sf.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(sf)
        try:
            if os.path.isdir(local_dir):  # 判断本地参数是目录还是文件
                remote_dir = remote_dir.replace("\\", "/")
                for f in sftp.listdir(remote_dir):  # 遍历远程目录


                    try:
                        for files in (sftp.listdir(os.path.join(remote_dir,f).replace("\\","/"))):

                            if certain_file:
                                if files == certain_file:
                                    if not os.path.exists(os.path.join(local_dir, f)):
                                        os.mkdir(os.path.join(local_dir, f))
                                    sftp.get(os.path.join(os.path.join(remote_dir, f),files).replace("\\", "/",4), os.path.join(os.path.join(local_dir, f),files))
                                    continue
                            else:
                                if not os.path.exists(os.path.join(local_dir, f)):
                                    os.mkdir(os.path.join(local_dir, f))
                                sftp.get(os.path.join(os.path.join(remote_dir, f), files).replace("\\", "/", 4),
                                         os.path.join(os.path.join(local_dir, f), files))
                                continue

                        if certain_file:
                            if f == certain_file:
                                sftp.get(os.path.join(remote_dir, f).replace("\\", "/", 4),
                                         os.path.join(local_dir, f))
                                continue
                        else:
                            sftp.get(os.path.join(remote_dir, f).replace("\\", "/", 4),
                                     os.path.join(local_dir, f))
                            continue


                    except:
                        traceback.print_exc()

        except Exception as e:
            traceback.print_exc()
            print("注意只能有一个文件夹嵌套")
        sf.close()


