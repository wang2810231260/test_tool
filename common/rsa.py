import base64
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def encrypt_rsa(text):
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCz3dGZLjPiSnSj53A+slY4SXCcLiiBOTC88A8qZh9PMjnPVEeXCQA0G9Wp5aU2d6da10EDvo/MgKocwDaq2Xu1l/61G7PLVZUENcu/VCwoCuictMZdMyLHD/k8XP7lDWk1IMyn602wyStNWCJwc6MYJvJg9vHs1K3irgWpk5sRMQIDAQAB'
    key_der = base64.b64decode(public_key)
    rsa_key = RSA.import_key(key_der)
    cipher = PKCS1_v1_5.new(rsa_key)
    
    text_bytes = text.encode('utf-8')
    chunk_size = 117
    
    ct_hex = ""
    for i in range(0, len(text_bytes), chunk_size):
        chunk = text_bytes[i:i+chunk_size]
        encrypted_chunk = cipher.encrypt(chunk)
        hex_chunk = binascii.hexlify(encrypted_chunk).decode('utf-8')
        ct_hex += hex_chunk.zfill(256)
        
    return base64.b64encode(binascii.unhexlify(ct_hex)).decode('utf-8')