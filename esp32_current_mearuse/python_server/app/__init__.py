from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_login import LoginManager

# 注册蓝图
def create_bluemap(system_app):
    from app.index import index
    from app.login import login
    from app.admin import admin
    from app.esp_client import esp_client

    system_app.register_blueprint(index, url_prefix='/')
    system_app.register_blueprint(login, url_prefix='/login')
    system_app.register_blueprint(admin, url_prefix='/admin')
    system_app.register_blueprint(esp_client, url_prefix='/esp_client')

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login.index'
create_bluemap(app)

from app.init import Init