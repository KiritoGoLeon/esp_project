from flask import Blueprint

# 实例化蓝图对象
admin = Blueprint("admin", __name__,template_folder='templates')
from . import views