from flask import Blueprint

# 实例化蓝图对象
esp_client = Blueprint("esp_client", __name__,template_folder='templates')
from . import views