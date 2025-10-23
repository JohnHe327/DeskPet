# DeskPet

我永远喜欢安洁莉娜安心院！

---

## 制作方法

1. 在[PRTS](prts.wiki)上下载基建、战斗正面的`.atlas`，`.png`，`.skel`文件
   - 按`F12`，选择网络(Network)，筛选`char`，点击网页中加载模型
2. 使用`spine`-`纹理解包器`导入`atlas`文件，设置输出文件夹得到碎图
3. （可选）使用`waifu`放大碎图，替换原图
   - 图片放大后阴影会变明显，可能需要使用PS逐个修正
4. 将基建`.skel`或`.json`文件拖入`spine`，设置图片放大的缩放倍数，点击`图片`，选择对应碎图文件夹
   - 来自PRTS的碎图设置缩放0.5倍
5. 将战斗`.skel`或`.json`文件拖入`spine`，取消勾选新项目，选择创建一个新骨架，点击`图片`，选择对应碎图文件夹
6. 选择`spine`-`导出`-`png`，预定输出画布大小为width × height
   + 导出类型：动画
   + 骨架：选择一个骨架
   + 动画：全部
   + 输出类型：[√]最大边界
   + 输出文件夹：`PATH/spine/`
   + 渲染：[ ]骨骼 [√]图片 [ ]其他 [√]线性过滤
   + 视区：[√]剪裁 (-width/2) (-height/4) (width) x (height)
   + 大小：缩放100%
   + 背景：[√]透明
   + 帧/秒：25
   + 播放：[√]包含最后一帧
7. 选择另一个骨架，同样导出
8. 将spine的输出父文件夹（`PATH`）修改入`spine2action.py`并运行，自动分类动作并生成`left``right`文件夹
9.  （可选）如需自定义掉落动作，可新建`drop`文件夹，放入动作序列

---
## 附件
[spine3.8.75 及部分小人素材](https://wwr.lanzoui.com/b02idsv8b)
密码：`mrfz`

[waifu及PS资源](https://pan.baidu.com/s/11AUitpgiys6YiyoDoBOKfg?pwd=p38g)

打包为exe：
```
pyinstaller -F -w -i icon.ico deskpet.pyw
```
