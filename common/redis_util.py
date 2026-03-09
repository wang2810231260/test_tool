import redis
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.logger import logger
from common.yaml_util import yaml_util

class RedisUtils:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(root_path, 'config', 'config.yaml')
            config = yaml_util.read_yaml(config_path)
            if not config or 'redis' not in config:
                logger.error("config.yaml 中未找到 Redis 配置文件")
                raise Exception("Redis configuration missing")
            
            redis_conf = config['redis']
            
            self.conn = redis.Redis(
                host=redis_conf.get('host', '127.0.0.1'),
                port=redis_conf.get('port', 6379),
                password=redis_conf.get('password', None) or None,
                db=redis_conf.get('db', 0),
                decode_responses=True # Automatically decode string responses back to Python strings
            )
            
            # Ping to verify connection
            if self.conn.ping():
                logger.info("Redis连接成功.")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            raise e

    def set(self, key, value, ex=None):
        """Set a value in Redis with an optional expiration in seconds"""
        try:
            result = self.conn.set(key, value, ex=ex)
            logger.info(f"Redis SET - key: {key}")
            return result
        except Exception as e:
            logger.error(f"Redis SET 失败 - key: {key}, error: {e}")
            return None

    def get(self, key):
        """Get a value by key from Redis"""
        try:
            result = self.conn.get(key)
            logger.info(f"Redis GET - key: {key}")
            return result
        except Exception as e:
            logger.error(f"Redis GET 失败 - key: {key}, error: {e}")
            return None

    def delete(self, *keys):
        """Delete one or more keys from Redis"""
        try:
            result = self.conn.delete(*keys)
            logger.info(f"Redis DELETE - keys: {keys}")
            return result
        except Exception as e:
            logger.error(f"Redis DELETE 失败 - keys: {keys}, error: {e}")
            return 0

    def keys(self, pattern="*"):
        """Search keys containing a string"""
        try:
            result = self.conn.keys(pattern)
            return result
        except Exception as e:
            logger.error(f"Redis KEYS 失败 - pattern: {pattern}, error: {e}")
            return []

    def close(self):
        try:
            if self.conn:
                self.conn.close()
                logger.info("Redis连接已关闭.")
        except Exception as e:
            logger.error(f"关闭Redis连接失败: {e}")
