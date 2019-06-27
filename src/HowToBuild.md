
目前尚未解决No pyface.toolkits plugin found for toolkit wx问题
# Build流程
- 安装最新pyinstaller，pyside，pyface，mayavi等
- 运行BuildWithSpec.bat或者先运行Build.bat然后修改Spec文件再运行BuildWithSpec.bat


# bug解决
- 递归深度超出限制：在spec中添加递归深度变为更大
- 遇到问题UnicodeDecodeError，解决方法是命令行先输出chcp 65001，然后运行
- 运行时显示导入Pyside失败：修改pyinstaller将PySide改为PySide2，然后重新编译！