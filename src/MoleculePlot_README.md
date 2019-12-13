## 改一段源码的经历
**经验：打开debug模式找参数能够解决很多问题！一路跳转找源代码不如分析对象中有什么参数，然后直接更改参数！**  

- 在mayavi中有一个parallel projection的功能用于切换平行视图，同时有lightning的设置，但是没有在maya官方文档中找到，查看源代码也没有看到相关的函数调用，于是推测maya使用了其他模块比如tvtk或者traits，如何定位相应的函数？
- 发现maya的ui文件夹中有一些图标文件是和出来的GUI一样，但是那里的图标是maya的ui用于pipeline的，于是推测与调整parallel的不是一个模块，然后搜索tvtk的ico文件或者png文件，发现了和GUI一样的可以有的parallel projection按钮，然后在里面的light manager发现了mode的切换api，在scene\_model文件中发现了Item(name="parallel_projection")，是需要的代码
- 然后里在scene model里面有get light manager函数，里面有一个scene editor，是TVTKScene的instance，然后发现tvtk\_scene中有parallel\_porjection = Bool(False,dec...)这一句，继续搜索可以找到更多调整的函数
- 但现在的问题是，如何通过maya的mlab对象拿到这个tvtkScene呢？
- 实际上在mayavi\_scene中运行这个文件，执行main中的代码，已经能够显示一个TVTK Scene了，于是代码分析的起点可以从这里开始
- 发现在mayavi\_scene\_factory中有get\_scene\_preferences，里面的res['stereo'] = eval(pref.get('tvtk.scene.stereo'))推测有用，于是用stereo = scene.stereo拿到了MayaScene的stereo
- 又发现stereo很可能是stereo = Bool(False)这个内容，**使用debug，发现stereo的确是一个bool**
- 依葫芦画瓢，关键在于**res['stereo'] = eval(pref.get('tvtk.scene.stereo'))**这一句，于是导入pref（from mayavi.preferences.preference\_manager import preference\_manager as pref
），写一个pref = preference\_manager.preferences,**parallel_projection =  eval(pref.get('tvtk.scene.parallel\_projection'))**，但是发现**pref.get('tvtk.scene.parallel\_projection')为None，于是尝试用pref的set方法搞一个print(pref.set('tvtk.scene.parallel\_projection',True))**
- 但是结果发现没有生效，采用
```
p =bindings.get_scene_preferences()  
p['tvtk.scene.parallel_projection'] = True  
set_scene_preferences(scene, p)  
```结果报错：Cannot set the undefined 'tvtk.scene.parallel_projection' attribute of a 'MayaviScene' object.
- 这里就可以发现MayaviScene对象是有background color这一个选项的，于是有必要从bgcolor如何设置找起
- bgcolor是在MayaviScene里面的background，但MayaviScene是工厂模式调用出来的通过get\_scene\_preferences()，另外bgcolor有一个scene.renderer，于是使用debug将scene的renderer对象找到

## 然而

- 在debug的时候发现，scene本身就有parallel\_projection这一个参数，并且里面的light\_manager里面也有light\_mode参数，于是直接更改为True和"vtk"，**完成！**