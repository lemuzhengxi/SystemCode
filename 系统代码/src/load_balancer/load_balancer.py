from collections import defaultdict

class LoadBalancer:
    def __init__(self):
        self.node_loads = defaultdict(int)
        self.strategies = {
            'least_connections': self._least_connections_strategy,
            'round_robin': self._round_robin_strategy,
            'weighted': self._weighted_strategy
        }
        self.current_strategy = 'least_connections'
        
    def get_tasks(self, node_capacity):
        """根据负载均衡策略分配任务"""
        return self.strategies[self.current_strategy](node_capacity)
        
    def _least_connections_strategy(self, node_capacity):
        """最小连接数策略"""
        min_load_node = min(self.node_loads.items(), key=lambda x: x[1])
        return self._allocate_tasks(min_load_node[0], node_capacity)
        
    def _weighted_strategy(self, node_capacity):
        """加权分配策略"""
        weights = self._calculate_weights()
        node_id = max(weights.items(), key=lambda x: x[1])[0]
        return self._allocate_tasks(node_id, node_capacity)
        
    def _calculate_weights(self):
        """计算节点权重"""
        weights = {}
        for node_id, load in self.node_loads.items():
            # 考虑CPU、内存、网络等资源
            node_stats = self._get_node_stats(node_id)
            weights[node_id] = self._weight_function(node_stats, load)
        return weights 

    def _round_robin_strategy(self, node_capacity):
        """轮询策略"""
        active_nodes = list(self.node_loads.keys())
        if not active_nodes:
            return []
        
        # 使用计数器实现轮询
        if not hasattr(self, '_counter'):
            self._counter = 0
        self._counter = (self._counter + 1) % len(active_nodes)
        
        selected_node = active_nodes[self._counter]
        return self._allocate_tasks(selected_node, node_capacity)

    def _allocate_tasks(self, node_id, capacity):
        """为节点分配任务"""
        from src.url_manager import URLManager
        url_manager = URLManager()
        
        # 根据节点容量获取合适数量的URL
        urls = url_manager.get_batch_urls(min(capacity, SystemConfig.URL_BATCH_SIZE))
        
        # 更新节点负载
        self.node_loads[node_id] += len(urls)
        return urls 