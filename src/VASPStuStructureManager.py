
import traceback
import numpy as np
from public import XVI_Status
import os
from utils import get_vasp_dir_in_dir
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



class VASPStuStructureManager():

    def final_outani_structure_export(self,xvi_items):
        for xvi in xvi_items:
            if not (xvi.status == XVI_Status.Convergence or xvi.status == XVI_Status.NotConvergence):continue
            if hasattr(xvi, "local_vasp_dir") == True and xvi.local_vasp_dir is not None and len(
                    xvi.local_vasp_dir) > 0:

                self.trans_one_to_xsd(vasp_dir=xvi.local_vasp_dir,
                                      xsd_file=xvi.local_xsd_path,
                                      status = xvi.status,
                                      output_dir=os.path.dirname(xvi.local_xsd_path),
                                      xvi=xvi)


    def trans_one_to_xsd(self, vasp_dir,xsd_file,status,output_dir,xvi):

            def get_poscar_contcar_coord(choose):
                if choose == "POSCAR":
                    file = "POSCAR"
                elif choose == "CONTCAR":
                    file = 'CONTCAR'
                else:
                    print("Error: you can only choose POSCAR or CONTCAR")
                    return

                with open(os.path.join(vasp_dir, file).replace("\\\\","/",99), "r") as f:
                    data = f.readlines()
                    for i in range(len(data)):
                        if "Direct" in data[i]:
                            data = data[i+1:]
                            break
                    init_coord = {}
                    line_number = 0
                    for i in data:
                        c = i.replace("T","",6)
                        c = c.replace("F", "", 6)
                        c = c.replace("\n", "", 6)
                        c = c.split(" ")
                        while "" in c:
                            c.remove("")
                        init_coord[str(line_number)] = c
                        line_number += 1

                    return init_coord

            def judge_coord_same(list1,list2):
                print(list1," | ",list2)

                def transfer_to_same_format(list_):
                    # 注意四位小数就行了
                    return int(10000* float(list_[0])),int(10000* float(list_[1])),int(10000* float(list_[2]))
                x1,y1,z1 = transfer_to_same_format(list1)
                x2,y2,z2 = transfer_to_same_format(list2)
                print(">>>>>>>>>>>>>>>>")
                print(x1,y1,z1)
                print("to")
                print(x2, y2, z2)
                if abs(x1 - x2)<=2 and abs(y1 - y2)<=2 and abs(z1 - z2)<=2:
                    return True




            def compare_and_change_xsd_info(file_name,final_coord,initial_coord,output_dir,status,xvi):

                    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
                    print("file name: ", file_name)

                    xsd = ET.parse(file_name)
                    xsd_tree = xsd.getroot()
                    imapping = xsd_tree.find("AtomisticTreeRoot") \
                        .find("SymmetrySystem") \
                        .find("MappingSet") \
                        .find("MappingFamily") \
                        .find("IdentityMapping")
                    atoms = imapping.findall("Atom3d")

                    space_group = imapping.find("SpaceGroup")
                    sdata = {}
                    sdata["AVector"] = space_group.get("AVector")
                    sdata["BVector"] = space_group.get("BVector")
                    sdata["CVector"] = space_group.get("CVector")
                    print("space group info")
                    print(sdata)



                    print("total atom number: ", len(atoms))

                    right_count = 0
                    print(atoms)
                    for i in atoms:
                        # 第一个原子是没有坐标的，是000
                        if i.get("XYZ") is None:
                            print("None")
                            continue
                        else:
                            xyz = i.get("XYZ")
                        list1 = xyz.split(",")

                        #这里直接开始比对，然后替换

                        for key in initial_coord:
                            if judge_coord_same(list1,initial_coord[key]):
                                right_count += 1

                                i.set("XYZ",",".join(final_coord[key]))
                                print(initial_coord[key],final_coord[key])

                                break
                        print("Not MATCH")
                    # match state用来展示导出时原子匹配的数目，全部匹配才有效
                    xvi.match_state = "%s/%s"%(right_count+1,len(atoms))



                    self.save_path =os.path.join(output_dir,file_name.split("\\")[-1].replace(".xsd","")+"_%s.xsd" % status)
                    index = 0
                    while os.path.exists(self.save_path):
                        self.save_path =os.path.join(output_dir,file_name.split("\\")[-1].replace(".xsd","")+"_%s%s.xsd" % (index,status))
                        index += 1
                    print("Export To",self.save_path)
                    xsd.write(self.save_path)

                    # 第一个原子不会比对，直接就是0,0,0，这里打印比对成功的数目
                    print("Finished compare, total %s/%s matched. \nNotice: the first atom is always 0,0,0 in Material Studio, if there's no 0,0,0 in CONCAR, please change the code there."%(right_count,len(atoms)))

            coord_dict = get_poscar_contcar_coord("CONTCAR")
            initial_coord = get_poscar_contcar_coord("POSCAR")
            compare_and_change_xsd_info(xsd_file,
                                        final_coord=coord_dict,
                                        initial_coord=initial_coord,
                                        status=status,
                                        output_dir=output_dir,
                                        xvi=xvi)



