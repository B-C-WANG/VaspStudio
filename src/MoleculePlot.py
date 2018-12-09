'''

from
http://docs.enthought.com/mayavi/mayavi/auto/example_chemistry.html#example-chemistry

'''

import os
import warnings
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
os.environ['ETS_TOOLKIT'] = 'wx'

import numpy as np
#from mayavi.tools import engine_manager
from mayavi import mlab
#from mayavi.core.ui.mayavi_scene import MayaviScene
from VDE.AtomSpace import atom_index_trans_reverse, atom_index_trans
from VDE.VASPMoleculeFeature import VASP_DataExtract
import traceback


class Plot():
    @staticmethod
    def make_color(r, g, b):
        return (r / 255, g / 255, b / 255)

    @staticmethod
    def plot_sphere(mlab, coord, radius, color, resolution=40):
        if len(np.array(coord).shape) == 1:
            mlab.points3d(coord[0], coord[1], coord[2],
                          scale_factor=radius,
                          color=Plot.make_color(color[0], color[1], color[2]),

                          scale_mode="none",
                          resolution=resolution
                          )
        elif len(np.array(coord).shape) == 2:
            mlab.points3d(coord[:,0], coord[:,1], coord[:,2],
                          scale_factor=radius,
                          color=Plot.make_color(color[0], color[1], color[2]),
                          scale_mode="none",
                          resolution=resolution
                          )

    @staticmethod
    def plot_line(mlab, startPos, endPos, radius, color,tube_resolution=20):
        mlab.plot3d([startPos[0], endPos[0]],
                    [startPos[1], endPos[1]],
                    [startPos[2], endPos[2]],
                    color=Plot.make_color(color[0],
                                          color[1],
                                          color[2]),
                    tube_radius=radius,
                    tube_sides=tube_resolution,
                    )

    @staticmethod
    def plot_double_color_line(mlab, startPos, endPos, radius, colorA, colorB,tube_resolution=20):
        middle_pos = (startPos + endPos) / 2
        Plot.plot_line(mlab, startPos, middle_pos, radius, colorA,tube_resolution)
        Plot.plot_line(mlab, middle_pos, endPos, radius, colorB,tube_resolution)


