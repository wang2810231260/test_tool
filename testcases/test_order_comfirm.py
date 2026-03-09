import pytest
import allure
from common.logger import logger
import time
@allure.feature("订单确认放款")
class  TestOrderComfirm:
    @allure.story("订单审核通过确认放款")
    def test_order_comfirm(self,api):
        with allure.step("检查订单是否审核通过"):
            while True:
                res=api.get_loan_info()
                res_json=res.json()
                assert res_json.get('code')==200
                order_status=res_json['data']['orderStatus']
                logger.info('获取最新订单状态结果:{}'.format(order_status))
                # break
                if order_status !=22:
                    logger.warning(f'订单审核未通过，当前订单状态未:{order_status},5s后获取最新状态')
                    time.sleep(5)
                else:
                    with allure.step("订单审核通过确认放款"):
                        res=api.get_product()
                        res_json=res.json()
                        product_list=res_json['data']['products']
                        logger.info('获取产品结果:{}'.format(product_list))
                        assert res_json.get('code') == 200
                        if product_list:
                            max_product = max(product_list, key=lambda x: x.get('maxAmount', 0))
                            logger.info('max product: {}'.format(max_product))
                            res=api.payout(productId=max_product['productId'])
                            res_json=res.json()
                            assert res_json.get('code')==200
                            logger.info('放款成功')
                            break
                    



        

        
        