import pytest
import allure
from common.logger import logger
import time
from common.db_util import DBUtils
import json
from common.callback import payment_callback
from common.common_params import get_access_token

@allure.feature("还款模块")
class TestPayment:
    @allure.story("模拟还款")
    def test_payment(self,api):
        with allure.step("检查订单是否处于待还款"): 
            res=api.get_loan_info()
            res_json=res.json()
            assert res_json.get('code')==200
            order_status=res_json['data']['orderStatus']
            logger.info('获取订单状态结果:{}'.format(order_status))
            if order_status == 7 or order_status == 11 or order_status == 9 :   
                logger.info('当前订单处于待还款')
                with allure.step("获取还款信息"):
                    res=api.paymentInfo()
                    res_json=res.json()
                    assert res_json.get('code')==200
                    payment_info=res_json['data']
                    logger.info('获取还款信息结果:{}'.format(payment_info))
                    unpaid_amount=payment_info['unpaid']
                    logger.info('当前订单剩余应还金额:{}'.format(unpaid_amount))
                    with allure.step("进行还款"):
                        payment_type=payment_info['channelList'][0]
                        logger.info('选择还款方式:{}'.format(payment_type))
                        res=api.createPayment(amount=unpaid_amount,channel=payment_type['channelCode'])
                        res_json=res.json()
                        assert res_json.get('code')==200
                        logger.info('创建还款流水成功')
                        with allure.step("回调还款"):
                            db=DBUtils()
                            access_token=get_access_token()
                            user=db.select_one('get_userId_by_token',(access_token,))
                            order=db.select_one('get_payment_order',(user['account_id'],)) 
                            payment_info=db.select_one('get_payment_info_by_order_id',(order['id'],))
                            if payment_info:
                                try:
                                    order_no = payment_info['order_no']
                                    amount = int(payment_info['amount'])
                                    payment_callback(order_no,status='SUCCESS',amount=amount)
                                    logger.info('回调还款成功')
                                    while True:
                                          res=api.get_loan_info()
                                          res_json=res.json() 
                                          assert res_json.get('code')==200
                                          order_status=res_json['data']['orderStatus']
                                          if order_status == 8:
                                            logger.info('订单已结清')
                                            break
                                            assert True     
                                          else:
                                            time.sleep(5)   
                                            logger.info('订单未结清')
                                            assert False
                                except Exception as e:
                                    logger.error('回调还款失败:{}'.format(e))
                                    assert False
                            else:   
                                logger.error('未查询到还款流水')
                                assert False
            #           

                        

                    
                
            
