from app import db,login
from flask_login import UserMixin,current_user,AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Permission:  # 权限常量
    NORMAL_USER = 0x01  # 普通用户
    DEPT_ADMIN = 0x02  # 部门管理者
    ROOT_USER =  0x04  # 超级用户

class RoleID:  # 权限常量
    user = 1  # 普通用户
    dept_admin = 2  # 部门管理者
    root_user = 4  # 超级用户

t_stu_cur = db.Table("table_role_user",
         db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
         db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
         )

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(64))
    name = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    # 多对多关系属性, 还需要设置参数secondary="关系表名"
    users = db.relationship("User", backref="role", secondary="table_role_user")
    #users = db.relationship('User', backref='role')

    def __init__(self, **kwargs):  # 初始化角色权限
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    # 角色权限
    def has_permission(self, perm):  # 判断当前角色是否已经有该权限
        return self.permissions & perm == perm

    def add_permission(self, perm):  # 角色添加权限
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permiss(self, perm):  # 角色删除权限
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):  # 重置角色
        self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name



# 采集的安卓数据
class AndroidCodata(db.Model):
    __tablename__ = 'android_codata'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    current_value = db.Column(db.Integer)
    wa = db.Column(db.Integer)
    esp_device_id = db.Column(db.Integer, db.ForeignKey('esp_device.id'))

# ESP设备
class EspDevice(db.Model):
    __tablename__ = 'esp_device'
    id = db.Column(db.Integer, primary_key=True)
    esp_type = db.Column(db.Integer)
    esp_id = db.Column(db.String(128))
    android_codatas = db.relationship("AndroidCodata", backref="esp_device")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



#继承了flask-login和数据库
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, default=datetime.now)
    esp_devices = db.relationship("EspDevice", backref="user")


    def create_card(self,img,record_state,record_log):

        mcrad = CardRecord(user_name=self.username,record_time=str(datetime.now()),record_state=record_state,record_log=record_log)
        self.card_record.append(mcrad)
        db.session.add(self)
        db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 这里的 role是backref,是隐藏默认添加的外键
        self.role = []

    def set_role(self,role):
        self.role.append(role)

    def get_new(self):
        return self.role
    # 不能读取
    @property
    def password(self):
        raise "you cant read it"

    # 使用user.password='asda'设置时存入生成的散列密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def change_password(self,new_password):
        self.password_hash = generate_password_hash(new_password)
    # 检查密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 检查权限
    def can(self, permissions):
        if self.role is None:
            return False
        else:
            for role_item in self.role:
                if (role_item.permissions & permissions) == permissions:
                    return True
            return False

    #是否是管理员
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_admin(self):
        return False
# 匿名访问者
login.anonymous_user = AnonymousUser

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


