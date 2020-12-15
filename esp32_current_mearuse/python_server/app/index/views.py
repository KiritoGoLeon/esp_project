from . import index
import os
from flask import render_template,redirect,url_for,jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from config import Config

from app.models_manager.user.user_models import User,Role,AndroidCodata
from sqlalchemy import extract,and_
from datetime import datetime

import json


@index.route("/upload_apk", methods = ['GET', 'POST'])
@login_required
def upload_apk():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join("./apk/", f.filename))
    return jsonify({"errno": 0, "errmsg": "上传成功"})


@index.route("/android_get_info", methods = ['GET', 'POST'])
def android_get_info():
    result={
    "update": "Yes",
    "new_version": "0.8.3",
    "apk_file_url": "http://192.168.1.107:5003/",
    "update_log": "1，添加删除信用卡接口\r\n2，添加vip认证\r\n3，区分自定义消费，一个小时不限制。\r\n4，添加放弃任务接口，小时内不生成。\r\n5，消费任务手动生成。",
    "target_size": "5M",
    "new_md5": "A818AD325EACC199BC62C552A32C35F2",
    "constraint":False
    }
    return jsonify(result)


@index.route("/get_new_apk", methods = ['GET', 'POST'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    filename="app-debug.apk"
    return send_from_directory(directory, filename, as_attachment=True)


@index.route("/get_current", methods = ['GET', 'POST'])
def get_current():

    now_user = User.query.filter_by(username='root').first()
    use_esp = None
    for esp_device in now_user.esp_devices:
        use_esp = esp_device

    historys = AndroidCodata.query.filter(and_(
        extract('year', AndroidCodata.date) == datetime.now().year,
        extract('month', AndroidCodata.date) == datetime.now().month
    )).all()

    mresult_data = []
    mresult_time = []
    for mitem in historys:
        mresult_data.append(mitem.current_value)
        mresult_time.append(str(mitem.date))

    result = {
        "time": mresult_time,
        "data": mresult_data
    }
    print(result)
    return jsonify({"state": "ok", "data": result})


@index.route("/get_wa", methods = ['GET', 'POST'])
def get_wa():
    now_user = User.query.filter_by(username='root').first()
    use_esp = None
    for esp_device in now_user.esp_devices:
        use_esp = esp_device

    historys = AndroidCodata.query.filter(and_(
        extract('year', AndroidCodata.date) == datetime.now().year,
        extract('month', AndroidCodata.date) == datetime.now().month
    )).all()

    mresult_data = []
    mresult_time = []
    for mitem in historys:
        mresult_data.append(mitem.wa)
        mresult_time.append(str(mitem.date))

    result = {
        "time": mresult_time,
        "data": mresult_data
    }
    print(result)
    return jsonify({"state": "ok", "data": result})

@index.route("/")
def index():
    return  render_template('index/index.html')
