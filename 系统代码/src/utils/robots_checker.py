import urllib.robotparser

class RobotsChecker:
    def __init__(self):
        import os
        self.rp = urllib.robotparser.RobotFileParser()
        self.robots_cache = {}
        # Windows兼容的缓存目录配置
        self.cache_dir = os.path.join("data", "robots_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def can_fetch(self, url):
        """检查是否可以爬取该URL"""
        domain = self._get_domain(url)
        if domain not in self.robots_cache:
            self.rp.set_url(f"{domain}/robots.txt")
            self.rp.read()
            self.robots_cache[domain] = self.rp
            
        return self.robots_cache[domain].can_fetch("*", url)
