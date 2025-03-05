import socket
import dns.resolver
from functools import lru_cache

class DNSResolver:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 1
        self.resolver.lifetime = 1
        
    @lru_cache(maxsize=1000)
    def resolve(self, domain):
        """解析域名获取IP地址"""
        try:
            answers = self.resolver.resolve(domain, 'A')
            return [str(rdata) for rdata in answers]
        except Exception as e:
            print(f"DNS解析失败 {domain}: {str(e)}")
            return None
            
    def get_ip(self, url):
        """从URL获取IP地址"""
        domain = self._extract_domain(url)
        return self.resolve(domain) 