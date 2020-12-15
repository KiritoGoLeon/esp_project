from flask import abort
from functools import wraps
from flask_login import current_user
from ..user.user_models import Permission

Permission = Permission()
#权限
def permission_required(permission):
    '''定义装饰器@permission_required(permission)'''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            if not current_user.can(permission):#如果当前用户不具有permission则抛出403错误。
                abort(403)
            return f(*args,**kwargs)
        return decorated_function
    return decorator