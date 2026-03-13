import time
import uuid
import platform
from common.logger import logger

# Global variable to store access token
_access_token = "9cc826a1fe0b47cb9c8ff242eafddfde"


def set_access_token(token):
    global _access_token
    _access_token = token

_current_step = 0

def get_access_token():
    return _access_token

_admin_token = None

def set_admin_token(token):
    global _admin_token
    _admin_token = token

import os

def get_admin_token():
    if _admin_token is not None:
        return _admin_token
    # Try to get from Flask session if not in memory
    from flask import session, has_request_context
    if has_request_context() and 'admin_token' in session:
        return session['admin_token']
        
    return os.environ.get('ADMIN_TOKEN')

_current_sys_code = None

def set_current_sys_code(code):
    global _current_sys_code
    _current_sys_code = code

def get_current_sys_code():
    if _current_sys_code is not None:
        return _current_sys_code
    return os.environ.get('SYS_CODE')


_current_mobile = None

def set_current_mobile(mobile):
    global _current_mobile
    _current_mobile = mobile

_user_id = None
def set_user_id(user_id):
    global _user_id
    _user_id = user_id

def get_user_id():
    return _user_id

def get_current_mobile():
    return _current_mobile

def set_current_step(step):
    global _current_step
    logger.info(f"Setting current step to: {step}")
    _current_step = step

def get_current_step():
    return _current_step

def get_common_params():
    """
    Generate common parameters for API requests
    """
    return {
        "platform": "android",
        "appVersion": "v1.0.0",
        "appVersionCode": 1,
        "accessToken": _access_token,
    }
