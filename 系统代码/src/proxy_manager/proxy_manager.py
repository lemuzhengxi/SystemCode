import requests
import random
from src.config.system_config import SystemConfig

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.update_interval = 300  # 5分钟更新一次代理池
        
    def get_proxy(self):
        """获取一个代理"""
        if not self.proxies:
            self._update_proxy_pool()
        return random.choice(self.proxies) if self.proxies else None
        
    def _update_proxy_pool(self):
        """更新代理池"""
        try:
            response = requests.get(SystemConfig.PROXY_POOL_URL)
            if response.status_code == 200:
                self.proxies = response.json()
        except Exception as e:
            print(f"更新代理池失败: {str(e)}") 