import pytest
import allure
from apis.api_service import ApiService
# from common.yaml_util import yaml_util # Removed as per refactor
import os
import json
import random
from common.logger import logger
from common.common_params import set_access_token
from common import common_params
from common.db_util import DBUtils
from common.id_utils import CBUUtil, CUITUtil
@allure.feature("登录注册功能")
class TestLogin:
    def generate_mobile(self):
        first_digit = str(random.randint(1, 8))
        other_digits = "".join([str(random.randint(0, 9)) for _ in range(9)])
        suffix = first_digit + other_digits
        return suffix
    @allure.story("登录场景")
    def test_login_by_sms(self, api):
        mobile = self.generate_mobile()
        common_params.set_current_mobile(mobile)
        logger.info(f"Generated mobile : {mobile}")
        
        with allure.step(f"send sms to {mobile}"):
            res=api.send_sms_code(mobile=mobile, sms_type=0)
            res_json = res.json()
            assert res_json.get('code') == 200
            logger.info("发送验证码成功")
        with allure.step(f"login with mobile {mobile}"):
            res = api.login_by_sms(mobile=mobile, auth_code="8888")
            res_json = res.json()
            assert res_json.get('code') == 200
            logger.info("登录成功")
            token=res_json['data']['accessToken']
            logger.info("token: {}".format(token))
            if token:
                set_access_token(token)
                logger.info("token: {}".format(token))
                with allure.step("获取用户订单状态"):
                    res = api.get_loan_info()
                    res_json = res.json()
                    assert res_json.get('code') == 200
                    logger.info("获取用户订单状态成功：{}".format(res_json['data']))
                    if res_json['data']['orderStatus'] == 0:
                        logger.info("订单状态为0,用户信息需要填写")
                        current_step = res_json['data']['nextStep']
                        common_params.set_current_step(current_step)
                        db=DBUtils()
                        #查找用户id
                        result=db.select_one('get_userId_by_token',(token,))
                        user_id=result['account_id']
                        common_params.set_user_id(user_id)
                        db.close()
                        # Write to temp file for web_app.py to read unconditionally
                        temp_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'common', 'temp_run_data.json')
                        with open(temp_file_path, 'w') as f:
                            json.dump({
                                'mobile': common_params.get_current_mobile(),
                                'user_id': user_id
                            }, f)
                        

               
                   


 
