
import pytest
import allure
from common.logger import logger
from common.common_params import set_current_step
@allure.feature("复贷模块")
class TestReLoan:
    @allure.story("续贷")
    def test_reloan(self,api):
        res=api.get_loan_info()
        res_json=res.json()
        assert res_json.get('code')==200
        order_status=res_json['data']['orderStatus']
        logger.info('获取订单状态结果:{}'.format(order_status))
        if order_status == 8:
            logger.info('当前订单处于复贷首页')
            set_current_step(res_json['data']['nextStep'])   
            assert True
        else:
            logger.info('当前订单未处于复贷')
            assert False