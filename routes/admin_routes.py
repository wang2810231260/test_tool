from flask import Blueprint, request, json
from common.db_util import DBUtils
from common.redis_util import RedisUtils
import time
from common.callback import payout_callback,payment_callback
import requests
from common import common_params


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/order_invalid', methods=['GET'])
def order_invalid():
    mobile = request.args.get('mobile')
    mobile='+54'+mobile
    app = request.args.get('app')
    if not mobile:
        return json.dumps({"code": 400, "msg": "手机号不能为空"})
    db = DBUtils()
    try:
        user = db.select_one('get_userId_by_mobile_and_sys_code', (mobile,app))
        if not user:
            return json.dumps({"code": 404, "msg": "用户不存在"})
        user_id = user['id']    
        db.execute_db('invalid_order_by_userId', (user_id,))
        return json.dumps({"code": 200, "msg": "订单已置为失效"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()

@admin_bp.route('/liveness_invalid', methods=['GET'])
def liveness_invalid():
    mobile = request.args.get('mobile')
    app=request.args.get('app')
    if not mobile:
        return json.dumps({"code": 400, "msg": "手机号不能为空"})
    mobile='+54'+mobile

    db = DBUtils()
    try:
        user = db.select_one('get_userId_by_mobile_and_sys_code', (mobile,app))
        if not user:
            return json.dumps({"code": 404, "msg": "用户不存在"})
        
        user_id = user['id']
        current_time=int(time.time() * 1000)
        liveness = db.select_all('get_liveness_by_userId', (user_id,current_time))
        if not liveness:
            return json.dumps({"code": 404, "msg": "活体不存在或当前活体已失效"})
        # liveness_id = liveness['id']
        for i in liveness:
            liveness_id = i['id']
            db.execute_db('invalid_liveness_by_userId', (liveness_id,))
        return json.dumps({"code": 200, "msg": "活体已置为失效"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()

@admin_bp.route('/order_invalid_to_pending', methods=['GET'])
def order_invalid_to_pending():
    mobile = request.args.get('mobile')
    mobile='+54'+mobile
    app = request.args.get('app')
    if not mobile:
        return json.dumps({"code": 400, "msg": "手机号不能为空"})
    db = DBUtils()
    try:
        user = db.select_one('get_userId_by_mobile_and_sys_code', (mobile,app))
        if not user:
            return json.dumps({"code": 404, "msg": "用户不存在"})
        user_id = user['id']
        order = db.select_one('get_order_by_userId', (user_id,))
        if not order:
            return json.dumps({"code": 404, "msg": "订单不存在"})
        order_id = order['id']
        db.execute_db('update_order_check_status', (order_id,))
        return json.dumps({"code": 200, "msg": "订单已置为审核中"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()
@admin_bp.route('/generate_payout', methods=['GET'])
def generate_payout():
    mobile = request.args.get('mobile')
    mobile='+54'+mobile
    app = request.args.get('app')
    status = request.args.get('status')
    if not mobile:
        return json.dumps({"code": 400, "msg": "手机号不能为空"})
    db = DBUtils()
    try:
        user = db.select_one('get_userId_by_mobile_and_sys_code', (mobile,app))
        if not user:
            return json.dumps({"code": 404, "msg": "用户不存在"})
        user_id = user['id']
        order = db.select_one('get_payout_order', (user_id,))
        if not order:
            return json.dumps({"code": 404, "msg": "不存在待放款订单"})
        order_id = order['id']
        # 查找放款流水
        payout_info = db.select_one('get_payout_info_by_order_id', (order_id,))
        if not payout_info:
            return json.dumps({"code": 404, "msg": "不存在放款流水"})
        order_no = payout_info['order_no']
        try:
            payout_callback(order_no,status)
            return json.dumps({"code": 200, "msg": "放款成功"})
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()

@admin_bp.route('/generate_payment', methods=['GET'])
def generate_payment():
    mobile = request.args.get('mobile')
    mobile='+54'+mobile
    app = request.args.get('app')
    status = request.args.get('status')
    if not mobile:
        return json.dumps({"code": 400, "msg": "手机号不能为空"})
    db = DBUtils()
    try:
        user = db.select_one('get_userId_by_mobile_and_sys_code', (mobile,app))
        if not user:
            return json.dumps({"code": 404, "msg": "用户不存在"})
        user_id = user['id']
        order = db.select_one('get_payment_order', (user_id,))
        if not order:
            return json.dumps({"code": 404, "msg": "不存在待还款订单"})
        order_id = order['id']
        # 查找还款流水
        payment_info = db.select_one('get_payment_info_by_order_id', (order_id,))
        if not payment_info:
            return json.dumps({"code": 404, "msg": "不存在还款流水"})
      
        order_no = payment_info['order_no']
        amount = int(payment_info['amount'])
        try:
            payment_callback(order_no,status,amount)
            return json.dumps({"code": 200, "msg": "还款成功"})
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()

@admin_bp.route('/get_product_list', methods=['GET'])
def get_product_list():
    mobile = request.args.get('mobile')
    mobile='+54'+mobile
    app = request.args.get('app')
    if not mobile:
        return json.dumps({"code": 400, "msg": "手机号不能为空"})
    db = DBUtils()
    try:
        user = db.select_one('get_userId_by_mobile_and_sys_code', (mobile,app))
        if not user:
            return json.dumps({"code": 404, "msg": "用户不存在"})
        user_id = user['id']
        product = db.select_all('get_product_by_userId', (user_id,))
        if not product:
            return json.dumps({"code": 404, "msg": "不存在产品"})
        return json.dumps({"code": 200, "msg": "产品列表", "data": product})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()   

@admin_bp.route('/update_product_list', methods=['GET'])
def update_product_list():
    mobile = request.args.get('mobile')
    mobile='+54'+mobile
    app = request.args.get('app')
    stage_info = request.args.get('stage_info')
    if not mobile:
        return json.dumps({"code": 400, "msg": "手机号不能为空"})
    db = DBUtils()
    try:
        user = db.select_one('get_userId_by_mobile_and_sys_code', (mobile,app))
        if not user:
            return json.dumps({"code": 404, "msg": "用户不存在"})
        user_id = user['id']
        db.execute_db('update_product_by_userId', (stage_info,user_id))
        return json.dumps({"code": 200, "msg": "产品列表更新成功"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close() 
@admin_bp.route('/get_coupon_template', methods=['GET'])
def get_coupon_template():
    current = request.args.get('current', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    token = common_params.get_admin_token()
    if token is None:
        return json.dumps({"code": 401, "msg": "token过期"})
    url = f"https://admin-api-test-arb.jinglewill.com/api/coupon?current={current}&size={size}"
    try:
        headers = {"Content-Type": "application/json","Authorization":f'{token}'}
        response = requests.get(url, timeout=10,headers=headers)
        return json.dumps({"code": 200, "msg": "获取优惠券模版成功", "data": response.json()})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
@admin_bp.route('/add_coupon', methods=['POST'])
def add_coupon():
    data = request.json
    data['couponType'] = str(data['couponType'])
    data['isAvailable']='1'
    data['validType']='1'
    # return data
    request_data={
        "appName":data['showName'],
        "couponType":data['couponType'],
        "distributeAmount":data['distributeAmount'],
        "distributeCount":data['count'],
        "validDays":data['validDays'],
        "sysCode":data['sysCode'],
        "isAvailable":data['isAvailable'],
        "validType":data['validType'],
        "name":data['name'],
    }
    
    print(request_data)
    token = common_params.get_admin_token()
    if token is None:
        return json.dumps({"code": 401, "msg": "token过期"})
    url = "https://admin-api-test-arb.jinglewill.com/api/coupon"
    try:
        headers = {"Content-Type": "application/json", "Authorization": f'{token}'}
        response = requests.post(url, json=request_data, timeout=10, headers=headers)
        
        # safely parse JSON
        try:
            resp_data = response.json()
        except Exception:
            resp_data = response.text

        # If HTTP status is not successful, we might want to return 500
        if response.status_code != 201:
            return json.dumps({"code": 500, "msg": f"接口请求失败: {response.status_code}", "data": resp_data})
            
        return json.dumps({"code": 200, "msg": "新增优惠券成功", "data": resp_data})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
@admin_bp.route('/delete_coupon', methods=['GET'])
def delete_coupon():
    id = request.args.get('id')
    token = common_params.get_admin_token()
    if token is None:
        return json.dumps({"code": 401, "msg": "token过期"})
    if not id:
        return json.dumps({"code": 400, "msg": "id不能为空"})
    db = DBUtils()
    try:
        db.execute_db('delete_coupon', (id,))
        return json.dumps({"code": 200, "msg": "删除优惠券成功"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()

@admin_bp.route('/edit_coupon', methods=['POST'])
def edit_coupon():
    data = request.json
    data['couponType'] = str(data['couponType'])
    data['isAvailable']='1'
    data['validType']='1'
    # return data
    request_data={
        "appName":data['showName'],
        "couponType":data['couponType'],
        "distributeAmount":data['distributeAmount'],
        "distributeCount":data['count'],
        "validDays":data['validDays'],
        "sysCode":data['sysCode'],
        "isAvailable":data['isAvailable'],
        "validType":data['validType'],
        "name":data['name'],
        "id":data['id'],
    }
    
    print(request_data)
    token = common_params.get_admin_token()
    if token is None:
        return json.dumps({"code": 401, "msg": "token过期"})
    url = "https://admin-api-test-arb.jinglewill.com/api/coupon"
    try:
        headers = {"Content-Type": "application/json", "Authorization": f'{token}'}
        response = requests.put(url, json=request_data, timeout=10, headers=headers)
        
        # safely parse JSON
        try:
            resp_data = response.json()
        except Exception:
            resp_data = response.text

        if response.status_code != 204:
            return json.dumps({"code": 500, "msg": resp_data['message'], "data": resp_data})
            
        return json.dumps({"code": 200, "msg": "编辑优惠券成功", "data": resp_data})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})

@admin_bp.route('/reset1',methods=['POST'])
def reset1():

    data=request.json
    app=data['app']
    mobile=data['mobile']
    mobile='+54'+mobile
    try:
        db=DBUtils()
        user=db.select_one("get_userId_by_mobile_and_sys_code",(mobile,app))
        if not user:
            return json.dumps({"code": 400, "msg": "用户不存在"})
        user_id=user['id']
        order=db.select_one("get_order_by_userId",(user_id,))
        if not order:
            return json.dumps({"code": 400, "msg": "用户不存在订单"})
        order_id=order['id']
        print(order_id)
        redis_client=RedisUtils()
        key=f'popup:applyAutoConfirm:orderId:{order_id}'
        get_key=redis_client.get(key)
        res=redis_client.delete(key)
        return json.dumps({"code": 200, "msg": "重置成功"})


    except Exception as e:

        return json.dumps({"code": 500, "msg": str(e)})

@admin_bp.route('/reset2',methods=['POST'])
def reset2():
    data=request.json
    app=data['app']
    mobile=data['mobile']
    mobile='+54'+mobile
    try:
        db=DBUtils()
        user=db.select_one("get_userId_by_mobile_and_sys_code",(mobile,app))
        if not user:
            return json.dumps({"code": 400, "msg": "用户不存在"})
        user_id=user['id']
        redis_client=RedisUtils()
        key=f'popup:page:accountId:{user_id}'
        redis_client.delete(key)
        db.execute_db("delete_popup_page",(user_id,))
        return json.dumps({"code": 200, "msg": "重置成功"})
    except Exception as e:

        return json.dumps({"code": 500, "msg": str(e)})
@admin_bp.route('/reset3',methods=['POST'])
def reset3():

    data=request.json
    app=data['app']
    mobile=data['mobile']
    mobile='+54'+mobile
    try:
        db=DBUtils()
        user=db.select_one("get_userId_by_mobile_and_sys_code",(mobile,app))
        if not user:
            return json.dumps({"code": 400, "msg": "用户不存在"})
        user_id=user['id']
        order=db.select_one("get_order_by_userId",(user_id,))
        if not order:
            return json.dumps({"code": 400, "msg": "用户不存在订单"})
        order_id=order['id']
        redis_client=RedisUtils()
        key=f'popup:waitConfirm:orderId:{order_id}'
        res=redis_client.delete(key)
        return json.dumps({"code": 200, "msg": "重置成功"})


    except Exception as e:

        return json.dumps({"code": 500, "msg": str(e)})

@admin_bp.route('/get_coupon_user',methods=['GET'])
def get_user_coupon():
    current = request.args.get('current', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    token = common_params.get_admin_token()
    if token is None:
        return json.dumps({"code": 401, "msg": "token过期"})
    url = f"https://admin-api-test-arb.jinglewill.com/api/accountCoupon?current={current}&size={size}"
    try:
        headers = {"Content-Type": "application/json","Authorization":f'{token}'}
        response = requests.get(url, timeout=10,headers=headers)
        return json.dumps({"code": 200, "msg": "获取用户优惠券成功", "data": response.json()})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
      
@admin_bp.route('/to_read',methods=['GET'])
def to_read():
    id = request.args.get('id')
    if not id:
        return json.dumps({"code": 400, "msg": "id不能为空"})
    db=DBUtils()
    try:
        db.execute_db("update_coupon_user",(id,))
        return json.dumps({"code": 200, "msg": "标记已读成功"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()
@admin_bp.route('/delete_coupon_user',methods=['GET'])
def delete_coupon_user():
    id = request.args.get('id')
    if not id:
        return json.dumps({"code": 400, "msg": "id不能为空"})
    db=DBUtils()
    try:
        db.execute_db("delete_coupon_user",(id,))
        return json.dumps({"code": 200, "msg": "删除成功"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
    finally:
        db.close()
@admin_bp.route('/get_coupon_list',methods=['GET'])
def get_coupon_list():
    sys_code=request.args.get('sysCode')
    if not sys_code:
        return json.dumps({"code":400,"msg":"sysCode不能为空"})
    token=common_params.get_admin_token()
    if not token:
        return json.dumps({"code":401,"msg":"token过期"})
    try:
        url=f"https://admin-api-test-arb.jinglewill.com/api/coupon/list?isAvailable=1&sysCode={sys_code}"
        headers = {"Content-Type": "application/json","Authorization":f'{token}'}
        response = requests.get(url, timeout=10,headers=headers)
        return json.dumps({"code": 200, "msg": "获取优惠券列表成功", "data": response.json()})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})
@admin_bp.route('/add_coupon_user',methods=['GET'])
def add_coupon_user():
    sys_code=request.args.get('sysCode')
    mobile=request.args.get('mobile')
    mobile="+54"+mobile
    coupon_id=request.args.get('couponId')
    db=DBUtils()
    user=db.select_one("get_userId_by_mobile_and_sys_code",(mobile,sys_code))
    if not user:
        return json.dumps({"code": 400, "msg": "用户不存在"})
    user_id=user['id']
    if not sys_code or not mobile or not coupon_id:
        return json.dumps({"code": 400, "msg": "参数不能为空"})
    token=common_params.get_admin_token()
    if not token:
        return json.dumps({"code": 401, "msg": "token过期"})
    data={
            "accountIds":str(user_id),
            "couponId":coupon_id,
            "sysCode":str(sys_code)
        }
    url=f"https://admin-api-test-arb.jinglewill.com/api/accountCoupon"
    try:
        headers = {"Content-Type": "application/json","Authorization":f'{token}'}
        response = requests.post(url, timeout=10,headers=headers,json=data)
        try:
            resp_data = response.json()
        except Exception:
            resp_data = response.text
        if response.status_code not in (200, 201):
            return json.dumps({"code": 500, "msg": f"接口请求失败: {response.status_code}", "data": resp_data})
        return json.dumps({"code": 200, "msg": "新增优惠券成功", "data": resp_data})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})

@admin_bp.route('/expired_coupon',methods=['GET'])
def expired_coupon():
    id=request.args.get('id')
    print(id)
    if not id:
        return json.dumps({"code": 400, "msg": "id不能为空"})
    db=DBUtils()
    try:
        db.execute_db("update_coupon_user_status",(id,))
        return json.dumps({"code": 200, "msg": "过期成功"})
    except Exception as e:
        return json.dumps({"code": 500, "msg": str(e)})