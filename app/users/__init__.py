"""
只处理与users相关的业务
"""


from flask import Blueprint
users = Blueprint('users',__name__)

from . import views