class MoleculePlot():
    COORD_SCALER = 0.001
    RADIUS_SCALER = 0.001

    def __init__(self,
                 vasp_dir: str,
                 atom_radius_config: dict,
                 bond_config: dict,
                 atom_color_config: dict,
                 bond_radius=0.2,
                 repeat_config=(0, 0, 0),
                 background_color=(0, 0, 0),
                 circle_resolution=40,
                 tube_resolution=20,
                 window_sizeX=800,
                 window_sizeY=800
                 ):
        a = VASP_DataExtract(vasp_dir)
        c = a.get_output_as_atom3Dspace(get_energy=False)
        self.circle_resolution = circle_resolution
        self.window_sizeX = window_sizeX
        self.window_sizeY = window_sizeY
        self.bond_radius = bond_radius
        self.tube_resolution = tube_resolution
        coord, force, energy, atom_cases = c.generate_data(output_force=True)
        self.repeat_config = repeat_config
        self.atom_cases = atom_cases
        self.coord = coord
        self.background_color = tuple([i / 255 for i in background_color])
        self.atom_color_config = atom_color_config
        self.mlab = None
        try:
            a.get_box_tensor_and_type_info()
            self.box_tensor = a.box_tensor_info
        except:
            print("Can not get VectorABC, can not apply periodicity")
            self.box_tensor = None

        # 把元素名称的radius转化成原子序数
        new_dict = {}
        for key in atom_radius_config:

            print(atom_index_trans[key])
            new_dict[atom_index_trans[key]] = atom_radius_config[key]
        self.atom_radius_config = new_dict
        new_dict = {}
        for key in bond_config:
            new_dict[(atom_index_trans[key[0]], atom_index_trans[key[1]])] = bond_config[key]
        self.bond_config = new_dict

        new_dict = {}
        for key in atom_color_config:
            new_dict[atom_index_trans[key]] = atom_color_config[key]
        self.atom_color_config = new_dict

    def apply_period(self, coord):
        '''
        在xyz方向分别进行重复n次
        [0,0,0]不重复
        [0,0,1]在z轴重复一次
        '''
        c = coord
        if self.box_tensor is None: return
        for direction, repeat_count in enumerate(self.repeat_config):
            if repeat_count == 0: continue

            if len(c.shape) == 2:
                c = c.reshape(1, c.shape[0], c.shape[1])
            bt = self.box_tensor[direction]

            change = np.array([0, bt[0], bt[1], bt[2]]).astype("float32")
            repeat = list(range(-repeat_count, repeat_count + 1))
            repeat.remove(0)
            repeat.insert(0, 0)

            new_c = []
            for j in repeat:
                offset = change * float(j)
                new_c.append(c + offset)
            new_c = np.concatenate(new_c, axis=1)

            c = new_c
            c = c.reshape(c.shape[1], c.shape[2])
        return c

    def plot(self, sample_index: int = -1):
        '''
         # 默认选取最后一个原子进行绘制
        '''

        maya_figure = mlab.figure(1, bgcolor=self.background_color, size=(self.window_sizeX, self.window_sizeY))
        mlab.clf()
        scene = maya_figure.scene

        mlab.options.offscreen = False
        #mayaengine = engine_manager.get_engine()
        # mayaengine.scenes

        #assert isinstance(scene, MayaviScene)

        #scene.isometric_view()
        # scene.background = (0,1,0)
        scene.parallel_projection = True
        try:
            scene.light_manager.light_mode = "vtk"
        except:
            traceback.print_exc()

        

        # renderer = scene.renderer
        # pass
        #
        # stereo = scene.stereo
        # from mayavi.preferences.preference_manager import preference_manager
        # from mayavi.preferences import bindings
        # from mayavi.core.ui.mayavi_scene import set_scene_preferences
        # pref = preference_manager.preferences
        # print(pref.get('tvtk.scene.parallel_projection'))
        # print(pref.set('tvtk.scene.parallel_projection',False))
        #
        # p =bindings.get_scene_preferences()
        # p['tvtk.scene.parallel_projection'] = True
        # set_scene_preferences(scene, p)
        # preference_manager.trait_set()
        # parallel_projection =  eval(pref.get('tvtk.scene.parallel_projection'))

        # 设置方位角，0度是侧视图，
        # mlab.view(azimuth=0)

        coord = self.coord[sample_index, :, :]
        print("Before", coord.shape)
        coord = self.apply_period(coord)
        print("After", coord.shape)

        pair_index = self.get_bond_plot_index(coord)



        # 绘制分子
        for atom_type in self.atom_cases:
            c = coord[coord[:,0] == atom_type,:]
            try:
                radius = self.atom_radius_config[atom_type]
            except KeyError:
                print("No radius for atom %s" % atom_index_trans_reverse[atom_type])
                radius = 1
            try:
                color = self.atom_color_config[atom_type]
            except KeyError:
                print("No color for atom %s" % atom_index_trans_reverse[atom_type])
                color = (255, 255, 255)

            Plot.plot_sphere(mlab, c[:,1:], radius, color, self.circle_resolution)


        # for atom_index in range(coord.shape[0]):
        #     c = coord[atom_index, :]
        #     atom_type = int(c[0] + 0.1)
        #     try:
        #         radius = self.atom_radius_config[atom_type]
        #     except KeyError:
        #         print("No radius for atom %s" % atom_index_trans_reverse[atom_type])
        #         radius = 1
        #     try:
        #         color = self.atom_color_config[atom_type]
        #     except KeyError:
        #         print("No color for atom %s" % atom_index_trans_reverse[atom_type])
        #         color = (255, 255, 255)
        #
        #     Plot.plot_sphere(mlab, c[1:], radius, color,self.circle_resolution)
        pair_index = [i.split("-") for i in pair_index]
        # 绘制化学键
        for pair in pair_index:
            atom1_c = coord[int(pair[0]), 1:]
            atom1_type = int(coord[int(pair[0]), 0])
            atom2_type = int(coord[int(pair[1]), 0])
            atom2_c = coord[int(pair[1]), 1:]
            colorA = self.atom_color_config[atom1_type]
            colorB = self.atom_color_config[atom2_type]
            #print(colorA,colorB)
            Plot.plot_double_color_line(mlab, atom1_c, atom2_c, radius=self.bond_radius,
                                        colorA=colorA,
                                        colorB=colorB,
                                        tube_resolution=self.tube_resolution
                                        )
            self.mlab = mlab
        mlab.show()

    def __del__(self):
        # 不要在这里使用mlab.close，因为mlab在另一个线程，需要它
        pass
            #
            # if self.mlab:
            #
            #     mlab.close()

    def get_bond_plot_index_by_pair(self,coord):
        # get_bond_plot_index是采用coord遍历，这里按照bond pair遍历，得到的list就可以采用批量绘制
        bond_pair = list(self.bond_config.keys())
        # 最后得到的应该是shape为-1,2的array list，每个分别是起始原子和结束原子，都是多个
        pair_index = []
        for pair in bond_pair:
            # 没有的原子种类不进行绘制
            if pair[0] in self.atom_cases and pair[1] in self.atom_cases:
                pass

        pass

    def get_bond_plot_index(self, coord):
            # 因为一般是小批量应用，一次导出100个结构不得了了，所以可以不用太过在意时间复杂度

            bond_pair = list(self.bond_config.keys())
            pair_index = []
            for atom_index in range(coord.shape[0]):

                c = coord[atom_index, :]

                atom_type = int(c[0] + 0.1)
                for pair in bond_pair:
                    if atom_type == pair[0]:
                        another_atom = pair[1]
                        for another_atom_index in self.get_other_atoms_in_distance(coord, c[1:], another_atom,
                                                                                   self.bond_config[pair]):
                            pair_index.append("-".join(sorted([str(atom_index), str(another_atom_index)])))

                    elif atom_type == pair[1]:
                        another_atom = pair[0]
                        for another_atom_index in self.get_other_atoms_in_distance(coord, c[1:], another_atom,
                                                                                   self.bond_config[pair]):
                            pair_index.append("-".join(sorted([str(atom_index), str(another_atom_index)])))
            return set(pair_index)

    def get_other_atoms_in_distance(self, coord, atom1_coord, atom2_type: int, atom1_2_distance: float):
            # print(coord)
            # 这里一般numpy没有浮点数比较问题
            # 这个是符合原子种类要求的index
            coord_index = np.argwhere(coord[:, 0] == atom2_type).reshape(-1)
            # print(coord_index)
            # 这个是符合原子种类要求的坐标
            other_atom_coord = coord[coord_index, 1:]

            distance = np.sqrt(np.sum(np.square(other_atom_coord - atom1_coord), axis=1))
            # 这个是符合原子种类要求的子array中满足distance要求的
            in_distance_atom = np.argwhere(distance < atom1_2_distance)
            # 返回满足distance要求和元素要求的所有原子在原本array中的index

            return coord_index[in_distance_atom].reshape(-1)

