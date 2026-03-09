import base64
import os
import requests
import json
import uuid
import hashlib
import time
import random
from common.tokenkey import get_token_key

def get_drm_id():
    try:
        random_bytes = os.urandom(32)
        encoded = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
        return encoded.strip()
    except Exception as e:
        print(f"Error generating drmId: {e}")
        return ""

def get_mob_device_info(drm_id):
    try:
        manufacturer = "vivo"
        brand = "vivo"
        board = "crow"
        serial_num = "unknown" 
        device = "PD2361"
        device_nickname = "V2361A"
        total_memory = "7620272128"
        total_internal = "256000000000"
        cpu_count = "8"
        
        device_info_str = f"{manufacturer}{brand}{board}{serial_num}{device}{device_nickname}{total_memory}{total_internal}{cpu_count}"
        sha256_hash = hashlib.sha256(device_info_str.encode('utf-8')).hexdigest()
        temp_id = sha256_hash[:16]
        
        source = temp_id + drm_id
        mob_device_id = hashlib.md5(source.encode('utf-8')).hexdigest().upper()
        
        info_list = [manufacturer, brand, board, serial_num, device, device_nickname, total_memory, total_internal, cpu_count]
        joined_str = ",".join(info_list)
        mob_device_meta = base64.b64encode(joined_str.encode('utf-8')).decode('utf-8')
        
        return mob_device_id, mob_device_meta
    except Exception as e:
        print(f"Error generating Mob info: {e}")
        return "", ""

