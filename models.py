"""
此中包含了所有需要创建的模型类
使用数据库进行管理
"""



# 使用Flask_Login需要使要验证的实体对象（models.py中的Users对象）继承自UserMixin类
from flask_login import UserMixin

from config import *




class Users(db.Model,UserMixin):
    '''
        用户信息表
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(120), unique=True)
    selfinfo = db.Column(db.Text(1000))
    imgpath = db.Column(db.String(120),unique=True,default=r'/static/images/uploads/default.jpg')
    isActive = db.Column(db.Boolean, default=True)

    def __init__(self, name, email,password,phonenumber,imgpath,selfinfo):
        # 用于实例对象进行赋值
        self.name = name
        self.email = email
        self.phonenumber = phonenumber
        self.password=  password
        self.imgpath = imgpath
        self.selfinfo = selfinfo

    def __repr__(self):
        return f'<User:{self.name}>'
    
  
   
    