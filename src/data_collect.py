import os
def get_vasp_dir_in_dir(dir):
    files = os.walk(dir)
    vasp_dir = []
    for i in files:
        if "OUTCAR" in i[2]:
            vasp_dir.append(i[0])
    #print("get vasp dirs:\n","\n".join(vasp_dir))
    return vasp_dir

class DataCollector(object):
    '''
    OUT.ANI to XYZ file

    '''


    def __init__(self,run_result_dir,output_dir):

        if run_result_dir == "":
            run_result_dir = os.getcwd()
        if output_dir == "":
            output_dir = os.getcwd()

        self.base_dir = run_result_dir
        self.output_dir =output_dir
        self.result_dirs = get_vasp_dir_in_dir(run_result_dir)
        t = []
        for i in self.result_dirs:
            t.append(i.split(self.base_dir)[-1])
        self.result_dirs = t





    def OUTANI_to_xyz_file(self,result_dir_path):

            with open(self.base_dir+result_dir_path+"/OUT.ANI", "r") as f:
                data = f.readlines()
            temp = []
            for index, info in enumerate(data):
                if info.startswith("STEP"):
                    temp.append(index)
            final_step = data[temp[-1]-1:]
            final_step = "".join(final_step)

            new_name = result_dir_path.split("/")[-1]


            with open(self.output_dir+"/"+new_name+".xyz","w") as f:
                f.write(final_step)


    def all_OUTANI_to_xyz_file(self):
        for i in self.result_dirs:
            self.OUTANI_to_xyz_file(i)

    def collect_all_energy_from_OUTCAR(self):
        all_info = []
        for i in self.result_dirs:
            print("Process %s"%i)
            energy = self.collect_energy(i)

            all_info.append([i,energy])
        with open(self.output_dir+"/energy_collect.csv" , 'w') as f:
            data = []
            try:
                for i in all_info:
                    data.append(",".join(i))
            except:
                pass
            string = "\n".join(data)
            f.write(string)






    def collect_energy(self,result_dir_path):


            info_ = ""

            with open(self.base_dir+result_dir_path+"/OUTCAR", "r") as f:

                data = f.readlines()
            temp = []
            for index, info in enumerate(data):
                info = info.strip()
                if info.startswith("energy without entropy"):
                    info_ = info
            energy = info_.split("energy without entropy =")[1].split("energy")[0]
            return energy


if __name__ == '__main__':

    # DIRs of the DIR of result
    RUN_RESULTS_DIR = ""
    # the DIR for xyz files to write to.
    FILE_OUTPUT_DIR = ""

    a = DataCollector(run_result_dir=RUN_RESULTS_DIR,output_dir=FILE_OUTPUT_DIR)
    a.all_OUTANI_to_xyz_file()
    a.collect_all_energy_from_OUTCAR()







