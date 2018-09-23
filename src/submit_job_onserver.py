"QTAVASP-SubmitJobOnServer"
# -*- coding: utf-8 -*-

import os
import copy
import time
import math

import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import json


'''
POSCAR中添加placeHolder用于取代信息
'''
ATOM_INFO_HOLDER = "<atom_info>"
POS_INFO_HOLDER = "<pos_info>"
LATTICE_VECTOR_HOLDER = "<lattice_vector>"
FORT188_HOLDER = "<fort188_info>"

'''
fort188中的placeHolder
'''
import random
class NodeDirIO(object):
    def __init__(self,info_dir,debug_mode=True):

        self.info_dir = info_dir
        self.buffer_data = None
        self.data = {}
        self.debug = debug_mode

    def record(self,dir,debug):
        if self.debug:
            nodel = str(random.random()) + "DebugModeOn"
        else:
            nodel = self.read_and_clear_buffer()
        self.data[dir] = nodel



    def read_and_clear_buffer(self):
        try:
            with open(self.buffer_file,"r")as f:
                buffer_data = f.read().replace("\n","")
            return buffer_data
        except:
            pass
        with open(self.buffer_file, "w")as f:
            f.write("")

    @property
    def node_dir_io_file(self):
        return self.info_dir + "/IO"

    @property
    def buffer_file(self):
        return self.info_dir + "/Temp"

    def save(self):

        with open(self.node_dir_io_file, "w") as f:
            f.write(json.dumps(self.data))

# class NodeDirIO(object):
#     '''
#     用于记录节点和相应的文件夹信息
#
#     '''
#
#     def __init__(self,info_dir):
#
#         self.info_dir = info_dir
#         self.buffer_data = None
#         self.read_existing_data()
#
#     def read_existing_data(self):
#
#         try:
#             with open(self.node_dir_io_file, "r") as f:
#                 self.data = json.loads(f.read())
#                 self.now_group_number = int(self.data["now_group_number"])+1
#             print("now group: ",self.now_group_number)
#         except:
#             print("No information to offer, create new.")
#             self.now_group_number = 0
#             self.data = {}
#             self.data["now_group_number"] = self.now_group_number
#
#     def show_data(self,group=None):
#         print(">>>>>>>>>>>>>>>>>>>>>")
#         if group == None:
#             for i in self.data:
#                 if i.startswith("group"):
#                     print(i,"\n")
#                     for nodel in self.data[i]:
#                         print(nodel, self.data[i][nodel])
#         else:
#             try:
#                 for nodel in self.data["group" + str(group)]:
#                     print(nodel, self.data["group" + str(group)]["nodel"][nodel])
#             except:
#                 print("Error when reading data for group %s" %group)
#         print(">>>>>>>>>>>>>>>>>>>>>")
#     def clear(self):
#         with open(self.node_dir_io_file, "w") as f:
#             f.write("")
#         self.data = ""
#
#
#
#     def save(self):
#         print(self.data)
#         with open(self.node_dir_io_file, "w") as f:
#             f.write(json.dumps(self.data))
#
#
#
#     def del_group_data(self,index):
#         try:
#             self.data["group" + str(index)] = {}
#             print("Group %s is deleted"%index)
#         except:
#             print("No such group %s"%index)
#         self.save()
#
#
#
#
#     @property
#     def node_dir_io_file(self):
#         return self.info_dir + "/IO"
#
#     @property
#     def buffer_file(self):
#         return self.info_dir + "/Temp"
#
#     def record(self,dir,debug=False):
#         if debug:
#             nodel = "debugTest%s" % dir
#         else:
#             nodel = self.read_and_clear_buffer()
#         try:
#             self.data["group" + str(self.now_group_number)][nodel] = dir
#         except:
#             self.data["group" + str(self.now_group_number)] = {}
#
#
#             self.data["group" + str(self.now_group_number)][nodel] = dir
#
#
#
#     def read_and_clear_buffer(self):
#         try:
#             with open(self.buffer_file,"r")as f:
#                 buffer_data = f.read().replace("\n","")
#             return buffer_data
#         except:
#             ""
#         with open(self.buffer_file, "w")as f:
#             f.write("")

