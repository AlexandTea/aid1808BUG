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

# class Houses(db.Model):
#     '''
#         房屋信息表
#     '''
#     __tablename__ = 'houses'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200),nullable=False)
#     pub_date = db.Column(db.DateTime,nullable=False)
#     read_num = db.Column(db.Integer)
#     content = db.Column(db.Text, nullable=False)
#     images = db.Column(db.Text)

#     def __init__(self, title,pub_date,read_num, content,images):
#         # 用于实例对象进行赋值
#         pass

#     def __repr__(self):
#         return f'<User:{self.title}>'

# class History(db.Model):
#     '''
#         查询记录表
#     '''
#     __tablename__ = 'history'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200),nullable=False)
#     pub_date = db.Column(db.DateTime,nullable=False)
#     read_num = db.Column(db.Integer)
#     content = db.Column(db.Text, nullable=False)
#     images = db.Column(db.Text)


#     def __init__(self, title,pub_date,read_num, content,images):
#         # 用于实例对象进行赋值
#         pass

#     def __repr__(self):
#         return f'<User:{self.title}>'

    
 
