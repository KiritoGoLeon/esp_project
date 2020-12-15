from  app import db

from ..models_manager.user.user_models import User, Role,EspDevice,AndroidCodata
from ..models_manager.permission.permission import Permission

DEBUG = False
from datetime import datetime
import uuid

from config import Config
class Init():
# 创建数据库
    if DEBUG:
        # 删除所有表
        db.drop_all()
        # 创建表
        db.create_all()

        esp32_device = EspDevice(esp_type=0,esp_id="esp32_01")
        db.session.add(esp32_device)

        root_user = User(email='kirito@qq.com', username='root', password='123')
        root_user.esp_devices.append(esp32_device)
        db.session.add(root_user)
        db.session.commit()



