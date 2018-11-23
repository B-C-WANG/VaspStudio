# VaspStudio
An useful tool to submit your VASP job on HPC automatically, manage your jobs, extract eneries and export final structure to .xsd files.

## 更新日志 Update
### 2018年11月23日 v0.21
- 增加文件树折叠存储
- 修改收敛的导出结构的颜色，避免和收敛状态颜色相同
- 减少了不必要的窗口弹出
- Job Config新增复制功能
### 2018年9月23日 v0.201
- 从VASP提取能量对于某些情况下会出现错误，主要是energy without entropy的定位问题 
- 增加bug参考手册
### 2018年6月30日
- 更新中英文文档
### 2018年6月24日 v0.2
- 项目从DFT_Calc/pyqt5program/AUTOVASP中公开，版本v0.2。
- v0.1版本为无GUI界面的任务提交工具
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
## 工作流程
- 任务信息：所有信息用XVI对象存储，包括xsd文件路径，提取出的能量，状态等信息。UI绘制时根据这些信息绘制，一些是直接设置字符串，一些是根据状态更换颜色。UI信息获取是设置attr的数组，然后getattr获得信息进行更新。
- 信息提取：完全用XVI对象作为参数，直接获取其成员，然后修改其成员，最后返回更新，这些可用外部脚本进行。
- 多线程：目前只有任务提交使用了多线程，其他如能量提取等耗时相对较短没有使用多线程。
- 任务提交：使用python的ftp和ssh等协议连接HPC，上传下载文件和执行命令。
- UI信息：像标题栏宽度、文件树展开等这一类，在存储时对其中的信息进行存储，比如宽度用list存储，存储找VSP类中，当update UI信息时读取这些信息。
- 文件结构树：比如a/b/c/d.xsd，先用斜杠分割成a,a/b,a/b/c和a/b/c/d.xsd，然后以它们作为key，node对象作为value，能够获取node就将下一个作为它的child，如果不能获取就重新创建node，当发现是一个VSP中存储的有效XVI类时，比如用路径a/b/c/d.xsd能够获取到一个XVI类，则设置为最末节点，开始绘制信息。
- Job配置：使用文本存储所有创建的lib库的信息，用创建时设置的key作为字典的key，在lib里面是分字典存储，但是提交任务时会合成一个字典，所以key不能重复。
- 云端投Job：首先根据config设置的Key来拿到所有的lib库设置对象，比如文本库Text，文件库File，TFfunction库等。然后根据对象的instance作出相应的行为，比如Text就创建文件，File就记录文件路径，TF function就写入json信息等。最后将必要的base file准备好，额外的信息写入json文件，准备好云端执行的py文件，将这些文件上传上去，运行命令python...云端的脚本会自动进行任务提交操作，并给出反馈信息，提交完成后会给另一个线程提示，此时另一个线程运行命令获取反馈信息，更新本地信息（比如任务节点信息）。
- 二进制build：运行build.bat即可，使用pyinstaller进行build
- 输入文件创建：Material Studio的.xsd文件实际上是xml文件，可以解析后得到坐标等信息。关于过渡态，需要在Material Studio中标注键长，从而从xml文件中新增的项中找到这两个原子。一些原子没有坐标而表示为Image of ...，这种情况很难进行原子定位，故没有处理。
## 关于pyqt开发
- 建议网上搜索教程学习demo进行
- 用Qt的API进行查询，另外QtDesigner中修改控件属性后会在UI中有相应的代码，可以查阅
- 很多控件是在UI创建的，所以在Main.py中看不到它的获取。
- 在Main.py中控件没有代码补全，需要在UI_...py文件中找代码补全。


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