from MoleculePlot import *


# # 原子的半径绘制
# atom_radius_config = {"H": 0.8,
#                       "C": 1,
#                       "O": 1,
#                       "Pt": 2}
# # 原子的颜色
# atom_color_config = {"H": (255, 255, 255),
#                      "C": (255, 0, 0),
#                      "O": (0, 255, 0),
#                      "Pt": (0, 0, 255)}
# # 成键设置
# bond_config = {
#                   ("H", "C"): 1.8,  # 表示C和H距离小于2就成键
#                   ("Pt", "C"): 3,
#                   ("Pt", "O"): 3,
#                   ("Pt", "H"): 2,
#                   ("C", "O"): 1.8,
#                   ("H", "O"): 1.8,
#
#               }
# # 周期性设置
# repeat_config = (1, 1, 0)
# # 背景颜色设置
# background_color = (255, 255, 255)
# # 以下是绘制的分辨率，影响运行速度
# circle_resolution = 40
# tube_resolution = 20

def submit_plot(xvi_item, config_string):
    # 这里采用字符串exec传参
    # global atom_radius_config, bond_config, \
    #     atom_color_config, repeat_config, background_color, \
    #     circle_resolution, tube_resolution, window_sizeX, window_sizeY
    print(config_string)
    exec(config_string)
    #print(globals())
    #print("Locals")
    print(locals()["atom_radius_config"])

    vasp_dir = xvi_item.local_vasp_dir
    m = MoleculePlot(vasp_dir=vasp_dir,
                     atom_radius_config=locals()["atom_radius_config"],
                     bond_config=locals()["bond_config"],
                     atom_color_config=locals()["atom_color_config"],
                     repeat_config=locals()["repeat_config"],
                     bond_radius=locals()["bond_radius"],
                     background_color=locals()["background_color"],
                     circle_resolution=locals()["circle_resolution"],
                     tube_resolution=locals()["tube_resolution"],
                     window_sizeX=locals()["window_sizeX"],
                     window_sizeY=locals()["window_sizeY"],
                     )
    m.plot(-1)