def get_location_info():
    try:
        response = requests.get('http://ip-api.com/json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return str(data.get('lat')), str(data.get('lon'))
    except Exception as e:
        print(f"Error fetching location: {e}")
    return "39.927927927927925", "116.42302968397085" 

def get_collect_params(action_mode="INFO"):
    real_lat, real_lon = get_location_info()
    real_drm_id = get_drm_id()
    real_mob_id, real_mob_meta = get_mob_device_info(real_drm_id)
    time_now = int(time.time() * 1000)

    # Random generation logic
    battery_level = random.randint(10, 100)
    battery_max = random.choice([4000.0, 4500.0, 5000.0, 6000.0])
    battery_now = battery_max * (battery_level / 100.0)
    
    # 64GB, 128GB, 256GB, 512GB in bytes
    total_space = random.choice([64, 128, 256, 512]) * 1024 * 1024 * 1024
    used_space = int(total_space * random.uniform(0.1, 0.9))
    free_space = total_space - used_space
    
    # 4GB, 6GB, 8GB, 12GB, 16GB in bytes
    ram_size = random.choice([4, 6, 8, 12, 16]) * 1024 * 1024 * 1024
    ram_usable = int(ram_size * random.uniform(0.3, 0.7))

    collect_params = {
      "ActionMode": action_mode,
      "Battery": {
        "batteryLevel": battery_level,
        "batteryMax": battery_max,
        "batteryNow": battery_now,
        "batteryPowerLossNow": random.randint(-1000000, -10000),
        "chargeCounter": random.randint(100000, 5000000),
        "charging": random.choice([True, False]),
        "health": random.choice([1, 2, 3]),
        "icon": random.randint(10000000, 20000000),
        "plugged": random.choice([0, 1, 2]),
        "present": True,
        "scale": 100,
        "status": random.choice([2, 3, 4, 5]),
        "technology": "Li-ion",
        "temperature": random.randint(200, 400),
        "timeLeft": -1,
        "voltage": random.randint(3500, 4500)
      },
      "Calenders": [],
      "DataVersion": "25051200",
      "DataVersion": "25051200",
      "Device": {
        "accessibilityEnabled": "0",
        "airplaneMode": 0,
        "androidId": "",
        "bluetoothName": "",
        "bootTime": int(time_now - random.randint(1000000, 1000000000)),
        "dataRoaming": "1",
        "defaultInputMethod": "com.sohu.inputmethod.sogou.vivo/.SogouIME",
        "developmentSettingsEnabled": "1",
        "deviceNickName": "V2361A",
        "drmId": "t_dIeeWIIQXc8R7Z7lmtHRmdez4tYFBPNSdy8OggVXQ=",
        "elapsedRealtime": random.randint(1000000, 50000000),
        "isAuthSms": True,
        "isSimulator": False,
        "localeDisplayLanguage": "中文",
        "localeISO3Country": "CHN",
        "localeISO3Language": "zho",
        "mobileDbm": random.randint(-120, -60),
        "mockLocation": 0,
        "networkType": "4G",
        "screenOffTimeout": "600000",
        "touchExplorationEnabled": "0",
        "updateMills": random.randint(100000, 2000000),
        "usbDebug": True
      },
      "DeviceManufacturer": "vivo",
      "DeviceProduct": "PD2361",
      "DeviceTime": time_now,
      "DeviceType": "V2361A",
      "GAID": "c874e45e-834b-4ebd-8184-d1528b289335",
      "Hardware": {
        "board": "crow",
        "brand": "vivo",
        "cores": random.choice([4, 8]),
        "deviceHeight": str(random.choice([1920, 2185, 2340, 2400])),
        "deviceName": "V2361A",
        "deviceWidth": str(random.choice([720, 1080])),
        "model": "V2361A",
        "release": str(random.choice([11, 12, 13, 14])),
        "sdkVersion": str(random.choice([30, 31, 33, 34]))
      },
      "IMEI": "",
      "Ip": "172.22.40.125",
      "Latitude": real_lat,
      "LocationType": "fused",
      "Longitude": real_lon,
      "MobDeviceId": "FCBA00342248E8AE0C5F0CD9E65993FB",
      "MobDeviceMeta": "dml2byx2aXZvLGNyb3csdW5rbm93bixQRDIzNjEsVjIzNjFBLDc2MjAyNzIxMjgsMjU2MDAwMDAwMDAwLDg=",
      "OSType": "Android",
      "OSVersion": 34,
      "Package": [
      {
      "installTime": 16743435,
      "name": "vivo 短视频",
      "path": "/data/preload/com.kaixinkan.ugc.video/UgcVideo.apk",
      "pkg": "com.kaixinkan.ugc.video",
      "type": 0,
      "updateTime": 16743435,
      "version": "10.4.90.1"
      },
      { 
      "installTime": 1761894402591,
      "name": "RapiLuka",
      "path": "/data/app/~~728UGPN5Sc8fIjd1TffmgQ==/com.rapirapa.app.android-jNb2-Sv8CVZ5v1e5cd1MlQ==/base.apk",
      "pkg": "com.rapirapa.app.android",
      "type": 0,
      "updateTime": 1764836134255,
      "version": "1.0.17"
    }
      ],  
      "PackageCode": 1,
      "PackageName": "jg.cuenta.soles.app.dev",
      "PackageVersion": "1.0.1",
      "Partner": "",
      "RequestId": str(uuid.uuid4()),
      "Root": False,
      "SDKSource": "react-native-android-jg.cuenta.soles.app.dev",
      "SDKVersion": "3.0.0",
      "SdkPublicIp": "103.143.93.85",
      "Sms": [],
      "StorageInfo": {
        "appFreeMemory": 0,
        "appMaxMemory": 268435456,
        "appTotalMemory": 15644224,
        "containSd": 0,
        "extraSd": 0,
        "internalStorageTotal": total_space,
        "internalStorageUsable": free_space,
        "memoryCardFreeSize": free_space,
        "memoryCardSize": total_space,
        "memoryCardSizeUse": used_space,
        "memoryCardUsableSize": free_space,
        "ramTotalSize": ram_size,
        "ramUsableSize": ram_usable
      },
      "VPN": False,
      "Wifi": "",
      "WifiList": []
    }
    
    # collect_params["SDKVersions"] = get_token_key(collect_params)
    
    return collect_params
