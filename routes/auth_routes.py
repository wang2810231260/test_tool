from flask import Blueprint, request, session, url_for, redirect, Response, render_template
import requests
import json
from common.rsa import encrypt_rsa
from common import common_params

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        captcha_input = request.form.get('captcha')
        captcha_uuid = request.form.get('captcha_uuid')

        try:
            encrypted_password = encrypt_rsa(password)
            res = requests.post(
                'https://admin-api-test-arb.jinglewill.com/auth/login',
                json={
                    "username": username,
                    "password": encrypted_password,
                    "code": captcha_input,
                    "uuid": captcha_uuid
                }
            )
            res_json = res.json()
            if 'status' in res_json:
                return Response(json.dumps(res_json), mimetype='application/json')
            else:
                 token = res_json.get('token') or res_json.get('data', {}).get('token')
                 if token:
                    common_params.set_admin_token(token)
                    session['admin_token'] = token
                 
                 session['logged_in'] = True
                 return Response(json.dumps(res_json), mimetype='application/json')
            
        except Exception as e:
            return Response(json.dumps({"success": False, "msg": f"Error authenticating: {str(e)}"}), mimetype='application/json', status=500)
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/captcha')
def captcha_image():
    try:
        res = requests.get('https://admin-api-test-arb.jinglewill.com/auth/code')
        res_json = res.json()
        return Response(json.dumps(res_json), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), mimetype='application/json', status=500)
 