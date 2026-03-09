import pymysql
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.logger import logger
from common.yaml_util import yaml_util

class DBUtils:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.sqls = self.load_sqls()
        self.connect()

    def load_sqls(self):
        """sql文件是否存在"""
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sql_path = os.path.join(root_path, 'config', 'sqls.yaml')
        return yaml_util.read_yaml(sql_path) or {}

    def get_sql(self, sql_key_or_statement):
        """
        查找sql
        """
        if sql_key_or_statement in self.sqls:
            return self.sqls[sql_key_or_statement]
        return sql_key_or_statement

    def connect(self):
        try:
            root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(root_path, 'config', 'config.yaml')
            config = yaml_util.read_yaml(config_path)
            if not config or 'db' not in config:
                logger.error("config.yaml 中未找到配置文件")
                raise Exception("Database configuration missing")
            
            db_conf = config['db']
            
            self.conn = pymysql.connect(
                host=db_conf['host'],
                port=db_conf['port'],
                user=db_conf['user'],
                password=db_conf['password'],
                database=db_conf['database'],
                charset=db_conf['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
            logger.info("数据库连接成功.")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise e
# 支持增，删，查
    def execute_db(self, sql, args=None):
        try:
            sql = self.get_sql(sql)
            result = self.cursor.execute(sql, args)
            self.conn.commit()
            real_sql = self.cursor.mogrify(sql,args)            
            logger.info(f'sql执行记录:{real_sql}')
            return result
        except Exception as e:
            logger.error(f"执行SQL失败: {sql}, error: {e}")
            self.conn.rollback()
            return None

    def select_one(self, sql, args=None):
        try:
            sql = self.get_sql(sql)
            self.conn.commit()  # Ensure we get fresh data instead of cached snapshot
            self.cursor.execute(sql, args)
            real_sql = self.cursor.mogrify(sql,args)            
            logger.info(f'sql执行记录:{real_sql}')
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"查询单条记录失败: {sql}, error: {e}")
            return None
    def select_all(self, sql, args=None):
        try:
            sql = self.get_sql(sql)
            self.conn.commit()  # Ensure we get fresh data instead of cached snapshot
            self.cursor.execute(sql, args)
            real_sql = self.cursor.mogrify(sql,args)            
            logger.info(f'sql执行记录:{real_sql}')
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"查询多条记录失败: {sql}, error: {e}")
            return None

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            logger.info("数据库连接已关闭.")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

