from flask import Flask, jsonify, request
from src.node_manager import NodeManager
from src.load_balancer import LoadBalancer
from src.url_manager import URLManager

class MasterNode:
    def __init__(self):
        self.app = Flask(__name__)
        self.node_manager = NodeManager()
        self.load_balancer = LoadBalancer()
        self.url_manager = URLManager()
        self._setup_routes()
        
    def _setup_routes(self):
        # 节点管理接口
        @self.app.route('/node/register', methods=['POST'])
        def register_node():
            node_info = request.json
            node_id = self.node_manager.register_node(node_info)
            return jsonify({'node_id': node_id})
            
        @self.app.route('/node/heartbeat', methods=['POST'])
        def heartbeat():
            node_id = request.json['node_id']
            self.node_manager.update_heartbeat(node_id)
            return jsonify({'status': 'ok'})
            
        @self.app.route('/node/unregister', methods=['POST'])
        def unregister_node():
            node_id = request.json['node_id']
            self.node_manager.unregister_node(node_id)
            return jsonify({'status': 'ok'})
            
        # 任务分发接口
        @self.app.route('/task/get', methods=['GET'])
        def get_task():
            node_id = request.args.get('node_id')
            node_capacity = self.node_manager.get_node_capacity(node_id)
            urls = self.load_balancer.get_tasks(node_capacity)
            return jsonify({'urls': urls})

        # 监控接口
        @self.app.route('/monitor/stats', methods=['GET'])
        def get_stats():
            stats = {
                'active_nodes': len(self.node_manager.get_active_nodes()),
                'total_urls': self.url_manager.get_total_count(),
                'processed_urls': self.url_manager.get_processed_count(),
                'node_stats': self.node_manager.get_nodes_stats()
            }
            return jsonify(stats)

    def run(self):
        # Windows兼容性配置
        import platform
        if platform.system() == 'Windows':
            self.app.run(host=SystemConfig.MASTER_HOST, port=SystemConfig.MASTER_PORT)
        else:
            self.app.run(host='0.0.0.0', port=SystemConfig.MASTER_PORT)
