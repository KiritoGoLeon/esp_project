from flask import render_template, flash, redirect, url_for, request,g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from .forms import LoginForm, RegistrationForm


from . import login
from app.models_manager.user.user_models import User,Role

@login.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    # 获取表单
    form = LoginForm()
    # 如果是接收表单
    if form.validate_on_submit():
        # 查找用户
        user = User.query.filter_by(username=form.username.data).first()
        # 检查密码
        if user is None or not user.check_password(form.password.data):
            flash('账号或者密码错误')
            # 这个是指文件夹下的东西
            return redirect(url_for('login.index'))
        # 如果正确加载用户
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # 跳转到用户界面
            next_page = url_for('index.index')
        return redirect(next_page)
    return render_template('login/index.html', title='Sign In', form=form)

@login.route('/logout')
@login_required
def logout():
    # 先登出用户
    logout_user()
    return redirect(url_for('login.index'))


@login.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data, password =form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        # 跳转到登录界面
        return redirect(url_for('login.index'))
    #这里是指得temp下的文件夹, 我放在login目录,所以要前面加目录
    return render_template('login/register.html', title='Register', form=form)



