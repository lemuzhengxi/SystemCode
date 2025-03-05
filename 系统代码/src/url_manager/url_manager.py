import redis
from src.config.system_config import SystemConfig

class URLManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=SystemConfig.REDIS_HOST,
            port=SystemConfig.REDIS_PORT
        )
        
    def add_url(self, url):
        """添加新URL到待爬取队列"""
        if not self._is_duplicate(url):
            self.redis_client.sadd("pending_urls", url)
            
    def get_batch_urls(self, batch_size=100):
        """获取一批待爬取的URL"""
        urls = []
        for _ in range(batch_size):
            url = self.redis_client.spop("pending_urls")
            if url:
                urls.append(url.decode())
        return urls
        
    def _is_duplicate(self, url):
        """检查URL是否已经被爬取过"""
        return self.redis_client.sismember("crawled_urls", url) 