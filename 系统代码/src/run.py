import argparse
from src.master.master_node import MasterNode
from src.crawler.crawler_node import CrawlerNode

def main():
    parser = argparse.ArgumentParser(description='分布式爬虫系统')
    parser.add_argument('--mode', choices=['master', 'crawler'], required=True,
                       help='运行模式: master或crawler')
    args = parser.parse_args()
    
    if args.mode == 'master':
        master = MasterNode()
        master.run()
    else:
        crawler = CrawlerNode()
        crawler.start()

if __name__ == '__main__':
    main() 