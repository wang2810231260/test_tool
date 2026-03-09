import pytest
import os
import shutil

if __name__ == '__main__':
    pytest.main()
    os.system("allure generate ./reports/temp -o ./reports/html --clean")
