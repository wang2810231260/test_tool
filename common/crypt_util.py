import base64
import json
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class CryptUtil:
    def __init__(self, key_hex, iv_hex):
        self.key = binascii.unhexlify(key_hex)
        self.iv = binascii.unhexlify(iv_hex)
        self.mode = AES.MODE_CBC

    def encrypt(self, plain_text):
        if isinstance(plain_text, dict) or isinstance(plain_text, list):
            plain_text = json.dumps(plain_text)
        
        # New cipher instance for each operation for safety (CBC maintains state)
        cipher = AES.new(self.key, self.mode, self.iv)
        ct_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return ct

    def decrypt(self, cipher_text):
        if not cipher_text:
            return ""
        try:
            cipher = AES.new(self.key, self.mode, self.iv)
            ct_bytes = base64.b64decode(cipher_text)
            pt_bytes = unpad(cipher.decrypt(ct_bytes), AES.block_size)
            return pt_bytes.decode('utf-8')
        except Exception as e:
            # Handle decryption error gracefully or re-raise
            print(f"Decryption failed: {e}")
            return cipher_text
