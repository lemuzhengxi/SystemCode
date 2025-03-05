from bs4 import BeautifulSoup
import re

class HTMLParser:
    def __init__(self):
        self.parsers = {
            'default': self._default_parser,
            'article': self._article_parser,
            'list': self._list_parser
        }
        
    def parse(self, html, parser_type='default'):
        """解析HTML内容"""
        if parser_type not in self.parsers:
            parser_type = 'default'
        return self.parsers[parser_type](html)
        
    def _default_parser(self, html):
        """默认解析器"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 检查robots meta标签
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        if robots_meta and ('noindex' in robots_meta.get('content', '').lower()):
            return None
            
        data = {
            'title': soup.title.string if soup.title else '',
            'text': soup.get_text(),
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'meta': {
                meta.get('name'): meta.get('content')
                for meta in soup.find_all('meta')
                if meta.get('name') and meta.get('content')
            }
        }
        return data 