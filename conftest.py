import pytest
import os
from common.yaml_util import yaml_util
from apis.api_service import ApiService

@pytest.fixture(scope="session")
def api():
    """
    Fixture to initialize ApiService globally for the session.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    config = yaml_util.read_yaml(config_path)
    base_url = config['base_url']
    return ApiService(base_url)


def pytest_collection_modifyitems(session, config, items):
    """
    读取配置.
    """
    import os
    from common.yaml_util import yaml_util
    
    # If running from the web UI, skip the static config.yaml test_order filtering
    if os.environ.get('USE_WEB_ORDER') == '1':
        return
    
    
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    try:
        conf = yaml_util.read_yaml(config_path)
        test_order = conf.get('test_order', [])
    except Exception:
        test_order = []
        
    if not test_order:
        return
    order_map = {filename: i for i, filename in enumerate(test_order)}

# 过滤不存在配置
    items[:] = [item for item in items if os.path.basename(item.fspath) in order_map]
#根据过滤后的重新排序
    items.sort(key=lambda item: order_map.get(os.path.basename(item.fspath)))

def pytest_runtest_logstart(nodeid, location):
    """
    Hook to log the start of each test case with a special marker.
    This helps the web runner identify the currently running test.
    """
    print(f">>>CURRENT_CASE:::{nodeid}", flush=True)

