from flask import Blueprint

# 实例化蓝图对象
index = Blueprint("index", __name__,template_folder='templates',static_folder='static')
from . import views