# movie-recommendation-system
Python+Django
# 

[toc]

## 简单介绍

很简单一个推荐系统，主要给自己练手，熟悉一下Django和Python，大概一个月完成，用的Django和Python都是3版本。

数据用的MovieLens的，原始数据在work\data\MovieLens下。

Django的确实好用，看开发文档可以解决挺多事，大部分内容都是模仿官方文档给的polls教程完成的。

## 系统使用

下载完成以后在`work\movie\movieapp\setting`里找到DATABASE设置数据库的端口、名称和密码。（用的MySQL）

激活虚拟环境，然后在`terminal`

利用`py manage.py makemigrations`  生成迁移文件

利用`py mange.py migrate` 更新数据库

数据库需要自行导入work\data下的`homepage_movie`，`homepage_genres`和`homepage_rating`（homepage_rating比较大，快速导入可以看最后一节数据库导入非常大的csv）

利用`py manage.py createsuperuser` 创建超级管理员（创建超级用户可以后台查看models数据)

最后`py mange.py runserver` 就可以运行了

## Django常用语句

```python
django-admin startproject movieapp # 新建工程 (movieapp)可替代工程名
py manage.py startapp movieapp # 创建项目 (movieapp)可替代项目名
py manage.py createsuperuser # 超级创建管理员

py manage.py makemigrations # 模型的改变生成迁移文件
py manage.py migrate # 数据库迁移
py manage.py runserver # 运行
```

## 虚拟环境

创建虚拟环境以后要添加`Package` 

可以点击Pycharm里的setting→Project:work→Project Interpreter选择相应虚拟环境添加

```python
conda deactivate #关闭pycharm自动打开的base虚拟环境
# 创建虚拟环境venv0
python -m venv0
# 进入venv0虚拟环境下的Scripts 激活venv0虚拟环境
activate
# 离开虚拟环境
deactivate
```

## 注册和登录

真没学过Js,Html和CSS，所以登录注册页面是在网上搜索的，是下面这个网址。jQuery的星星求助了朋友。

主页用的Django的模板语句，有点意思。

>https://www.cnblogs.com/wj-1314/p/10751411.html

## 推荐算法

推荐算法用的协同过滤，网上搜索一下就能找到公式。

## 数据库

创建项目时Django用的不是MySQL，有需求可以在项目setting下更改DATABASES。

数据库实在出太多问题了，只记录三个。

### 忘记密码

> https://www.cnblogs.com/jerrys/p/10626408.html

### 导入CSV报错

建立的schema和table的编码设定都是`utf8_general_ci`

但是导入csv时数据不能导入，尝试以下几个方法：

1. csv文件另存为`csv utf-8(逗号分隔).csv`格式，同时另存为工具中的设置web选项-编码-Unicod(UTF-8)
2. 将文件用记事本打开，另存为中将编码格式改成utf-8，再保存
3. 将文件用notepad打开，编码转换为utf-8，不可以使用utf-8-BOM

### 导入数据量非常大的csv

路径要更换一下

```mysql
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/movies.csv' into table movies fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\r\n';
```

如果下面报错提示

```mysql
error:
he MySQL server is running with the --secure-file-priv option so it cannot execute this statement
```

按下面这个链接修改下my.ini文件

> https://blog.csdn.net/wu9caiji/article/details/91818855

如果报错字符类型有问题，可以尝试csv的第一行删掉。
