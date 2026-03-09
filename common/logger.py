import logging
import os
import time

class Logger:
    def __init__(self):
        self.log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
            
        self.log_name = os.path.join(self.log_path, '{}.log'.format(time.strftime('%Y_%m_%d')))
        
        self.logger = logging.getLogger('api_test')
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            # File handler
            fh = logging.FileHandler(self.log_name, encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

logger = Logger().get_logger()
