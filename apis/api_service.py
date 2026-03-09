from apis.base_api import BaseApi
import os
import json
from common.collect_data import get_collect_params

class ApiService(BaseApi):
    # --- Login API Methods ---
    # 发送验证码
    def send_sms_code(self, mobile, sms_type="8"):
        """
        Send SMS Code
        """
        json_data = {
            "mobile": mobile,
            "codeType": sms_type
        }
        return self.request("post", "/api/v1/user/getVerifyCode", json=json_data)
# 登录
    def login_by_sms(self, mobile, auth_code="8888"):
        """
        Login by SMS
        """
        json_data = {
            "mobile": mobile,
            "code": auth_code
        }
        return self.request("post", "/api/v1/user/login", json=json_data)
# 获取用户订单状态
    def get_loan_info(self):
        """
        Get Loan Info
        """
        return self.request("post", "/api/v1/order/home")
    # 获取产品列表
    def get_product(self):
        """
        Get Product
        """
        return self.request("post", "/api/v1/order/product")
        # 创建订单
    def create_order(self,product_id,loan,period):
        """
        Create Order
        """
        json_data = {
            "product_id": product_id,
            "loan": loan,
            "period": period
        }
        return self.request("post", "/app/ApiService/api/vj1/orders/createOrders", json=json_data)
    #更新用户个人信息
    def update_user_info(self, **kwargs):
        """
        Update User Personal Info
        """
        return self.request("post", "/api/v1/account/info/update",json=kwargs)

    # 获取银行列表接口
    def get_bank_list(self):
        return self.request("post", "/api/v1/account/bankList")

# ocr识别上传 
    def ocr_upload(self, card_type, ocr_file_path):
        """
        Ocr Upload
        """
        import mimetypes
        import base64
        
        filename = os.path.basename(ocr_file_path)
        with open(ocr_file_path, "rb") as f:
            file_content = f.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')

        json_data = {
            "card_type": card_type,
            "imageBase64": base64_content
        }
        return self.request("post", "/api/v1/account/idCardOcr", json=json_data)

    # 用户上传活体
    def update_user_liveness_info(self, liveness_file_path):
        """
        Update User Liveness Info
        """
        import mimetypes
        import base64
        
        filename = os.path.basename(liveness_file_path)
        with open(liveness_file_path, "rb") as f:
            file_content = f.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')

        json_data = {
            "imageBase64": base64_content
        }
        return self.request("post", "/api/v1/account/live", json=json_data)
    #订单申请
    def apply_order(self,token_key,loanAmount,productId):
        """
        apply order
        """
        json_data = {
            "tokenKey": token_key,
            "loanAmount": loanAmount,
            "productId": productId,
        }
        return self.request("post", "/api/v1/order/apply", json=json_data)

    #大数据上报 
    def collect(self, action_mode="INFO", params=None):
        """
         collect
        """
        if params is None:
            params = get_collect_params(action_mode)
            
        json_data = {
            "type": 1,
            "deviceInfo": json.dumps(params)
        }
        return self.request("post", "/api/v1/common/collect", json=json_data)
    # 确认放款
    def payout(self,productId):
        """
        payout
        """
        json_data={
            "productId":productId
            
        }
        return self.request("post","/api/v1/order/confirmLoan",json=json_data)

    def paymentInfo(self):
        """
        paymentInfo
        """
        return self.request("post","/api/v1/payment/payment/info" )
    def paymentType(self,amount):
        """
        paymentType
        """
        json_data={
            "amount":amount
        }
        return self.request("post","/app/ApiService/api/vj1/payment/payTypeListForNewApp",json=json_data)
    
    def createPayment(self,amount,channel):
        """
        createPayment
        """
        json_data={
            "amount":amount,
            "channel":channel
            
        }
        return self.request("post","/api/v1/payment/payment/apply",json=json_data)



