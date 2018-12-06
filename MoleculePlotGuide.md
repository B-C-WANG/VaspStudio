## How To Plot Molecule in VaspStudio?
![](https://i.imgur.com/9tW9xVB.png)
### Set plot config
![](https://i.imgur.com/X4Ua20W.png)

- atom\_radius\_config: 绘制某种原子的半径
- atom\_color\_config: 某种原子的RGB值
- bond\_config: 设置成键，两个元素距离小于规定值时成键
- repeat\_config: 设置周期性，比如(1,1,0)代表X轴方向重复1次，Y重复1次，注意重复时正负方向都会有，最后得到的晶胞大小是(3,3,1)
- background\_color：背景颜色的RGB值
- window\_sizeX, window\_sizeY：一开始显示窗口的大小，用于方便快速截图
- circle\_resolution：绘制球体时的分辨率，较高质量好，但是卡顿
- tube\_resolution：绘制键的分辨率，较高质量好，但是卡顿
![](https://i.imgur.com/CGgbeaX.png)