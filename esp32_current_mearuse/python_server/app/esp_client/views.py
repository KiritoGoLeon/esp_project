from flask import render_template, flash, redirect, url_for, request,g,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db

from datetime import datetime

from . import esp_client
from app.models_manager.user.user_models import User,Role,AndroidCodata

@esp_client.route('/', methods=['GET', 'POST'])
def index():

    return jsonify({"state": "ok"})

@esp_client.route('/upload_data', methods=['GET', 'POST'])
def upload():
    data = request.get_json()
    now_user = User.query.filter_by(username='root').first()
    use_esp = None
    for esp_device in now_user.esp_devices:
        use_esp = esp_device

    print(data)
    now_data = AndroidCodata(date=datetime.now(),current_value= abs(data['current']),wa=data['wa'])
    use_esp.android_codatas.append(now_data)

    db.session.add(now_data)
    db.session.add(use_esp)
    db.session.add(now_user)
    db.session.commit()
    return jsonify({"state": "ok"})




