'''
此模块用于配置路由映射函数以及反馈给客户端的视图
'''

import os
from datetime import datetime

from flask import Flask, redirect, render_template, request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from config import *
from models import *



  


@app.errorhandler(404)
def page_not_found(e):
    '''用于无法找到页面时的404提示'''
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    '''用于服务器出现错误时的提示'''
    return render_template('500.html'), 500

@app.route('/',methods=['GET','POST'])
def index():
    '''用于登录'''
    if request.method == 'GET':
        if session.get('uname','') and session.get('upwd',''):
            lname = session['uname']
            print('存在session信息,直接登录')
            return render_template('/index.html',lname=lname)
        else:
            if request.cookies.get('uname','') and request.cookies.get('upwd',''):
                session['uname']=request.cookies.get('uname','')
                session['upwd']=request.cookies.get('upwd','')
                lname = session['uname']
                print('存在cookies信息,直接登录')
                return render_template('/index.html',lname=lname)
            else:
                print('无登录信息,请重新登录')
                return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
    '''用于登录'''
    if request.method == 'GET':
        if session.get('uname','') and session.get('upwd',''):
            print('session信息已存在,直接登录')
            return redirect('/')
        else:
            if request.cookies.get('uname','') and request.cookies.get('upwd',''):
                print('cookies中判断已经登录过,重定向至主页')
                return redirect('/')
            else:
                print('无cookie信息,请重新登录')
                return render_template('/login.html')
            print('无session信息,请重新登录')
            return render_template('/login.html')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        username = request.form.get('username','')
        upassword = request.form.get('upassword','')

        user = db.session.query(Users).filter(Users.name == username).first()
        if user and user.password==upassword:
            remember = request.values.get('check')
            print('remember:',remember)
            session['uname']=user.name
            session['upwd']=upassword
            if remember:
                resp = redirect('/')
                resp.set_cookie('uname',username,3600*24*7)
                resp.set_cookie('upwd',upassword,3600*24*7)
                return resp
            else:
                return redirect('/')
        else:
            return render_template('/login.html')

@app.route('/cancel',methods=['POST'])
def cancel():
    '''用于注销信息'''
    resp = redirect('/')
    if 'uname' in session and 'upwd' in session:
        del session['uname']
        del session['upwd']
    if 'uname' in request.cookies and 'upwd' in request.cookies:
        resp.delete_cookie('uname')
        resp.delete_cookie('upwd')
    return resp

@app.route('/register',methods=['GET','POST'])
def register():
    '''用于注册'''
    if request.method == 'GET':
        return redirect('/')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        username = request.form.get('username','')
        upassword = request.form.get('upassword','')
        repassword = request.form.get('repassword','')
        if upassword != repassword:
            return redirect('/')
        phonenumber = request.form.get('phonenumber','')
        uemail = request.form.get('uemail','')
        result = db.session.query(Users).filter(Users.name == username,Users.phonenumber == phonenumber).first()
        if result :
            return redirect('/')
        else:
            user = Users(name=username, email=uemail, phonenumber=phonenumber,password = upassword,selfinfo=None,imgpath=None)
            db.session.add(user)
            db.session.commit()
            session['uname']=username
            session['upwd'] =upassword
            return redirect('/')


@app.route('/private',methods=['GET','POST'])
@login_require
def private():
    uname=session.get('uname','')
    user = Users.query.filter_by(name=uname).first()
    if request.method == 'GET':
        # print(f"user:{user},{user.selfinfo}")
        return  render_template('/private.html',user=user)
    else:
        if request.files.get('uimg',''):
            # 处理上传的文件
            # 1.得到上传的文件
            f = request.files.get('uimg')
            print('获取文件为:',f)
            # 2.将文件保存进指定的目录处
            # 3.或将文件保存进指定的目录处[绝对路径]
            # 获取当前文件所在的目录名
            # 加上上传时间格式化字符串作为文件名,避免重复datetime.now().strftime('%Y%m%d%H%M%S%f')
            # 获取文件扩展名
            ext = f.filename.split('.')[-1]
            filename =  datetime.now().strftime('%Y%m%d%H%M%S%f') + '.' + ext
            filepath = defaultpath+filename
            f.save(filepath)
            user.imgpath = r'/static/images/uploads/'+filename
        if request.form.get('upassword',''):
            user.password = request.form.get('upassword','')
        user.selfinfo = request.form.get('textarea','')
        user.name = request.form.get('username','')
        user.email = request.form.get('email','')
        user.phonenumber = request.form.get('phonenumber','')
        db.session.commit()
        return render_template('/private.html',user=user)