def cmd_print_and_run(cmd_string):
    print("Run cmd: ", cmd_string)
    os.system(cmd_string)

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
                        return  False, "Linux系统下文件名不能够包括除_.-以外的符号，请检查 %s"%file

                xsd_files.append(os.path.join(i[0],file))
    if relative:
        new_xsd_files =[]
        for i in xsd_files:
            new_xsd_files.append(i.split(dir)[1])
        xsd_files = new_xsd_files
    if linux_format:
        new_xsd_files = []
        for i in xsd_files:
            new_xsd_files.append(i.replace("\\","/",99).replace(" ","",99))
        xsd_files = new_xsd_files

    print("get xsd files:\n","\n".join(xsd_files))
    return xsd_files

class Counter():

    def __init__(self, _list):
        assert isinstance(_list, list)
        self.list = _list

    def run(self):
        self.output_dict = {}
        for i in self.list:
            try:
                self.output_dict[i] += 1
            except:
                self.output_dict[i] = 1
        return self.output_dict


def warn(string):
    print("[WARN] " + string)


def error(string):
    print("[ERROR] " + string)
    exit()


class XSD_Extract(object):

    def __init__(self, xsd_files, base_xsd_dir, base_POSCAR_dir, TF_condition_func, project_type,base_fort188_path=None):

        self.project_type = project_type
        self.xsd_files = xsd_files
        if ":" in self.xsd_files[0]:
            raise ValueError("The input xsd_files must be relative path.")

        self.base_POSCAR_path = base_POSCAR_dir + "/POSCAR"
        self.base_xsd_dir = base_xsd_dir

        self.transition = False
        if base_fort188_path is not None:

            self.transition = True
            self.base_fort188_path = base_fort188_path
            with open(os.path.join(base_fort188_path, "fort.188"), "r") as f:
                data = f.read()
                if FORT188_HOLDER not in data:
                    error("Placeholder %s should be in base fort.188 file." % FORT188_HOLDER)
        else:
            print("base fort188 not found transition state parse will not use.")

        # 所有的信息存储在total data中
        self.total_data = {}

        self.read_xsd_data()

        self.get_T_F_condition_for_all_files(TF_condition_func)

        self.output_dir = base_xsd_dir

        # 存储从xsd到OUTCAR的信息，用于再从OUTCAR转回xsd
        # self.xsd_OUTCAR_transfer_data = {}

    def read_xsd_data(self):
        '''
        read xsd data generate from Material studio.
        :return:
        '''
        for file_name in self.xsd_files:
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
            print("file name: ", file_name)
            self.total_data[file_name] = {}



            xsd_tree = ET.parse(str(self.base_xsd_dir + file_name)).getroot()
            # 由于会遇到多个MappingFamily的情况，所以多次寻找找有Atom3d的
            imapping = xsd_tree.find("AtomisticTreeRoot") \
                .find("SymmetrySystem") \
                .find("MappingSet") \
                .find("MappingFamily") \
                .find("IdentityMapping")
            family = xsd_tree.find("AtomisticTreeRoot") \
                .find("SymmetrySystem") \
                .find("MappingSet") \
                .findall("MappingFamily")


            a = []
            atoms = None
            for i in family:
                a.extend(i.findall("IdentityMapping"))
            for i in a:
                if len(i.findall("Atom3d")) >= 1:
                    atoms = i.findall("Atom3d")
            if atoms is None:
                print("No atoms found")
                exit()
            print("total atom number: ", len(atoms))
            atom_index = 0
            self.total_data[file_name]["atom_info"] = a_data = {}

            for i in atoms:
                data = {}
                data["element"] = el = i.get("Components")
                # 第一个原子是没有坐标的，是000
                if i.get("XYZ") is None:
                    xyz = "0,0,0"
                else:
                    xyz = i.get("XYZ")
                x, y, z = xyz.split(",")

                data["x"] = str(round(float(x), 6))
                data["y"] = str(round(float(y), 6))
                data['z'] = str(round(float(z), 6))
                a_data[i.get("ID")] = data

                atom_index += 1
            print("atom dict")
            print(a_data)

            space_group = imapping.find("SpaceGroup")
            sdata = {}
            sdata["AVector"] = space_group.get("AVector")
            sdata["BVector"] = space_group.get("BVector")
            sdata["CVector"] = space_group.get("CVector")
            print("space group info")
            print(sdata)

            self.total_data[file_name]["space_group"] = sdata

            if self.transition == True:
                dis_stre = imapping.findall("DistanceStretcher")
                if dis_stre == None:
                    error(
                        "Can not find DistanceStretcher for transition state in file %s, please use 'Measure distance' to give two atoms." % file_name)
                if len(dis_stre) >= 2:
                    error("There are two DistanceStretcher in %s, delete one to continue." % file_name)
                dis_stre = dis_stre[0].find("RestrictableMonitorTriggerSet")

                fort188 = {}
                fort188["atom1ID"] = dis_stre.get("Objects").split(",")[0]
                fort188["atom2ID"] = dis_stre.get("Objects").split(",")[1]
                fort188["distance"] = self.get_distance_of_coord([sdata["AVector"], sdata["BVector"], sdata["CVector"]]
                                                                 , a_data[fort188["atom1ID"]],
                                                                 a_data[fort188["atom2ID"]])
                print("fort188 info")
                print("atom1: ", a_data[fort188["atom1ID"]]["element"], "| atom2: ",
                      a_data[fort188["atom2ID"]]["element"], "| distance: ", fort188["distance"])

                self.total_data[file_name]["fort188_info"] = fort188

    def get_distance_of_coord(self, ABCVector_str_list, atom1_dict, atom2_dict):
        x1 = float(atom1_dict["x"])
        y1 = float(atom1_dict["y"])
        z1 = float(atom1_dict["z"])

        x2 = float(atom2_dict["x"])
        y2 = float(atom2_dict["y"])
        z2 = float(atom2_dict["z"])

        a1_coord = self.fract_to_corrd(ABCVector_str_list, x1, y1, z1)
        a2_coord = self.fract_to_corrd(ABCVector_str_list, x2, y2, z2)
        x1 = a1_coord[0]
        y1 = a1_coord[1]
        z1 = a1_coord[2]

        x2 = a2_coord[0]
        y2 = a2_coord[1]
        z2 = a2_coord[2]

        return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2), 6)

    def fract_to_corrd(self, ABCVector_str_list,
                       frac_x,
                       frac_y,
                       frac_z):
        A = ABCVector_str_list[0].split(",")
        B = ABCVector_str_list[1].split(",")
        C = ABCVector_str_list[2].split(",")

        return [float(A[0]) * float(frac_x) + float(B[0]) * float(frac_y) + float(C[0]) * float(frac_z),
                float(A[1]) * float(frac_x) + float(B[1]) * float(frac_y) + float(C[1]) * float(frac_z),
                float(A[2]) * float(frac_x) + float(B[2]) * float(frac_y) + float(C[2]) * float(frac_z)]

    def read_base_POSCAR(self):
        '''

        read base POSCAR, now only atom element &  number and position will be changed.
        the POSCAR should contain <atom_info> and <pos_info> for replace.

        :return:
        '''
        with open(self.base_POSCAR_path, "r") as f:
            data = f.read()
            if LATTICE_VECTOR_HOLDER not in data:
                raise ValueError("There should be a <lattice_vector>.")
            if ATOM_INFO_HOLDER not in data:
                raise ValueError("There should be a <atom_info> to feed atom info data.")
            if POS_INFO_HOLDER not in data:
                raise ValueError("There should be a <pos_info> to feed position data.")
        self.base_POSCAR_data = data

    def get_T_F_condition_for_all_files(self, condition_func):
        '''
        in vasp, after the position will be T T T or F F F,
        the input function will judge, if satisfied the condition will get T T T.

        :param condition_dict:
        :return:
        '''
        for file in self.total_data:
            data = self.total_data[file]
            for atom_id in data["atom_info"]:
                data["atom_info"][atom_id]["TF_condition"] = condition_func(
                    float(data["atom_info"][atom_id]['x']),
                    float(data["atom_info"][atom_id]['y']),
                    float(data["atom_info"][atom_id]['z'])
                )

    def ___example_condition_func(self, x, y, z):
        x = float(x)
        y = float(y)
        z = float(z)
        if z > 0.1:
            return True

    def main_generate_POSCAR_and_output(self):
        '''
        收集数据，转化为POSCAR，同时输出其他必要信息，主要是POTCAR所需元素信息等

        :return:
        '''

        self.read_base_POSCAR()
        self.output_data = {}

        for file_name in self.total_data:

            new_file_name = copy.deepcopy(file_name)
            data = self.total_data[file_name]

            if self.transition:
                fort188_string = ""
                fort_state = 0

            # new_file_name = new_file_name.split("/")[-1]
            # self.xsd_OUTCAR_transfer_data[new_file_name] = {}
            atom_info = ""
            atoms_ = []
            for atoms in data["atom_info"]:
                atoms_.append(data["atom_info"][atoms]["element"])

            counter_ = Counter(atoms_).run()

            atoms_ = list(counter_.keys())

            for i in atoms_:
                atom_info += i + "   "
            atom_info += "\n"
            for i in atoms_:
                atom_info += str(counter_[i]) + '   '

            self.output_data[file_name] = {}
            self.output_data[file_name]["atom_info"] = atoms_

            pos_info = ""
            line_number = 1
            for atom in atoms_:
                for id in data["atom_info"]:
                    # self.xsd_OUTCAR_transfer_data[new_file_name][line_number-1] = id
                    atom_pos = data["atom_info"][id]

                    if atom_pos["element"] == atom:
                        if self.transition:
                            if data["fort188_info"]["atom1ID"] == id:
                                fort188_string += str(line_number) + " "
                                fort_state += 1
                            if data["fort188_info"]["atom2ID"] == id:
                                fort188_string += str(line_number) + " "
                                fort_state += 1
                            if fort_state == 2:
                                fort188_string += str(data["fort188_info"]["distance"])
                                fort_state += 1

                        add_pos_info = " "
                        for i in [atom_pos["x"],atom_pos["y"],atom_pos["z"]]:
                            if float(i) < 0:
                                add_pos_info+= " "+ "%.5f"%float(i)
                            else:
                                add_pos_info+= "  "+ "%.5f"%float(i)
                        #pos_info += "  "+ "%.5f"%float(atom_pos["x"]) + "  " + "%.5f"%float(atom_pos['y']) + "  " + "%.5f"%float(atom_pos['z'])
                        pos_info += add_pos_info
                        if atom_pos["TF_condition"] == True:
                            pos_info += "   T   T   T\n"
                        else:
                            pos_info += "   F   F   F\n"
                        line_number += 1
            if self.transition:
                print("f_string", fort188_string)
            lattice_v_info = data["space_group"]["AVector"].replace(",", "  ", 5) + '\n'
            lattice_v_info += data["space_group"]["BVector"].replace(",", "  ", 5) + '\n'
            lattice_v_info += data["space_group"]["CVector"].replace(",", "  ", 5)

            self.aim_POSCAR_data = self.base_POSCAR_data.replace(ATOM_INFO_HOLDER, atom_info)
            self.aim_POSCAR_data = self.aim_POSCAR_data.replace(POS_INFO_HOLDER, pos_info)
            self.aim_POSCAR_data = self.aim_POSCAR_data.replace(LATTICE_VECTOR_HOLDER, lattice_v_info)

            output_dir = self.output_dir + "/" + new_file_name + "_" + self.project_type

            try:
                os.makedirs(output_dir)
            except Exception as e:
                print(e)
                print("[WARN] The dir %s exists, will replace." % (output_dir))
            if self.transition:
                with open(os.path.join(self.base_fort188_path, "fort.188"), "r") as f:
                    data = f.read()
                new_data = data.replace(FORT188_HOLDER, fort188_string)
                with open(os.path.join(output_dir, "fort.188"), "w") as f:
                    f.write(new_data)

            with open(output_dir + "/POSCAR", "w") as f:
                f.write(self.aim_POSCAR_data)

            self.output_data[file_name]["aim_file_dir"] = output_dir

        # with open(os.path.join(self.output_dir,"xsd_OUTCAR_trans.json"), "w") as f:
        #    f.write(json.dumps(self.xsd_OUTCAR_transfer_data))

        return self.output_data


