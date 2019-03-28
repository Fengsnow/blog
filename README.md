
#Django个人简易博客
 主要是django restframe work和Vue的结合，以简易为目的，能省就省
 - Python3.7.1
 - Django 2.1.7
 - Vue 3.0
#目前实现的功能
- Vue的适配，侧边栏动画，
- 文章，分页，分类，标签，搜索等
- 时间线的数据适配
- xadmin的使用，Ckeditor富文本的使用，图片的上传
- 使用pillow略缩图做首页图片的显示

#待实现

- 小工具的开发
- redis缓存，或许会开两个版本，一个用这个缓存，一个不用
- xadmin集成自本身，不在第三方安装了,因为装着很痛苦
- 评论的开发，或者接入畅言，因为总感觉没这个必要
- 登录功能，如果没有评论就不第三方登陆了



##安装运行

`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple numpy` 使用清华的镜像会快很多




##Xadmin的坑
(1)
Xadmin的安装，必须的保证是xadmin2.0的否则全线报错，最好去https://github.com/sshwsfc/xadmin/tree/django2
下载后本地安装

(2)
Xadmin添加用户小组件出错render() got an unexpected keyword argument 'renderer

render函数在django2.1上有变化
 .进入xadmin安装路径，编辑xadmin/views/dashboard.py

 36     #render() got an unexpected keyword argument 'renderer'
 37     #修改bug, 添加renderer
 39     def render(self, name, value, attrs=None, renderer=None):