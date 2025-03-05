from src.config.system_config import SystemConfig
from src.url_manager import URLManager

class TaskDispatcher:
    def __init__(self):
        self.url_manager = URLManager()
        self.current_strategy = "round_robin"  # 默认使用轮询策略
        
    def dispatch_urls(self):
        """根据当前策略分发URL"""
        if self.current_strategy == "round_robin":
            return self._round_robin_dispatch()
        elif self.current_strategy == "domain_based":
            return self._domain_based_dispatch()
            
    def _round_robin_dispatch(self):
        """轮询分发策略"""
        return self.url_manager.get_batch_urls(SystemConfig.URL_BATCH_SIZE)
        
    def _domain_based_dispatch(self):
        """基于域名的分发策略"""
        urls = self.url_manager.get_batch_urls(SystemConfig.URL_BATCH_SIZE)
        # 按域名分组URL
        return self._group_by_domain(urls) 