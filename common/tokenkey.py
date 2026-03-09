import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGD9Fd0XlON8JSQNiqgtCI5TsGaHJOBmSVCVEJP7IhDq6jDON4sB++mTRJuPyIrw/47ath6Ln7k6TLCQUQbvgZkh2H2WP5aH1U2wGrN4RgZcMJtO/OPkg0fgxc83WTSe66mEO4wj7bfgJZN1xayo3vOvsNSQ5pqLZ/0LEBxvzaBQIDAQAB
-----END PUBLIC KEY-----"""

def get_token_key(params=None):
    if params is None:
        from common.collect_data import get_collect_params
        params = get_collect_params()

    data = {
        "RequestId": params.get("RequestId"),
        "MobDeviceId": params.get("MobDeviceId"),
        "SDKSource": params.get("SDKSource"),
        "SDKVersion": params.get("SDKVersion"),
        "DataVersion": params.get("DataVersion"),
        "PackageName": params.get("PackageName"),
        "Partner": params.get("Partner"),
        "DeviceTime": params.get("DeviceTime"),
        "OSType": params.get("OSType"),
        "OSVersion": params.get("OSVersion"),
        "IMEI": params.get("IMEI"),
        "GAID": params.get("GAID"),
        "SdkPublicIp": params.get("SdkPublicIp"),
        "PackageCode": params.get("PackageCode"),
        "PackageVersion": params.get("PackageVersion"),
        "ActionMode": params.get("ActionMode"),
        "DrmId": params.get("Device", {}).get("drmId")
    }

    return rsa_base_data(data)

def rsa_base_data(data):
    try:
        json_str = json.dumps(data)
        data_bytes = json_str.encode('utf-8')
        print(f"DEBUG TOKENKEY: Length of data to encrypt: {len(data_bytes)}")
        
        if "YOUR_RSA_PUBLIC_KEY" in RSA_PUBLIC_KEY:
            print("Warning: RSA Public Key is missing. Returning placeholder.")
            return "MISSING_PUBLIC_KEY"
        key = RSA.importKey(RSA_PUBLIC_KEY)
        cipher = PKCS1_v1_5.new(key)
        
        MAX_BLOCK_SIZE = 117
        encrypted_bytes = b""
        for i in range(0, len(data_bytes), MAX_BLOCK_SIZE):
            chunk = data_bytes[i:i + MAX_BLOCK_SIZE]
            encrypted_bytes += cipher.encrypt(chunk)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        print(f"TokenKey Generation Error: {e}")
        import traceback
        traceback.print_exc()
        return ""
