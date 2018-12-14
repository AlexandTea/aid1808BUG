"""
包含主业务逻辑的路由和视图
操作
    将main声明成一个蓝图应用
"""
from flask import Blueprint
main = Blueprint('main',__name__)

from . import views


'''
定义一个装饰器用于拦截用户登录
'''


