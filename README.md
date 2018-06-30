# VaspStudio
An useful tool to submit your VASP job on HPC automatically, manage your jobs and extract eneries...
## 好用的VASP任务提交和管理软件
- 自动ssh登录Linux服务器投job，只需要Material Studio摆摆结构，SFTP下载文件，剩下的VASP Studio完成
- 直接从Material Studio的xsd文件转POSCAR，自动生成POTCAR，用户自定义INCAR等文件，生成投job的配置文件，批量选取投job
- 目前支持提取能量、频率、查看RMS收敛情况，导出最后收敛结构等功能
- 树状文件目录，色块标记，管理方便
- 十分详细的文档帮助快速入手，查看UserGuide


## 使用
- 下载Windows平台编译好的exe文件：https://sourceforge.net/projects/vaspstudio/files/
- 或安装Python3（推荐Anaconda3）pyqt5等运行./Main.py
- <font color="red"> **具体使用方法查看UserGuide** </font>
- <font color="red"> **如果觉得好用，点击右上角的Star增加项目的影响力** </font>

## 开发说明
- 如果不熟悉github代码提交，可将需要添加的功能代码发送到wangbch@shanghaitech.edu.cn，我会将作者添加到贡献者名单并将脚本整合到软件中
- 遵守GPL Licence开源协议
- 安装Qt Designer修改ui文件，安装Python3，pyqt5等必要模块开发

## 软件界面
![](https://i.imgur.com/NIYPnWP.png)
![](https://i.imgur.com/Qgvj576.png)
![](https://i.imgur.com/K3RhVTw.png)