def normal_test():
        mlab.figure(1, bgcolor=(0, 0, 0), size=(800, 800))
        mlab.clf()
        p1 = np.array([29, 30, 38]) / 1000  # 宜小不宜大
        p2 = np.array([29, 30, 27]) / 1000
        p3 = np.array([38, 30, 27]) / 1000

        Plot.plot_sphere(mlab, p1, 0.005, (255, 0, 0))
        Plot.plot_sphere(mlab, p2, 0.005, (255, 0, 0))
        Plot.plot_sphere(mlab, p3, 0.008, (0, 255, 0))
        Plot.plot_line(mlab, p1, p2, 0.0007, (0, 0, 255))
        Plot.plot_line(mlab, p2, p3, 0.0007, (0, 0, 255))

        mlab.show()


    # test_for_molecule()
    # normal_test()

def molecule_plot():
    m = MoleculePlot(
            # VASP所在文件夹
            "C:\\Users\wang\Desktop\运行结果\Au-slab-3x5-2M2P-1.xsd_normal",
            # 原子的半径绘制
            atom_radius_config={
                "H": 0.8,
                "C": 1,
                "O": 1,
                "Pt": 2,
                "Au":2
            },
            # 原子的颜色
            atom_color_config={
                "H": (255, 255, 255),
                "C": (255, 0, 0),
                "O": (0, 255, 0),
                "Pt": (0, 0, 255),
                "Au":(0,255,255)
            },
            # 成键设置
            bond_config={
                # ("H", "C"): 1.8,  # 表示C和H距离小于2就成键
                # ("Pt", "C"): 3,
                # ("Pt", "O"): 3,
                # ("Pt", "H"): 2,
                # ("C", "O"): 1.8,
                # ("H", "O"): 1.8,
                # ("C", "C"): 1.8,

            },
            # 周期性设置
            repeat_config=(0, 0, 0),
            # 背景颜色设置
            background_color=(255, 255, 255),
            # 以下是绘制的分辨率，影响运行速度
            circle_resolution=40,
            tube_resolution=20,
            # 窗口初始宽度
            window_sizeX= 600,
            # 窗口初始长度
            window_sizeY=800,
            bond_radius = 0.05


        )
    m.plot(-1)


if __name__ == "__main__":
    # 性能测试
   #profile.run("molecule_plot()")

    # TODO：更新参数接口到vasp studio，
    # 改为多线程调用

   molecule_plot()