import os
from flask import request
from config import AUTH_ENABLE, AUTH_WHITELIST
from modules.errors.errors import AuthError

def check_auth():
    if not AUTH_ENABLE:
        return
    path = request.path
    for prefix in AUTH_WHITELIST:
        if path.startswith(prefix):
            return
    evkey = request.headers.get('evkey') or request.args.get('evkey')
    env_key = os.environ.get('EVKEY')
    if not env_key:
        raise AuthError('未配置鉴权密钥')
    if evkey != env_key:
        raise AuthError('鉴权失败，evkey无效')
