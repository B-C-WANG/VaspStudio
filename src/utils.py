# -*- coding: utf-8 -*-
import os

def get_vasp_dir_in_dir(dir):
    files = os.walk(dir)
    vasp_dir = []
    for i in files:
        if "OUTCAR" in i[2]:
            vasp_dir.append(i[0])
    print("get vasp dirs:\n","\n".join(vasp_dir))
    return vasp_dir



def get_all_xsd_files_in_dir(dir,relative=False,linux_format=False):
    files = os.walk(dir)
    xsd_files = []
    for i in files:
        for file in i[2]:
            if file.endswith(".xsd"):
                for char in file:

                    if char.isalnum():continue
                    elif char not in ["-","_","."]:
                        return False, "Linux系统下文件名不能够包括除_.-以外的符号，请检查 %s"%file
                        #raise ValueError()

                xsd_files.append(os.path.join(i[0],file))
    if relative:
        new_xsd_files =[]
        for i in xsd_files:
            new_xsd_files.append(i.split(dir)[1])
        xsd_files = new_xsd_files
    if linux_format:
        new_xsd_files = []
        for i in xsd_files:
            new_xsd_files.append(i.replace("\\","/",99).replace(" ","",99).replace("\\\\","/",99))
        xsd_files = new_xsd_files


    return xsd_files
