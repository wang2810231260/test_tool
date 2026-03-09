import allure
from common.logger import logger
import pytest
from common.common_params import get_current_step
from common.tokenkey import get_token_key
from common.collect_data import get_collect_params

@allure.feature("订单申请模块")
class TestOrderApply:
    @allure.story("申请订单")
    def test_apply_order(self, api):
        res=api.get_loan_info()
        res_json = res.json()
        assert res_json.get('code') == 200  
        current_step=res_json['data']['nextStep'] 
        logger.info('当前步骤:{}'.format(current_step))
        # current_step=get_current_step()
        if current_step !=0:
            pytest.skip(f"跳过改测试用例，当前步骤为{current_step}, 预期步骤为0")
        with allure.step("申请订单,同时大数据上报"):
                collect_data = get_collect_params(action_mode='ORDER')
                res=api.collect(params=collect_data)
                res_json = res.json()
                token_key=res_json['data']['tokenKey']
                logger.info('大数据上报结果:{}'.format(res_json['data']))
                assert res_json.get('code') == 200
                res=api.get_product()
                res_json=res.json()
                product_list=res_json['data']['products']
                logger.info('获取产品结果:{}'.format(product_list))
                assert res_json.get('code') == 200
                if product_list:
                    max_product = max(product_list, key=lambda x: x.get('maxAmount', 0))
                    logger.info('max product: {}'.format(max_product))
                res = api.apply_order(token_key,loanAmount=int(max_product['maxAmount']),productId=max_product['productId'])
                res_json = res.json()
                logger.info('申请订单结果:{}'.format(res_json))
                assert res_json.get('code') == 200
                with allure.step("申请订单成功，获取最新订单状态"):
                        re=api.get_loan_info()
                        re_json=re.json()
                        assert re_json.get('code') == 200
                        order_status=re_json['data']
                        logger.info('获取最新订单状态结果:{}'.format(order_status))

                        
                      
           