import requests
from common.logger import logger
from common.crypt_util import CryptUtil
from common.yaml_util import yaml_util
from common.common_params import get_common_params
import os
import json
from urllib.parse import unquote

class RequestUtil:
    def __init__(self):
        self.session = requests.Session()
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        self.config = yaml_util.read_yaml(config_path)

    def send_request(self, method, url, **kwargs):
        method = str(method).lower()
        try:
            kwargs = self._pre_request(method, url, **kwargs)
            
            logger.info("Request Method: {}, URL: {}".format(method, url))
            if 'params' in kwargs:
                logger.info("Request Params: {}".format(kwargs['params']))
            if 'json' in kwargs:
                logger.info("Request Data (JSON): {}".format(kwargs['json']))
            if 'data' in kwargs:
                logger.info("Request Data (Form): {}".format(kwargs['data']))
            if 'files' in kwargs:
                 files_info = {k: str(v) for k, v in kwargs['files'].items()}
                
            res = self.session.request(method, url, **kwargs)
            
            self._post_request(res)
            
            logger.info("Response Status Code: {}".format(res.status_code))
            logger.debug("Response Text: {}".format(res.text))
            return res
        except Exception as e:
            logger.error("Request failed: {}".format(e))
            raise e

    def _pre_request(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})
        headers['User-Agent'] = 'Python-Interface-Test'
        # Collect sys_code: prioritizing common_params (which checks env for subprocesses)
        from common import common_params
        sys_code = common_params.get_current_sys_code() or self.config.get('sys_code')
        headers['SysCode'] = sys_code
        kwargs['headers'] = headers
        if method == "post":
            if 'json' not in kwargs and 'data' not in kwargs and 'files' not in kwargs:
                kwargs['json'] = {}
        
        if 'json' in kwargs:
             data = kwargs['json']
             
             common_data = get_common_params()
             if isinstance(data, dict):
                 common_data.update(data)
                 data = common_data
                #  logger.debug("Merged Request Data: {}".format(data))
             
             # if self.config.get('aes_key_hex') and self.config.get('aes_iv_hex'):
             #     key = self.config['aes_key_hex']
             #     iv = self.config['aes_iv_hex']
             #     crypt = CryptUtil(key, iv)
             #     encrypted_data = crypt.encrypt(data)
                 
             #     new_data = {
             #         "data": encrypted_data
             #     }
             #     kwargs['json'] = new_data
             # else:
             kwargs['json'] = data
        elif 'data' in kwargs:
            
             business_params = kwargs['data']
             
             all_params = get_common_params()
             if isinstance(business_params, dict):
                 all_params.update(business_params)
             
             # if self.config.get('aes_key_hex') and self.config.get('aes_iv_hex'):
             #     key = self.config['aes_key_hex']
             #     iv = self.config['aes_iv_hex']
             #     crypt = CryptUtil(key, iv)
             #     encrypted_data = crypt.encrypt(all_params)
                 
             #     kwargs['data']['data'] = encrypted_data
             #     logger.debug("Encrypted Form Data prepared: {}".format(kwargs['data']))
             # else:
             kwargs['data'] = all_params
             logger.debug("Merged Form Data (No Encryption): {}".format(kwargs['data']))

        return kwargs

    def _post_request(self, res):
        """
        Post-request interceptor: Handle response globally
        """
        try:
            pass
            # if self.config.get('aes_key_hex') and self.config.get('aes_iv_hex'):
            #      key = self.config['aes_key_hex']
            #      iv = self.config['aes_iv_hex']
            #      crypt = CryptUtil(key, iv)
                 
            #      # Check if response is JSON
            #      try:
            #          res_json = res.json()
            #          if isinstance(res_json, dict) and 'data' in res_json:
            #              encrypted_content = res_json['data']
                         
            #              if encrypted_content and isinstance(encrypted_content, str):
            #                  # URL decode the content first
            #                  encrypted_content = unquote(encrypted_content)
            #                  logger.info("Raw Response Data (Decoded): {}".format(encrypted_content))
                             
            #                  decrypted_content = crypt.decrypt(encrypted_content)
            #                  logger.info("Decrypted Response Data: {}".format(decrypted_content))
                             
            #                  # Try to parse decrypted content as JSON
            #                  try:
            #                      decrypted_json = json.loads(decrypted_content)
            #                      res_json['data'] = decrypted_json
            #                  except json.JSONDecodeError:
            #                      # If not JSON, just put string back
            #                      res_json['data'] = decrypted_content
                             
            #                  # Re-encapsulate: Update the response object so res.json() works with new data
            #                  # We need to set _content with bytes of the new json
            #                  res._content = json.dumps(res_json).encode('utf-8')
                             
            #      except ValueError:
            #          pass # Not JSON
        except Exception as e:
            logger.error("Response processing failed: {}".format(e))

request_util = RequestUtil()