class CollectOtherRunFiles(object):

    def __init__(self, other_run_file_dir, base_POTCAR_dir, output_info,POTCAR_suffix):

        self.other_file_dir = other_run_file_dir
        self.base_POTCAR_dir = base_POTCAR_dir
        self.output_info = output_info
        self.POTCAR_suffix = POTCAR_suffix
        self.copy_all_other_run_files_aim_path()
        self.get_POTCAR()


    def copy_all_other_run_files_aim_path(self):
        all_base_files = []
        for i in os.listdir(self.other_file_dir):

            if not i in ["POSCAR", "POTCAR", "fort.188"]:
                all_base_files.append(self.other_file_dir + "/" + i)

        for i in self.output_info:
            print("output info", self.output_info)
            aim_path = self.output_info[i]["aim_file_dir"]

            for base_file in all_base_files:
                os.system("cp %s %s" % (base_file, aim_path))

    def get_POTCAR(self):
        for i in self.output_info:
            element_info = self.output_info[i]["atom_info"]
            POTCAR_paths = []
            for element in element_info:
                POTCAR_paths.append(self.base_POTCAR_dir + "/%s/POTCAR" % (element+self.POTCAR_suffix))
            aim_paths = " ".join(POTCAR_paths)

            cmd_print_and_run("cat %s > %s" % (aim_paths, self.output_info[i]["aim_file_dir"] + "/POTCAR"))


