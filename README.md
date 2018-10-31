# <font color='green'>Flask_test_platform</font>
## 简介
flask_test_platform基于flask能快速构建web服务的特性，构建一个对测试人员友好的平台。致力于提高项目组的整体工作效率。

### 平台思路
集成项目过程中需要的各种资源，如：配置项、常用系统链接、文件管理等，项目资源统一分享，数据同源。

项目中的常用脚本服务化，通过web界面操作来完成以前本地执行脚本的完成的事项，如：查询验证码，加解密、测试数据构造等（根据实际项目需求扩展）

服务模拟，项目前后台开发进展不同步时，手动模拟后台服务，协助开发。其他用法看个人需求

集成接口自动化测试，可视化管理。

集成UI自动化报告，定时任务等（开发中。。。。）

##  现有功能演示
在线演示地址：http://119.27.173.43/

测试账号：Admin

密码：123456

#### 登录
![avatar](/static/images/login.png)

#### DashBoard
![avatar](/static/images/dashboard.png)
#### 测试用例
![avatar](/static/images/testcase.png)
#### 测试报告
![avatar](/static/images/report.png)
#### Admin管理
![avatar](/static/images/admin.png)

## 环境
python3.6

其他依赖包见requirements.txt

#### 虚拟环境（可选）
>#安装virtualenv
>pip install virtualenv
>
>#切换到你要创建虚拟环境路径，便于管理可以先创建个目录
>
>mkdir myproject
>
>cd myproject
>
>#-p 选择python版本,创建名为flaskenv的虚拟环境
>
>virtualenv -p python3.6 flaskenv
>
>#激活flaskenv
>
>source flaskenv/bin/activate

激活后数据python 可以看到是最新的版本

deactivate命令取消已激活的虚拟环境

对于不需要的虚拟环境
>rm -r /path/to/ENV

其他关于virtualenv的操作请参考官方教程：https://virtualenv.pypa.io/en/latest/userguide/

#### 安装依赖包
激活虚拟环境的情况下进入项目根目录运行
>pip -r install requirements.txt

特别说明，程序引用了`crypto`用于aes加密，依赖包安装完成后，需要手动将虚拟环境里面的`crypto`包名修改为`Crypto`,文件夹路径在虚拟环境的lib里面，如下：

>flaskenv/lib/python3.6/site-packages

安装完成后可以直接运行主程序
>python ypsh_test_platform.py

运行后本地访问：localhost：5001
如果运行包包缺失，请手动安装缺失的包
## 已开发完成功能
![avatar](/static/images/测试平台.png)

## 联系
各位看官，有好的建议或疑问，请联系：qianmengtmc@163.com、ypsh@live.com