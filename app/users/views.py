"""
Users中的视图以及路由函数
"""


import os
from datetime import datetime
import json

from flask import Flask, redirect, render_template, request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from . import users

@users.route('/user/test')
def test2():
        return '这是views下的视图'