class JobSubmit(object):

    def __init__(self, output_info, info_dir, job_submit_command,debug_mode=True):

        self.job_submit_command = job_submit_command

        if debug_mode:
            # 如果为debug mode，就只写入NodeDirIO
            print("debug mode is on.")
            self.node_dir_io = NodeDirIO(info_dir=info_dir, debug_mode=True)
            for i in output_info:
                aim_path = output_info[i]["aim_file_dir"]
                self.node_dir_io.record(aim_path,debug=True)
            self.node_dir_io.save()
            return

        cmd_print_and_run("mkdir %s" % info_dir)

        self.output_info = output_info

        self.node_dir_io = NodeDirIO(info_dir=info_dir,debug_mode=False)

        for i in output_info:
            aim_path = output_info[i]["aim_file_dir"]
            self.job_submit(aim_path)
        self.node_dir_io.save()

    def job_submit(self, path):

        os.chdir(path)  # change the now dir, use cd won't work
        cmd_print_and_run("pwd")

        time.sleep(.2)
        cmd_print_and_run("%s > %s" % (self.job_submit_command,self.node_dir_io.buffer_file))
        #
        time.sleep(.2)

        self.node_dir_io.record(path,debug=False)




def server_submit(xsd_files, base_xsd_dir, base_run_files,job_submit_command, base_POTCAR_dir, info_dir, TF_condition_func,project_type,
                  base_fort188_path=None,debug_mode=True,POTCAR_suffix=""):
    a = XSD_Extract(xsd_files=xsd_files,
                    base_xsd_dir=base_xsd_dir,
                    base_POSCAR_dir=base_run_files,
                    TF_condition_func=TF_condition_func,
                    base_fort188_path=base_fort188_path,
                    project_type=project_type

                    # 如果计算过渡态，则给定fort188文件路径，同时xsd文件中包含一个measure distance信息
                    # base_fort188_path=BASE_FILE_DIR
                    # base_fort188_path=None
                    )
    output_info = a.main_generate_POSCAR_and_output()

    a = CollectOtherRunFiles(other_run_file_dir=base_run_files, base_POTCAR_dir=base_POTCAR_dir,
                             output_info=output_info,POTCAR_suffix=POTCAR_suffix)

    b = JobSubmit(output_info=output_info, info_dir=info_dir,
                  job_submit_command=job_submit_command,
                  debug_mode=debug_mode
                  )


