from . import admin
from flask import render_template, redirect, url_for, flash,request,jsonify
from flask_login import login_user, logout_user, current_user, login_required
import  json
from  .forms import AdminEditForm

@admin.route("/", methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.DEPT_ADMIN)
def index():
    form = AdminEditForm()
    if form.validate_on_submit():
        print("sdf")

    result_json=[]
    result_json_item = \
        {
            "username":"kirito",
            "role":"asd",
            "passwd":"pasdf",
            "card_account": "123",
             "card_name":"asdf",
            "card_passwd":"123",
            "card_dir": "123",
            "create_time": "123",
        }
    result_json.append(result_json_item)
    return render_template('admin/index.html',result_json=json.dumps(result_json),form=form)