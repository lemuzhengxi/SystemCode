import time
from datetime import datetime

class CrawlerMonitor:
    def __init__(self):
        self.stats = {
            'start_time': None,
            'total_urls': 0,
            'success_urls': 0,
            'failed_urls': 0,
            'crawler_status': {}
        }
        
    def start_monitoring(self):
        """开始监控"""
        self.stats['start_time'] = datetime.now()
        
    def update_crawler_status(self, crawler_id, status):
        """更新爬虫状态"""
        self.stats['crawler_status'][crawler_id] = {
            'status': status,
            'last_update': datetime.now()
        }
        
    def get_statistics(self):
        """获取统计信息"""
        return {
            'uptime': (datetime.now() - self.stats['start_time']).seconds,
            'success_rate': self.stats['success_urls'] / self.stats['total_urls'] if self.stats['total_urls'] > 0 else 0,
            'active_crawlers': len([c for c in self.stats['crawler_status'].values() if c['status'] == 'active'])
        } 