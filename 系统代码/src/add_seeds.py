from src.url_manager.seed_manager import SeedManager

def add_initial_seeds():
    # Windows控制台编码设置
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    seed_manager = SeedManager()
    
    # 添加一些测试用的种子URL
    seed_urls = [
        'https://example.com',
        'https://example.org',
        # 添加更多URL...
    ]
    
    seed_manager.add_seed_urls(seed_urls)
    print("种子URL添加成功！")

if __name__ == '__main__':
    add_initial_seeds()
