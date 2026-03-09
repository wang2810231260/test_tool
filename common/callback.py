import requests
import json
import uuid
from common.logger import logger
from common import common_params

def payout_callback(order_no,status):
    """
    """
    if not order_no:
        logger.warning("Callback: No result list provided.")
        return

    url = "https://admin-api-test-arb.jinglewill.com/api/testTool/payoutCallback"
    token = common_params.get_admin_token() 
    payload = { 
        "orderNo": order_no,
        "status":status
    }
    logger.info(f"Sending Payout Callback for {order_no}. Payload: {json.dumps(payload)},url:{url}")
    try:
        headers = {"Content-Type": "application/json","Authorization":f'{token}'}
        logger.info(f"Callback Headers: {json.dumps(headers)}")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            logger.error(f"Callback Request Failed: {response.status_code} - {response.text}")
        logger.info(f"Callback Response: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Callback Request Failed: {e}")
def payment_callback(order_no,status,amount):
    """
    """
    if not order_no:
        logger.warning("Callback: No result list provided.")
        return

    url = "https://admin-api-test-arb.jinglewill.com/api/testTool/paymentCallback"
    token = common_params.get_admin_token()
    payload = { 
        "amount": amount,
        "orderNo": order_no,
        "status":status
    }   
    logger.info(f"Sending payment Callback for {order_no}. Payload: {json.dumps(payload)}")
    try:
        headers = {"Content-Type": "application/json","Authorization":f'{token}'}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            logger.error(f"Callback Request Failed: {response.status_code} - {response.text}")
        logger.info(f"Callback Response: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Callback Request Failed: {e}")

        payload = {
            "amount": amount_str,
            "orderNo": order_no,
            "status":"SUCCESS"
        }
        logger.info(f"Sending payment Callback for {order_no}. Payload: {json.dumps(payload)}")
        try:
            headers = {"Content-Type": "application/json","Authorization":f'{token}'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code != 200:
                logger.error(f"Callback Request Failed: {response.status_code} - {response.text}")
            logger.info(f"Callback Response: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Callback Request Failed: {e}")   

