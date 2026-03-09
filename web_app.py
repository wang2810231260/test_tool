from flask import Flask, render_template, request, redirect, url_for, session
import os
from common.yaml_util import yaml_util
from routes.auth_routes import auth_bp
from routes.test_routes import test_bp
from routes.data_routes import data_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
# 使用固定的 secret_key 以支持多进程和重启后的 Session 持久化
app.secret_key = 'your-very-secure-and-fixed-secret-key'

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(test_bp)
app.register_blueprint(data_bp)
app.register_blueprint(admin_bp)

@app.before_request
def require_login():
    # Use endpoint names with blueprint prefix
    allowed_routes = ['auth.login', 'auth.captcha_image', 'static']
    # If endpoint is None, it might be a 404 or static file we don't know about
    if request.endpoint and request.endpoint not in allowed_routes and 'logged_in' not in session:
        return redirect(url_for('auth.login'))

@app.route('/')
def index():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    config = yaml_util.read_yaml(config_path)
    sys_codes = config.get('sys_codes', [config.get('sys_code', 'ToCredi')])
    return render_template('index.html', sys_codes=sys_codes)

if __name__ == '__main__':
    # Change port to 5001 to avoid conflicts with AirPlay Receiver on macOS
    app.run(debug=True, port=5001)
