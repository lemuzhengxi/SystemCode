import time
from datetime import datetime
import threading

class NodeManager:
    def __init__(self):
        import os
        self.nodes = {}  # 存储所有节点信息
        self.node_lock = threading.Lock()
        
        # Windows服务检测
        if os.name == 'nt':
            self._check_windows_services()
            
        self._start_health_check()

    def _check_windows_services(self):
        """检查Windows服务状态"""
        try:
            import win32serviceutil
            if not win32serviceutil.QueryServiceStatus('MongoDB')[1] == 4:
                raise Exception("MongoDB服务未运行")
            if not win32serviceutil.QueryServiceStatus('Redis')[1] == 4:
                raise Exception("Redis服务未运行")
        except Exception as e:
            print(f"Windows服务状态异常: {str(e)}")
            exit(1)
        
    def register_node(self, node_info):
        """注册新节点"""
        with self.node_lock:
            node_id = node_info['node_id']
            self.nodes[node_id] = {
                'info': node_info,
                'last_heartbeat': datetime.now(),
                'status': 'active'
            }
        return node_id
        
    def unregister_node(self, node_id):
        """注销节点"""
        with self.node_lock:
            if node_id in self.nodes:
                del self.nodes[node_id]
                
    def update_heartbeat(self, node_id):
        """更新节点心跳"""
        with self.node_lock:
            if node_id in self.nodes:
                self.nodes[node_id]['last_heartbeat'] = datetime.now()
                
    def get_active_nodes(self):
        """获取所有活动节点"""
        with self.node_lock:
            return {
                node_id: node_info
                for node_id, node_info in self.nodes.items()
                if node_info['status'] == 'active'
            }
            
    def _start_health_check(self):
        """启动健康检查线程"""
        def check_health():
            while True:
                self._check_nodes_health()
                time.sleep(30)  # 每30秒检查一次
                
        thread = threading.Thread(target=check_health)
        thread.daemon = True
        thread.start()
        
    def _check_nodes_health(self):
        """检查所有节点健康状态"""
        with self.node_lock:
            now = datetime.now()
            for node_id, node_info in self.nodes.items():
                if (now - node_info['last_heartbeat']).seconds > 60:  # 60秒无心跳视为离线
                    node_info['status'] = 'inactive'
