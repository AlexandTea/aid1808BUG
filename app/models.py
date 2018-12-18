"""
此中包含了所有需要创建的模型类
使用数据库进行管理
"""

# 导入db以便在实体类中使用
from . import db

class Users(db.Model):
    '''
        用户信息表
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(120), unique=True)
    selfinfo = db.Column(db.Text(1000),default='请输入您的个人简介')
    imgpath = db.Column(db.String(120),default=r'/static/images/uploads/default.jpg')
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

    def to_dic(self):
        dic = {
            'id':self.id,
            'name':self.name,
            'password':self.password,
            'phonenumber':self.phonenumber,
            'email':self.email,
        }
        return dic

class Houses(db.Model):
    '''
        房屋信息表
    '''
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False)
    address = db.Column(db.String(200),nullable=False)
    urls = db.Column(db.String(200),nullable=False)
    district = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text, nullable=False)
    house_image = db.Column(db.String(120), default=r'/static/images/house/default.jpg')
    history_users = db.relationship('Users',secondary='history',lazy='dynamic',backref=db.backref('history_houses',lazy='dynamic'))
    favor_users = db.relationship('Users',secondary='favor',lazy='dynamic',backref=db.backref('favor_houses',lazy='dynamic'))

    def __init__(self, title,pub_date,address,urls,district,content,house_images):
        # 用于实例对象进行赋值
        self.title = title
        self.pub_date = pub_date
        self.address = address
        self.urls=urls
        self.district = district
        self.content = content
        self.house_image = house_images

    def __repr__(self):
        return f'<User:{self.title}>'

    def to_dic(self):
        dic = {
            'id':self.id,
            'title':self.title,
            'pub_date':self.pub_date,
            'address':self.address,
            'urls':self.urls,
            'district':self.district,
            'content':self.content,
            'house_image':self.house_image,
        }
        return dic

class History(db.Model):
    '''
        查询记录表
    '''
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    house_id = db.Column(db.Integer,db.ForeignKey('houses.id'))
    pub_date = db.Column(db.DateTime,nullable=False)


    def __init__(self, user_id,house_id,pub_date):
        # 用于实例对象进行赋值
        self.user_id = user_id
        self.house_id = house_id
        self.pub_date = pub_date


class Favor(db.Model):
    '''
        用户收藏
    '''
    __tablename__ = 'favor'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    house_id = db.Column(db.Integer,db.ForeignKey('houses.id'))
    pub_date = db.Column(db.DateTime,nullable=False)

    def __init__(self, user_id, house_id, pub_date):
        # 用于实例对象进行赋值
        self.user_id = user_id
        self.house_id = house_id
        self.pub_date = pub_date



    
 