if __name__ == '__main__':
    file = []
    # 读取本目录下的.vsd文件
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    for i in os.listdir(os.getcwd()):
        if i.endswith(".vsd"):
            file.append(i)
    if len(file) > 1:
        raise ValueError("There should only be one .vsd file.")
    with open(file[0], "r") as f:
        data = f.read()
        info = json.loads(data)
    # 从vs文件，实际上是VASP stuio项目的所有变量中提取信息
    if info["submit_job_function"] == "submitJob":
        xsd_files = info["submit_job_files"]
        base_xsd_dir = info["remote_project_dir"]
        base_POTCAR_dir = info["remote_base_POTCAR_dir"]
        base_run_files = info["remote_base_file_dir"]
        info_dir = base_xsd_dir
        job_submit_command = info["job_submit_command"]

        try:
            POTCAR_suffix = info["POTCAR_suffix"]
        except KeyError:
            POTCAR_suffix = ""


            # 这里fort.188就在这个base file目录之下，只是判断是否需要transition state
        project_type = info["project_type"]
        print(info["project_type"])
        if info["project_type"] == "TS_fort_188":
            base_fort188_path = base_run_files
        else:
            base_fort188_path = None
        exec(info["TF_condition_func"], globals())
        TF_condition_func = condition_func
        debug_mode = (info["debug_mode"] == "True" or info["debug_mode"] == True)


        print(base_fort188_path)

        server_submit(
            xsd_files=xsd_files,
            base_xsd_dir=base_xsd_dir,
            base_POTCAR_dir = base_POTCAR_dir,
            base_run_files=base_run_files,
            info_dir=info_dir,
            TF_condition_func=TF_condition_func,
            base_fort188_path=base_fort188_path,
            debug_mode=debug_mode,
            project_type=project_type,
            job_submit_command =job_submit_command,
            POTCAR_suffix = POTCAR_suffix

        )
