class SystemConfig:
    # Master节点配置
    MASTER_HOST = "localhost"
    MASTER_PORT = 5000
    
    # Redis配置(用于URL队列管理)
    REDIS_HOST = "127.0.0.1"  # Windows下推荐使用IP地址
    REDIS_PORT = 6379
    REDIS_WINDOWS_PATH = "G:\\青训营\\系统代码\\redis-data"  # 添加Windows专用存储路径
    
    # MongoDB配置(用于存储爬取数据)
    MONGO_URI = "mongodb://127.0.0.1:27017/?directConnection=true"  # 添加Windows连接参数
    MONGO_DB = "crawler_db"
    
    # 爬虫配置
    MAX_WORKERS = 4  # 每个节点的最大工作进程数
    CRAWL_DELAY = 1  # 爬取延迟(秒)
    
    # URL管理配置
    URL_BATCH_SIZE = 100  # URL批处理大小
    
    # 代理配置
    PROXY_POOL_URL = "http://localhost:5555/random"  # 代理池API 
    
    # 节点管理配置
    HEARTBEAT_INTERVAL = 30  # 心跳间隔(秒)
    NODE_TIMEOUT = 60  # 节点超时时间(秒)
    
    # 负载均衡配置
    DEFAULT_STRATEGY = 'least_connections'
    MIN_NODE_CAPACITY = 1
    MAX_NODE_CAPACITY = 10
    
    # 监控配置
    MONITOR_INTERVAL = 60  # 监控数据收集间隔(秒)
    MONITOR_RETENTION = 3600  # 监控数据保留时间(秒)
    
    # 爬虫重试配置
    MAX_RETRIES = 3
    RETRY_DELAY = 5
    REQUEST_TIMEOUT = 30
    
    # 数据存储配置
    STORAGE_BATCH_SIZE = 100
    STORAGE_RETRY_COUNT = 3
