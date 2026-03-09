import pytest
import allure
from common import common_params
from common.logger import logger
import random
import os
import time
from common import collect_data
from common.id_utils import CUITUtil, CBUUtil
def get_rut():
    rut = "" + "".join([str(random.randint(0, 9)) for _ in range(8)])
    return rut
@allure.feature("更新用户信息")
class TestUpdateUserInfo:
    def generate_mobile(self):
        first_digit = str(random.randint(1, 8))
        other_digits = "".join([str(random.randint(0, 9)) for _ in range(9)])
        suffix = first_digit + other_digits
        return suffix
    
    @allure.story("更新用户信息全流程")
    def test_update_user_info_flow(self, api):
        while True:
            current_step = common_params.get_current_step()
            logger.info(f"当前步骤为: {current_step}")
            if current_step == 1:
                self._update_user_work_info(api)
            elif current_step == 2:
                self._update_user_contact_info(api)
            elif current_step == 3:
                self._update_user_identity_info(api)
            elif current_step == 4:
                self._update_user_bank_info(api)
            else:
                logger.info(f"所有步骤已执行完毕，跳出循环。当前步骤: {current_step}")
                break

    @allure.story("更新用户工作信息")
    def _update_user_work_info(self, api):
        with allure.step("更新用户基本工作信息"):
            res = api.update_user_info(
                base={
                    "residentProvince": "hhh",
                    "residentCity": "hhh",
                    "residentAddress": "hhh",
                    "monthlyIncome": 1,
                    "education": 2,
                    "email": "hhh@qq.com",
                    "postCode": "1231",
                    "maritalStatus": 3,
                    "jobType": 2,
                    "pep": 0,
                    "pepReason": "",
                    "edited": True
                }
            )
            res_json = res.json()
            assert res_json.get('code') == 200
            common_params.set_current_step(res_json.get('data').get('nextStep'))
    
    @allure.story("更新用户联系人信息")
    def _update_user_contact_info(self, api):
        mobile1 = self.generate_mobile()
        mobile2 = self.generate_mobile()
        with allure.step("更新用户联系人信息"):
            res = api.update_user_info(
                contact={
                    "contact1": mobile1,
                    "contact2": mobile2,
                    "relationship1": 3,
                    "relationship2": 2,
                    "contact1Name": "test1",
                    "contact2Name": "test2"
                }
            )
            res_json = res.json()
            assert res_json.get('code') == 200
            common_params.set_current_step(res_json.get('data').get('nextStep'))

    @allure.story("更新用户身份信息")
    def _update_user_identity_info(self, api):
        with allure.step("更新用户身份信息"):
            # 身份证上传识别
            image_path_front = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'common', 'images', 'front.jpg')
            image_path_back = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'common', 'images', 'back.jpg')
            res_front=api.ocr_upload(
                card_type="front",
                ocr_file_path=image_path_front
            )
            res_back=api.ocr_upload(
                card_type="back",
                ocr_file_path=image_path_back
            )
            res_json_front = res_front.json()
            res_json_back = res_back.json()
            data=res_json_front['data']
            gender=data['gender']
            first_name=data['firstName']
            last_name=data['lastName']
            middle_name=data['middleName']
            birthday=data['dateOfBirth']
            identity=get_rut()
            id_photo_id=data['idPhotoId']
            id_photo_url=data['idPhotoUrl']
            id_photo_back_id=res_json_back['data']['idPhotoId']
            id_photo_back_url=res_json_back['data']['idPhotoUrl']
            id_issue_date=data['idIssueDate']
            id_expire_date=data['idExpireDate']
            nationality=data['nationality']
            country_of_birth=data['countryOfBirth']
            place_of_birth=res_json_back['data']['placeOfBirth']
            assert res_json_front.get('code') == 200
            logger.info("ocr front data :{}".format(res_json_front.get('data')))
            assert res_json_back.get('code') == 200
            logger.info("ocr back data :{}".format(res_json_back.get('data')))
            res = api.update_user_info(
                identity={
                    "gender":gender or 1,
                    "firstName":first_name or "defaultFirstName",
                    "lastName":last_name or "defaultLastName",
                    "middleName":middle_name or "defaultMiddleName",
                    "dateOfBirth":birthday or 977281200000,
                    "identity":identity,
                    "idPhotoId":id_photo_id,
                    "idPhotoUrl":id_photo_url,
                    "idPhotoBackId":id_photo_back_id,
                    "idPhotoBackUrl":id_photo_back_url,
                    "taxId":CUITUtil.generate_cuit(),
                    "idIssueDate":id_issue_date,
                    "idExpireDate":id_expire_date,
                    "nationality":nationality or "Argentina",
                    "countryOfBirth":country_of_birth or "Argentina",
                    "placeOfBirth":place_of_birth or "PROV. DE BUENOS AIRES"
                }
    
            )
            res_json = res.json()
            assert res_json.get('code') == 200
            common_params.set_current_step(res_json.get('data').get('nextStep'))
    
    @allure.story("更新用户银行信息")
    def _update_user_bank_info(self, api):
        with allure.step("更新用户银行信息"):
            # 获取银行列表
            res=api.get_bank_list()
            res_json = res.json()
            assert res_json.get('code') == 200
            bank_list=res_json['data']
            # logger.info("bank list :{}".format(bank_list))


            bank=bank_list[random.randint(0,len(bank_list)-1)]
            logger.info("bank :{}".format(bank))
            res = api.update_user_info(
              
              card={
                "bankName":bank['bankName'],
                "bankNoType":1,
                "bankCode":bank['bankCode'],
                "bankNo":CBUUtil.generate_cbu()
              }
            )
            res_json = res.json()
            assert res_json.get('code') == 200
            common_params.set_current_step(res_json.get('data').get('nextStep'))
            #进行大数据上报
            res=api.collect(action_mode="INFO")
            res_json = res.json()
            assert res_json.get('code') == 200  
   