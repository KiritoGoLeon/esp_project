from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

class AdminEditForm(FlaskForm):
    #useraccount = StringField('账号', validators=[DataRequired()])
    card_name= StringField('打卡名字', validators=[DataRequired()])
    card_account = StringField('打卡账号', validators=[DataRequired()])
    card_passwd = StringField('打卡密码', validators=[DataRequired()])
    submit = SubmitField('提交')