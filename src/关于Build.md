## 使用pyinstaller
- Build脚本：Build-pyinstall-useSpec.bat是编译成功的脚本，需要先运行Build.bat，然后停止，然后修改生成的Vasp Studio.spec文件，里面增加递归深度的修改import sys sys.setrecursionlimit(50000)，然后运行Build-pyinstall-useSpec.bat
- Build.bat-直接pyinstall进行Build，BuildMoleculePlotTest：对MoleculePlot文件进行Build，单独测试mayavi的build
## 使用cx_Freeze
需要在cx_Freeze里面把所有涉及到的包全部加上！  
然后在管理员cmd下运行python BuildFromcx_Freeze.py install  
运行时遇到了同样的问题，是No traitsui.toolkits plugin found for toolkit null
- 参考[https://stackoverflow.com/questions/50337382/creating-standalone-exe-using-pyinstaller-with-mayavi-import](https://stackoverflow.com/questions/50337382/creating-standalone-exe-using-pyinstaller-with-mayavi-import)修改，尽可能引用全
- 问题是开发使用的是pyqt5，而提示没有toolkit qt4，于是先尝试在python3中安装pyqt4，参考[https://blog.csdn.net/u012654847/article/details/75228929](https://blog.csdn.net/u012654847/article/details/75228929)安装pyqt4([https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4))，注意可能提示PyQt4已经存在，就uninstall然后重新从whl安装
- 修改了PyQt4过后先文件跑通一遍，因为有新的问题，mayavi不能够显示了，于是删除了pyqt4，重新安装pyqt5，提示没有GUI逐渐，于是安装wxPython，但是最终没有显示成功，也没有还原到之前能够显示的地方。报错主要是traits的报错
- 于是尝试尽可能重装所有的相关组件，pyqt5，mayavi，然后发现直接MoleculePlot不能够运行了，而在debug模式下可以运行，并且在VaspStudio中的mayavi可以正常运行。
- 遇到了一些bug，然后通过import PyQt5.sip和PyQt4.sip解决了，之后仍然出现了一开始的bug：No traitsui.toolkits plugin found for toolkit null


## bug记录
- Build可能遇到递归深度的问题，参考[https://blog.csdn.net/sinat_32651363/article/details/82841026](https://blog.csdn.net/sinat_32651363/article/details/82841026)，修改第一次生成的spec文件，加上递归深度50000等，然后运行
- 可能遇到 'utf-8' codec can't decode byte 0xce in position 122: invalid continuation byte的问题

- 运行编译好的文件时报错：RuntimeError: No traitsui.toolkits plugin found for toolkit null
- 在python运行时没有报错，但是编译好之后报错，[https://stackoverflow.com/questions/28079792/freezing-exe-a-traitsui-program-realistically-feasible](https://stackoverflow.com/questions/28079792/freezing-exe-a-traitsui-program-realistically-feasible)提到的可能性为使用了dynamic import
```
def import_toolkit(tk):
    try:
        # Try and import the toolkit's pyface backend init module.
        be = 'pyface.ui.%s.' % tk
        __import__(be + 'init')
    except:
        raise
    return be
```
- 解决方案：[https://stackoverflow.com/questions/50337382/creating-standalone-exe-using-pyinstaller-with-mayavi-import](https://stackoverflow.com/questions/50337382/creating-standalone-exe-using-pyinstaller-with-mayavi-import)