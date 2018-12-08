'''
整个flask项目的设置都集中放在此处
包括全局变量,正则表达式匹配动态路由,数据库连接设置
'''


"""
请将全局变量设置于此处
"""

from flask import Flask,redirect,request,session

# 服务器变量设置
PORT = 6060
HOST = '0.0.0.0'
app = Flask(__name__)


# 若要修改数据库的连接参数,请在此处修改
DBPARAS={
    'USERNAME' :'root',
    'PASSWORD' :'123456',
    'HOSTNAME' :'localhost',
    'MYSQLPORT' : '3306',
    'DATABASE' :'logintest1',
}


# 默认图片路径
import os
from datetime import datetime

defaultpath=os.path.dirname(__file__) + "/static/images/uploads/"


"""
此设置适用于动态路由的的路径匹配的正则表达式转换
"""

from werkzeug.routing import  BaseConverter


class RegexConverter(BaseConverter):
    '''正则转化类,继承自BaseConverter,和基础数据类型约束具有相同格式'''
    def __init__(self,url_map,*args):
        super(RegexConverter,self).__init__(url_map)
        self.regex=args[0]
 
# 将自定义转换器添加到转换器字典中，并指定转换器使用时名字为: re
app.url_map.converters['re'] = RegexConverter



'''
此设置为连接数据库的设置,请在此处调整数据库的设置
'''


#导入模块
from flask_sqlalchemy import SQLAlchemy
import pymysql

# 数据库配置

dbconf=f"mysql+pymysql://{DBPARAS['USERNAME']}:{DBPARAS['PASSWORD']}@{DBPARAS['HOSTNAME']}:{DBPARAS['MYSQLPORT']}/{DBPARAS['DATABASE']}"
app.config['SQLALCHEMY_DATABASE_URI'] =dbconf

# 指定当视图执行完毕后,自动提交数据库操作,不需要commit操作:db.session.commit()
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True

# 如果设置成 True (默认情况),Flask-SQLAlchemy将会追踪对象的修改并且发送信号。
# 这需要额外的内存,如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = False




# 设置session的名字
app.config['SECRET_KEY']='gaodezufang'

pymysql.install_as_MySQLdb()


# 创建应用实例
db = SQLAlchemy(app)




'''
定义一个装饰器用于拦截用户登录
'''
#func是使用该修饰符的地方是视图函数
def login_require(func):
    def decorator(*args,**kwargs):
        #现在是模拟登录，获取用户名，项目开发中获取session
        username = session.get('uname','')
        upassword = session.get('upwd','')

        #判断用户名存在且用户名是什么的时候直接那个视图函数
        if (username and upassword)or(request.cookies.get('uname','') and request.cookies.get('upwd','')):
            return func(*args,**kwargs)
        else:
            #如果没有就重定向到登录页面
            return redirect("/login")
    return decorator


# from flask_login import LoginManager

# #用户认证
# login_manger=LoginManager()



# #配置用户认证信息
# login_manger.init_app(app)
# #认证加密程度
# login_manger.session_protection='strong'
# #登陆认证的处理视图
# login_manger.login_view='auth.login'
# #登陆提示信息
# login_manger.login_message=u'对不起，您还没有登录'
# login_manger.login_message_category='info'





if __name__ == '__main__':
    pass






