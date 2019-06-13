import requests
from lxml.html import fromstring
from logger import logger
import re
import time
from functools import wraps
import pandas as pd

url = 'http://www.zxcs.me/sort/43'
filename = 'book13.csv'
url2 = 'http://www.zxcs.me/content/plugins/cgz_xinqing/cgz_xinqing_action.php?action=mood&id={code}'
url3 = 'http://www.zxcs.me/download.php?id={code}'
review = ['仙草', '粮草', '干草', '枯草', '毒草']
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
host = 'www.zxcs.me'
re1 = re.compile(r'^《(.*?)》.*?作者：(.*?)$')
re2 = re.compile(r'.*?(\d+)$')
re3 = re.compile(r'.*?(\d+[.]\d+)')

s = requests.session()

def get_wrapper(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        def inner():
            try:
                logger.info('[开始爬取]' + args[0])
                r = fun(*args, **kwargs)
            except:
                logger.error('[爬取异常]' + args[0])
                r = ''
            return r
        retry = 1
        r = inner()
        while not r and retry > 0:
            r = inner()
            retry -= 1
        if r and r.status_code == 200:
            logger.info('[爬取成功]' + args[0])
        # r.encoding = r.apparent_encoding
        return r
    return wrapper

s.get = get_wrapper(s.get)

def parse_tree(tree):
    all_items = []
    all_pl = tree.xpath('//*[@id="plist"]')
    for pl in all_pl:
        item = dict()
        dt = pl.xpath('dt/a')
        dd1 = pl.xpath('dd[1]')
        dd2 = pl.xpath('dd[2]')[0].getchildren()
        title = re1.match(dt[0].text).group(1)
        author = re1.match(dt[0].text).group(2)
        code = re2.match(dt[0].xpath('@href')[0]).group(1)
        try:
            size, abstract = dd1[0].text.strip().split('【内容简介】：')
            size = re3.match(size).group(1)
        except:
            size = 0
        
        abstract = abstract.split('正版订阅')[0].strip()
        cate1 = dd2[0].text
        cate2 = dd2[1].text
        item['title'] = title
        item['author'] = author
        item['code'] = code
        item['size'] = size
        item['abstract'] = abstract
        item['cate1'] = cate1
        item['cate2'] = cate2
        all_items.append(item)
    return all_items


def get_review(item, code):
    logger.info('尝试获取' + item['title'] + '的评价数据')
    html = s.get(url2.format(code=code), timeout=30, headers={'User-Agent': ua, 'host':host})
    if not html:
        for i in range(len(review)):
            item[review[i]] = 0
        return
    temp = list(map(int, html.text.split(',')))
    for i in range(len(temp)):
        item[review[i]] = temp[i]

def get_downloadLink(item, code):
    logger.info('尝试获取' + item['title'] + '的下载链接')
    html = s.get(url3.format(code=code), timeout=30, headers={'User-Agent': ua, 'host':host})
    try:
        html = fromstring(html.text)
        link = html.xpath('//span[@class="downfile"]/a')
        item['link1'] = link[0].xpath('@href')[0]
        item['link2'] = link[1].xpath('@href')[0]
    except:
        item['link1'] = ''
        item['link2'] = ''
    
    
    

def has_next(tree):
    try:
        next_node = tree.xpath('//div[@id="pagenavi"]/span/following-sibling::*[1]')
        if next_node and next_node[0].tag == 'a':
            logger.info('存在下一页: ' + next_node[0].text)
            return next_node[0].xpath('@href')[0]
    except:
        return ''




def main(url, round=100):
    urls = [url]
    novels = []
    while urls and round > 0:
        u = urls.pop()
        logger.info('开始爬取列表页面：' + str(u))
        html = s.get(u, timeout=30, headers={'User-Agent': ua, 'host':host})
        if not html:
            continue
        tree = fromstring(html.text)
        items = parse_tree(tree)
        for item in items:
            get_review(item, item['code'])
            get_downloadLink(item, item['code'])
        novels.append(items)
        print(items)
        next_u = has_next(tree)
        round -= 1
        if next_u:
            time.sleep(5)
            urls.append(next_u)
    return novels

def to_csv(novels, filename):
    data = pd.concat(map(pd.DataFrame, novels))
    data.to_csv(filename, index=False)


if __name__ == '__main__':
    novels = main(url)
    to_csv(novels, filename)