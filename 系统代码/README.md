# 分布式爬虫系统

## 项目简介
基于主从架构的分布式网络爬虫系统，支持动态节点管理、智能任务分发、负载均衡和实时监控。系统包含Master控制节点和多个爬虫工作节点，适用于大规模数据采集场景。

## 主要功能
- ✅ 主从节点心跳管理
- ✅ 动态任务分配与负载均衡
- ✅ 多进程网页抓取
- ✅ Redis队列管理URL
- ✅ MongoDB数据存储
- ✅ 代理IP自动管理
- ✅ 实时系统监控

## 技术栈
- **核心语言**: Python 3.9
- **Web框架**: Flask
- **数据库**: MongoDB、Redis
- **HTML解析**: BeautifulSoup4
- **系统监控**: psutil
- **进程管理**: multiprocessing

## 安装说明
```bash
# 克隆仓库
git clone https://github.com/yourusername/distributed-crawler-system.git

# 安装依赖
pip install -r requirements.txt

# 启动必要服务（Windows）
redis-server --service-start
mongod --dbpath G:\青训营\系统代码\redis-data
```

## 配置文件
修改 `src/config/system_config.py`：
- MASTER_HOST/MASTER_PORT: 主节点地址
- REDIS_*: Redis连接配置
- MONGO_URI: MongoDB连接字符串

## 运行系统
```bash
# 启动Master节点
python src/master/master_node.py

# 启动爬虫节点（多个终端分别运行）
python src/crawler/crawler_node.py
```

## 项目结构
```
├── src/
│   ├── config/         # 系统配置
│   ├── crawler/        # 爬虫节点实现
│   ├── master/         # 主节点控制
│   ├── node_manager/   # 节点生命周期管理
│   ├── task_dispatcher # 任务分发策略
│   └── utils/         # 工具模块
└── requirements.txt    # 依赖清单
```

## 许可证
MIT License