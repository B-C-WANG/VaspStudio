# VaspStudio
An useful tool to submit your VASP job on HPC automatically, manage your jobs, extract eneries and export final structure to .xsd files.
## 好用的VASP任务提交和管理软件
- 自动ssh登录Linux服务器投job，只需要Material Studio摆摆结构，SFTP下载文件，剩下的VASP Studio完成
- 直接从Material Studio的xsd文件转POSCAR，自动生成POTCAR，用户自定义INCAR等文件，生成投job的配置文件，批量选取投job
- 目前支持提取能量、频率、查看RMS收敛情况，导出最后收敛结构等功能
- 树状文件目录，色块标记，管理方便
- 十分详细的文档帮助快速入手，查看UserGuide
- ssh login HPC automatically, ONLY build your structure on Material Studio and download VASP dirs, Vasp Studio do other things.
- xsd file trans to POSCAR directly, generate POTCAR automatically, just make different INCAR, KPOINTS and other files, set a Job Config of different combination of these files, then select xsd files, submit them ONEKEY
- extract energy, frequency, RMS and export final structure
- very detailed UserGuide


## How to Use?
- 下载Windows平台编译好的exe文件：https://sourceforge.net/projects/vaspstudio/files/
- 或安装Python3（推荐Anaconda3）pyqt5等运行./Main.py
- <font color="red"> **具体使用方法查看UserGuide** </font>
- <font color="red"> **如果觉得好用，点击右上角的Star增加项目的影响力** </font>

- download binary file in Windows 10：https://sourceforge.net/projects/vaspstudio/files/
- install Python3(Anaconda3 recommended), pyqt5 and other essential python libs, run ./Main.py
- <font color="red"> **More details on UserGuide-english** </font>
- <font color="red"> **Star it if you think it helps ^v^** </font>

## How to contribute
- if not familiar with submitting with github, just send your scripts to wangbch@shanghaitech.edu.cn, I will help merge your code to become one of the Contributors.
- Install Qt Designer to modify .ui files
- 如果不熟悉github代码提交，可将需要添加的功能代码发送到wangbch@shanghaitech.edu.cn，我会将作者添加到贡献者名单并将脚本整合到软件中
- 遵守GPL Licence开源协议
- 安装Qt Designer修改ui文件，安装Python3，pyqt5等必要模块开发


## 软件界面
![](https://i.imgur.com/NIYPnWP.png)
![](https://i.imgur.com/Qgvj576.png)
![](https://i.imgur.com/K3RhVTw.png)