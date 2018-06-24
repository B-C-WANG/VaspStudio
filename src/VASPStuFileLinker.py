
from VASPStuProject import *

def get_vasp_dir_in_dir(dir):
    files = os.walk(dir)
    vasp_dir = []
    for i in files:
        if "OUTCAR" in i[2]:
            vasp_dir.append(i[0])

    return vasp_dir


class VASPStuFileLinker(object):

    '''
    通用规则：
    任务类型在.xsd后缀之后，Convergence和NotConvergence在.xsd之前，所以需要split .xsd



    '''


    def link_file_and_vsp_dir_by_name(self,
                                      XVI_items,
                                      dir):
        vasp_dir_name_dict = {}
        vasp_dirs = get_vasp_dir_in_dir(dir)
        for i in vasp_dirs:
            vasp_dir_name_dict[i.split("\\")[-1]] = i

        vasp_dir_names = list(vasp_dir_name_dict.keys())

        for xvi_item in XVI_items:
            name = xvi_item.relative_xsd_file_name
            print(name)
            if "/" in name:
                name = name.split("/")[-1]
            else:
                name = name.split("\\")[-1]

            if ".xsd" in name: name = name.split(".xsd")[0]
            if ".cif" in name: name = name.split(".cif")[0]
            for _name in vasp_dir_names:
                vasp_dir_name = copy.deepcopy(_name)
                if ".cif" in vasp_dir_name:
                    vasp_dir_name = vasp_dir_name.split(".cif")[0]
                if ".xsd" in vasp_dir_name:
                    vasp_dir_name = vasp_dir_name.split(".xsd")[0]
                print(name,vasp_dir_name)
                if name == vasp_dir_name:
                    print("Matched")
                    xvi_item.local_vasp_dir = vasp_dir_name_dict[_name]
                    xvi_item.status = XVI_Status.Finished
                    break

    def link_file_and_vsp_dir_by_path(self,
                                      XVI_items,
                                      dir):
        vasp_dir_name_dict = {}
        vasp_dirs = get_vasp_dir_in_dir(dir)

        for i in vasp_dirs:
            i = i.replace("\\","/",99)

            vasp_dir_name_dict[i.split(dir.replace("\\","/",99))[-1].split(".xsd")[0]] = i
        print(vasp_dir_name_dict)

        vasp_dir_names = list(vasp_dir_name_dict.keys())

        for xvi_item in XVI_items:
            name = xvi_item.relative_xsd_file_name.replace("\\","/",99).split(".xsd")[0]
            print(name)

            for _name in vasp_dir_names:
                print(name,_name)
                if name == _name:
                    print("Matched")
                    xvi_item.local_vasp_dir = vasp_dir_name_dict[_name]
                    xvi_item.status = XVI_Status.Finished
                    break

















