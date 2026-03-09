import pytest
import allure
import os
import time
from common import common_params
from common.logger import logger

@allure.feature("活体检测模块")
class TestLive:
    @allure.story("用户上传活体")
    def test_update_user_liveness_info(self, api):
        current_step = common_params.get_current_step()
        if current_step != 5:
            pytest.skip(f"跳过改测试用例，当前步骤为{current_step}, 预期步骤为5")
        with allure.step("用户上传活体"):
            image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'common', 'images', '20260121-003426.jpeg')
            while True:
                res = api.update_user_liveness_info(image_path)
                res_json = res.json()
                if res_json.get('code') == 200: 
                    logger.info("活体检测通过")
                    break
                else:
                    logger.warning("活体检测失败, 2s后重试")
                    time.sleep(2)