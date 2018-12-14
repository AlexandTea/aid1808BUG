'''
此模块用于配置路由映射函数以及反馈给客户端的视图
'''

import os
from datetime import datetime
import json

from flask import Flask, redirect, render_template, request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from . import main
from .. import db,login_required
from ..models import *




@main.errorhandler(404)
def page_not_found(e):
    '''用于无法找到页面时的404提示'''
    return render_template('/404.html'),404


@main.errorhandler(500)
def internal_server_error(e):
    '''用于服务器出现错误时的提示'''
    return render_template('/500.html'), 500

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    '''用于抵达主页'''
    if session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        print('存在session信息,直接登录')
        return render_template('/index.html',uname=uname)
    elif request.cookies.get('uname','') and request.cookies.get('upwd',''):
        session['uname']=request.cookies.get('uname','')
        session['upwd']=request.cookies.get('upwd','')
        uname = session['uname']
        print('存在cookies信息,直接登录')
        return render_template('/index.html',uname=uname)

@main.route('/login',methods=['GET','POST'])
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
        username = request.form.get('uname','')
        print('username:',username)
        upassword = request.form.get('upassword','')
        print('upassword:',upassword)

        user = db.session.query(Users).filter(Users.name == username).first()
        print('user:',user)
        if user and user.password==upassword:
            rememberme = request.values.get('rememberme','')
            print('rememberme:',rememberme)
            session['uname']=user.name
            session['upwd']=upassword
            if rememberme == "1":
                dic = {
                    'status':2,
                    'info':'已记住密码',
                }
            else:
                dic = {
                    'status':1,
                    'info':'未记住密码',
                }
            return json.dumps(dic)
        else:
            url=request.headers.get('Referer')
            dic = {
                'status':0,
                'url':url
            }
            return json.dumps(dic)

@main.route('/01-check',methods=['GET','POST'])
def check():
    # 检查用户名是否合格
    uname = request.args.get('uname','')
    print('uname:',uname)
    user= Users.query.filter_by(name=uname).first()
    if user:
        dic = {
            'status':1,
            'info':'该用户已经注册,可以登录',
        }
    else:
        dic = {
            'status':0,
            'info':'该用户未注册,不可登录',
        }
    return json.dumps(dic)

@main.route('/02-checknumber',methods=['GET','POST'])
def checknumber():
    # 检查手机号是否合格
    phonenumber = request.args.get('phonenumber','')
    print('phonenumber:',phonenumber)
    user= Users.query.filter_by(phonenumber=phonenumber).first()
    if user:
        dic = {
            'status':1,
            'info':'该手机号已经注册,请重新输入',
        }
    else:
        dic = {
            'status':0,
            'info':'该手机号未注册,可继续注册',
        }
    return json.dumps(dic)

@main.route('/03-checkemail',methods=['GET','POST'])
def checkemail():
    # 检查邮箱是否合格
    uemail = request.args.get('uemail','')
    print('uemail:',uemail)
    user= Users.query.filter_by(email=uemail).first()
    if user:
        dic = {
            'status':1,
            'info':'该邮箱已经注册,请重新输入',
        }
    else:
        dic = {
            'status':0,
            'info':'该邮箱未注册,可继续注册',
        }
    return json.dumps(dic)

@main.route('/setsession',methods=['GET','POST'])
@login_required
def setsession():
    '''用于记住密码时设置session信息'''
    if  session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        upwd = session.get('upwd','')
        resp = redirect('/')
        resp.set_cookie('uname',uname,7*24*60*60)
        resp.set_cookie('upwd',upwd,7*24*60*60)
        return resp

@main.route('/cancel',methods=['POST'])
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

@main.route('/register',methods=['GET','POST'])
def register():
    '''用于注册'''
    if request.method == 'GET':
        return redirect('/')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        try:
            username = request.form.get('uname','')
            upassword = request.form.get('upassword','')
            phonenumber = request.form.get('phonenumber','')
            uemail = request.form.get('uemail','')
            print(f'uname:{username},upassword:{upassword},phonenumber:{phonenumber},uemail:{uemail}')
            user = Users(name=username, email=uemail, phonenumber=phonenumber,password = upassword,selfinfo=None,imgpath=None)
            db.session.add(user)
            session['uname']=username
            session['upwd'] =upassword
            dic = {
                'status':1,
                'info':'恭喜你注册成功',
            }
        except Exception as e:
            print(e)
            dic = {
                'status':0,
                'info':'注册发生错误',
            }
        return json.dumps(dic)


@main.route('/private',methods=['GET','POST'])
# 用于拦截登录
@login_required
def private():
    uname=session.get('uname','')
    user = Users.query.filter_by(name=uname).first()
    print('user:',user)
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
            # 默认图片路径
            defaultpath="/Users/zhaozhengxing/Documents/OneDrive/python3/bug_project/app/static/images/uploads/"
            filepath = defaultpath+filename
            f.save(filepath)
            user.imgpath = r'/static/images/uploads/'+filename
        if request.form.get('upassword',''):
            user.password = request.form.get('upassword','')
        user.selfinfo = request.form.get('textarea','')
        user.email = request.form.get('email','')
        user.phonenumber = request.form.get('phonenumber','')
        db.session.commit()
        return render_template('/private.html',user=user)

