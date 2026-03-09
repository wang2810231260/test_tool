import pytest 
import allure
import time
from common.db_util import DBUtils
from common.logger import logger
from common.callback import payout_callback
from common.common_params import get_access_token
@allure.feature("放款模块")
class TestPayout:
    @allure.story("放款")
    def test_payout(self,api):
        with allure.step("检查订单是否处于放款中"):
            while True:
                res=api.get_loan_info()
                res_json=res.json()
                assert res_json.get('code')==200
                order_status=res_json['data']['orderStatus']
                logger.info('获取最新订单状态结果:{}'.format(order_status))
                if order_status == 5 or order_status == 12:
                    logger.info('当前订单处于放款中')
                    db = DBUtils()
                    access_token=get_access_token()
                    user=db.select_one('get_userId_by_token',(access_token,))
                    order=db.select_one('get_payout_order',(user['account_id'],))
                    try:
                        order_payout=db.select_one('get_payout_info_by_order_id',(order['id'],))
                        if order_payout:
                            logger.info('放款流水存在，执行放款')
                            payout_callback(order_payout['order_no'],status='SUCCESS')
                            logger.info('放款回调成功')
                            res=api.get_loan_info()
                            res_json=res.json()
                            assert res_json.get('code')==200
                            break
                        else:
                            logger.info('无可放款流水了')
                            break
                        
                    except Exception as e:
                        logger.error(f"放款回调失败: {e}")
                        break
                        
                else:
                    logger.info('当前订单未处于放款中,等待5秒后重试')
                    time.sleep(5)
                
        
    