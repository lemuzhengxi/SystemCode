import requests
import multiprocessing
multiprocessing.set_start_method('spawn')  # Windows兼容设置
from bs4 import BeautifulSoup
from src.robots_checker import RobotsChecker
from src.proxy_manager import ProxyManager
from src.config.system_config import SystemConfig
import socket
import time
import threading
import psutil

class CrawlerNode:
    def __init__(self):
        multiprocessing.freeze_support()  # Windows打包支持
        self.robots_checker = RobotsChecker()
        self.proxy_manager = ProxyManager()
        self.node_id = None
        self.master_url = f"http://{SystemConfig.MASTER_HOST}:{SystemConfig.MASTER_PORT}"
        self._register_with_master()
        self._start_heartbeat()
        
    def start(self):
        """启动爬虫节点"""
        pool = multiprocessing.Pool(processes=SystemConfig.MAX_WORKERS)
        while True:
            # 从Master获取任务
            urls = self._get_task_from_master()
            if urls:
                pool.map(self.crawl_url, urls)
                
    def crawl_url(self, url):
        """爬取单个URL"""
        retry_count = 0
        max_retries = SystemConfig.MAX_RETRIES
        
        while retry_count < max_retries:
            try:
                if not self.robots_checker.can_fetch(url):
                    return
                    
                proxy = self.proxy_manager.get_proxy()
                response = requests.get(url, proxies=proxy, timeout=SystemConfig.REQUEST_TIMEOUT)
                
                if response.status_code == 200:
                    data = self._parse_page(response.text)
                    self._store_data(data)
                    return
                    
            except Exception as e:
                retry_count += 1
                print(f"Error crawling {url} (attempt {retry_count}/{max_retries}): {str(e)}")
                time.sleep(SystemConfig.RETRY_DELAY)
        
        # 所有重试都失败后
        self._handle_failed_url(url)
            
    def _parse_page(self, html):
        """解析页面内容"""
        soup = BeautifulSoup(html, 'html.parser')
        # 实现页面解析逻辑
        return parsed_data 

    def _get_task_from_master(self):
        """从Master节点获取任务"""
        try:
            response = requests.get(f"{self.master_url}/task/get", params={'node_id': self.node_id})
            if response.status_code == 200:
                return response.json().get('urls', [])
        except Exception as e:
            print(f"获取任务失败: {str(e)}")
        return []

    def _store_data(self, data):
        """存储数据并向Master报告结果"""
        try:
            # 存储数据
            self.data_storage.store_data(data)
            
            # 报告结果
            requests.post(
                f"{self.master_url}/submit_result",
                json={'status': 'success', 'url': data['url']}
            )
        except Exception as e:
            print(f"存储数据失败: {str(e)}") 

    def _register_with_master(self):
        """向Master注册节点"""
        node_info = {
            'hostname': socket.gethostname(),
            'ip': socket.gethostbyname(socket.gethostname()),
            'capacity': self._get_node_capacity()
        }
        response = requests.post(f"{self.master_url}/node/register", json=node_info)
        self.node_id = response.json()['node_id']
        
    def _start_heartbeat(self):
        """启动心跳线程"""
        def send_heartbeat():
            while True:
                try:
                    requests.post(f"{self.master_url}/node/heartbeat", 
                                json={'node_id': self.node_id})
                except Exception as e:
                    print(f"心跳发送失败: {str(e)}")
                time.sleep(30)
                
        thread = threading.Thread(target=send_heartbeat)
        thread.daemon = True
        thread.start() 

    def _get_node_capacity(self):
        """计算节点当前容量"""
        # 获取系统资源使用情况
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        
        # 根据资源使用情况计算可用容量
        base_capacity = SystemConfig.MAX_WORKERS
        cpu_factor = (100 - cpu_percent) / 100
        memory_factor = (100 - memory_percent) / 100
        
        # 返回调整后的容量
        return int(base_capacity * min(cpu_factor, memory_factor))
