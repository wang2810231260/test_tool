import yaml
import os

class YamlUtil:
    def read_yaml(self, file_path):
        """
        Read yaml file
        :param file_path:
        :return: dict
        """
        if not os.path.exists(file_path):
            return None
        with open(file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data

yaml_util = YamlUtil()
