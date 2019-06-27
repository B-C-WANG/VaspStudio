import traceback
import numpy as np
from public import XVI_Status, Type

'''
存在一个bug，XVI文件的下一个循环可能使用上一个循环的数据，所以需要在添加else语句清零
比如
if info.startswith("energy  without entropy"):
    info_ = info
需要添加else:continue
否则上一个的info_就会留下来
'''


class VASPFreqExtract():
    @staticmethod
    def freq_extract( xvi_items, freq_number):
        for xvi in xvi_items:
            print(xvi.relative_xsd_file_name)
            try:
                if xvi.type != Type.Convergence: continue
                if hasattr(xvi, "local_vasp_dir") == True and xvi.local_vasp_dir is not None and len(
                        xvi.local_vasp_dir) > 0:
                    with open(xvi.local_vasp_dir + "/OUTCAR", "r") as f:
                        data = f.readlines()
                    real_freq = []
                    virtual_freq = []
                    for i in data:
                        if "cm-1" in i:
                            print(i)
                            if "f/i" in i:
                                virtual_freq.append(float(i.split("cm-1")[0].split("THz ")[-1]))
                            else:
                                real_freq.append(float(i.split("cm-1")[0].split("THz ")[-1]))

                    if len(virtual_freq) == 0 and len(real_freq) == 0:
                        continue
                    print(real_freq)
                    print(virtual_freq)
                    xvi.real_freq = real_freq
                    xvi.virtual_freq = virtual_freq
                    if len(xvi.virtual_freq) == freq_number:
                        xvi.status = XVI_Status.FreqPass
                    else:
                        xvi.status = XVI_Status.FreqFail
            except:
                continue


class VASPEnergyExtract():
    @staticmethod
    def energy_extract(xvi_items):
        # link 过后的结果才处理能量
        # 只有original的才能提取能量和RMS
        for xvi in xvi_items:
            energy = None  # 不要让前一个的局部变量变到下一个去了
            data = None

            _type = getattr(xvi, "type", "")
            if _type not in [Type.Origin, Type.Convergence, Type.NotConvergence]: continue
            if hasattr(xvi, "local_vasp_dir") == True and xvi.local_vasp_dir is not None and len(
                    xvi.local_vasp_dir) > 0:
                try:
                    with open(xvi.local_vasp_dir + "/OUTCAR", "r") as f:

                        data = f.readlines()
                    info_ = ""
                    for index, info in enumerate(data):
                        info = info.strip()
                        if info.startswith("energy  without entropy"):
                            info_ = info
                    energy = info_.split("energy  without entropy=")[1].split("energy")[0]
                    xvi.energy = energy
                except:
                    traceback.print_exc()


class VASP_RMS_Extract():
    @staticmethod
    def final_RMS_extract(xvi_items, thushold):
        for xvi in xvi_items:
            _type = getattr(xvi, "type", "")
            if _type != Type.Origin: continue
            if hasattr(xvi, "local_vasp_dir") == True and xvi.local_vasp_dir is not None and len(
                    xvi.local_vasp_dir) > 0:
                try:
                    with open(xvi.local_vasp_dir + "/OUTCAR", "r") as f:
                        data = f.readlines()
                        RMS_data = []
                        _tmp = ""
                        for i in data:
                            if "RMS" in i:
                                _tmp = i.replace("\n", "")
                                _tmp = _tmp.split(" ")
                                while "" in _tmp:
                                    _tmp.remove("")
                                _tmp = _tmp[-2]  # 看倒数第二个为原子最大的力，要求收敛

                                RMS_data.append(_tmp)
                    RMS_data = np.array(RMS_data).astype("float32")
                    xvi.final_RMS = "%.5f" % RMS_data[-1]
                    xvi.RMS_array = RMS_data
                    if RMS_data[-1] < thushold:
                        xvi.status = XVI_Status.Convergence
                    else:
                        xvi.status = XVI_Status.NotConvergence
                except:
                    traceback.print_exc()


if __name__ == '__main__':
    pass
