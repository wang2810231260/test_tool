import pytest
import allure
from common.logger import logger
import json
from common.common_params import set_current_step

@allure.feature("订单模块")
class TestCreateOrder:

    @allure.story("创建订单")
    def test_create_order(self, api):
        with allure.step("get loan info"):
            res=api.get_loan_info(popUp=0)
            res_json=res.json()
            logger.info("Response Business Code: {}".format(res_json.get('code')))
            assert res_json.get('code') == 0
            order_status=res_json.get('data').get('loan_info').get('order_status')
            logger.info("用户当前订单状态为: {}".format(order_status))
            if order_status in [0,10,1]:
                # 获取产品列表
                with allure.step('get product list'):
                    res=api.get_product()
                    res_json = res.json()
                    logger.info("Response data: {}".format(res_json.get('data')))
                    assert res_json.get('code') == 0
                    product_list = res_json.get('data').get('product_suitable')
                    if product_list:
                         max_product = max(product_list, key=lambda x: x.get('max_amount', 0))
                         logger.info('max product: {}'.format(max_product))
                         if max_product:
                            with allure.step('create order'):
                                res=api.create_order(product_id=str(max_product.get('id_str')),loan=str(max_product.get('max_amount')),period=str(max_product.get('max_period')))
                                res_json=res.json()
                                logger.info('res data :{}'.format(res_json.get('data')))
                                assert res_json.get('code') == 0
                                current_step=res_json.get('data').get('current_step')
                                logger.info("当前步骤为: {}".format(current_step))
                                if current_step:
                                    set_current_step(current_step)                              
                    else:
                         logger.warning("No products found in product_suitable list.")

                

                

                
                
