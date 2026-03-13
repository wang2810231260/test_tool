from flask import Blueprint, request, Response, session
import os
import subprocess
import json
from common import common_params

test_bp = Blueprint('tests', __name__)

STATUS_TO_TEST_MAP = {
    'pending': ['testcases/test_login.py','testcases/test_update_user_info.py','testcases/test_live.py'],
    'pending_liveness': ['testcases/test_login.py','testcases/test_update_user_info.py'],
    'not_pass': ['testcases/test_login.py', 'testcases/test_update_user_info.py', 'testcases/test_live.py','testcases/test_order_apply_not_pass.py'],
    'calculated': ['testcases/test_login.py', 'testcases/test_update_user_info.py', 'testcases/test_live.py','testcases/test_order_apply.py'],
    'shipped': ['testcases/test_login.py', 'testcases/test_update_user_info.py', 'testcases/test_live.py','testcases/test_order_apply.py','testcases/test_order_comfirm.py'],
    'payout_failed': ['testcases/test_login.py', 'testcases/test_update_user_info.py', 'testcases/test_live.py','testcases/test_order_apply.py','testcases/test_order_comfirm.py','testcases/test_payout_failed.py'],
    'paid': ['testcases/test_login.py', 'testcases/test_update_user_info.py', 'testcases/test_live.py','testcases/test_order_apply.py','testcases/test_order_comfirm.py','testcases/test_payout.py'],
    'reloan_trial': ['testcases/test_login.py', 'testcases/test_update_user_info.py', 'testcases/test_live.py','testcases/test_order_apply.py','testcases/test_order_comfirm.py','testcases/test_payout.py','testcases/test_payment.py','testcases/test_reloan.py']
}

@test_bp.route('/run_tests', methods=['GET'])
def run_tests():
    if 'logged_in' not in session:
        return Response("data: >>>ERROR::Unauthorized\n\n", mimetype='text/event-stream')

    token = common_params.get_admin_token()
    admin_token_str = str(token) if token else None

    def generate():
        cwd = os.getcwd()
        env = os.environ.copy()
        env['PYTHONPATH'] = cwd
        env['USE_WEB_ORDER'] = '1'
        env['PYTHONUNBUFFERED'] = '1'
        
        if admin_token_str:
            env['ADMIN_TOKEN'] = admin_token_str
        
        process = subprocess.Popen(
            ['pytest', '-s'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd,
            env=env,
            bufsize=1,
            universal_newlines=True
        )
        
        for line in iter(process.stdout.readline, ''):
            if line:
                yield f"data: {line}\n\n"
                if 'Callback Request Failed: 401' in line or 'token已失效' in line:
                    process.terminate()
                    yield "data: >>>TOKEN_EXPIRED\n\n"
                    return
                
        process.stdout.close()
        process.wait()
        
        if process.returncode == 0:
            yield "data: >>>TEST_EXECUTION_COMPLETE::SUCCESS\n\n"
        else:
            yield "data: >>>TEST_EXECUTION_COMPLETE::FAILURE\n\n"

    return Response(generate(), mimetype='text/event-stream')

@test_bp.route('/generate_order_tests', methods=['GET'])
def generate_order_tests():
    if 'logged_in' not in session:
        return Response("data: >>>ERROR::Unauthorized\n\n", mimetype='text/event-stream')

    status = request.args.get('status')
    if not status or status not in STATUS_TO_TEST_MAP:
        return Response("data: >>>ERROR::Invalid status\n\n", mimetype='text/event-stream')

    test_files = STATUS_TO_TEST_MAP[status]
    selected_app = request.args.get('app')
    token = common_params.get_admin_token()
    admin_token_str = str(token) if token else None

    def generate_custom():
        try:
            cwd = os.getcwd()
            env = os.environ.copy()
            env['PYTHONPATH'] = cwd
            env['USE_WEB_ORDER'] = '1'
            env['PYTHONUNBUFFERED'] = '1'
            
            if selected_app:
                env['SYS_CODE'] = selected_app
            if admin_token_str:
                env['ADMIN_TOKEN'] = admin_token_str
            
            valid_files = [f for f in test_files if os.path.exists(os.path.join(cwd, f))]
            total_files = len(valid_files)
            if total_files == 0:
                yield "data: >>>ERROR::No valid test files found for this status\n\n"
                return
            yield f"data: >>>TOTAL_FILES:::{total_files}\n\n"

            process = subprocess.Popen(
                ['pytest', '-s'] + valid_files, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd,
                env=env,
                bufsize=1,
                universal_newlines=True
            )
            
            current_file = None
            for line in iter(process.stdout.readline, ''):
                if line:
                    yield f"data: {line}\n\n"
                    if 'Callback Request Failed: 401' in line or 'token已失效' in line:
                        process.terminate()
                        yield "data: >>>TOKEN_EXPIRED\n\n"
                        return
                    if ">>>CURRENT_CASE:::" in line:
                        parts = line.split(">>>CURRENT_CASE:::")
                        if len(parts) > 1:
                            case_path = parts[1].split("::")[0].strip()
                            if case_path != current_file:
                                if current_file is not None:
                                    yield f"data: >>>FILE_COMPLETE:::{current_file}\n\n"
                                current_file = case_path
                                yield f"data: >>>STARTING_FILE:::{current_file}\n\n"
            process.wait()
            if current_file is not None:
                 yield f"data: >>>FILE_COMPLETE:::{current_file}\n\n"
            
            if process.returncode != 0 and process.returncode != 5:
                yield "data: >>>TEST_EXECUTION_COMPLETE::FAILURE\n\n"
            else:
                generated_mobile, generated_user_id = "", ""
                temp_file_path = os.path.join(cwd, 'common', 'temp_run_data.json')
                if os.path.exists(temp_file_path):
                    try:
                        with open(temp_file_path, 'r') as f:
                            data = json.load(f)
                            generated_mobile = data.get('mobile', '')
                            generated_user_id = data.get('user_id', '')
                    except: pass
                    os.remove(temp_file_path)
                yield f"data: >>>TEST_EXECUTION_COMPLETE::SUCCESS:::{generated_mobile}:::{generated_user_id}\n\n"
        except Exception as e:
            yield f"data: >>>ERROR::Internal Server Error: {str(e)}\n\n"

    return Response(generate_custom(), mimetype='text/event-stream')
