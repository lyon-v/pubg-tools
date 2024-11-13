# pubg-tools


## 预期  
在吃鸡游戏还是有人气的情况下，各位大佬在孜孜不倦的提供各种帮助。
然后ghub的lua存在不灵活的问题，如每次需要在lua里面更改弹道，并且需要手动选择切换枪械，所以比较麻烦。
当然还是不做AI类的识别。

预期做到以下几点：
1. 自动识别枪械，并可以自动切换配置
2. 可以在web端（浏览器）实时修改弹道配置
3. 因为分辨率情况不同的情况下，所以要支持枪械截图



## 架构

### 整体逻辑

1. 通过前端配置设置枪械参数（手动填表）,自动生成lua和相关配置文件。
2. logitech 导入lua,并运行。
3. 游戏运行后，通过每秒识别一次屏幕，获取枪械信息和配置信息，保存到配置文件；每次开镜自动识别枪械信息或者手动切换配置信息。
   

### 实现部分

1.pyqt开发前端，用于保存参数设置，生成lua和临时配置文件。
2.python 开发捕捉屏幕自动识别枪械功能，保存到临时配置文件。
3.lua部分需要修改，在游戏中能实时读取临时配置文件，避免手动指定枪械。