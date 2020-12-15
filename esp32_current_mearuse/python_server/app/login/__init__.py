from flask import Blueprint

# 实例化蓝图对象
login = Blueprint("login", __name__,template_folder='templates')
from . import views