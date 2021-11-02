# -*- coding: utf-8 -*-
"""
@author: 可以叫我才哥
"""

import requests
import re
import pandas as pd
import html
from lxml import etree
import time


def get_html(url):
    time.sleep(1)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }

    r = requests.get(url, headers=headers)

    # 请求的网页数据中有网页特殊字符，通过以下方法进行解析
    r = html.unescape(r.text)
    r = re.sub(':\xa0', '', r)

    return r


url = 'https://www.douban.com/doulist/110567393/'
r = get_html(url)
# 获取全部URL地址
r_text = re.sub(r'\s','',r)
urls = re.findall(r'<divclass="title"><ahref="(.*?)"',r_text)

works = []

for url in urls:
    work = {}
    work['url'] = url
    r_info = get_html(work['url'])
    r_info_html = etree.HTML(r_info)
    a = r_info_html.xpath('//div[@id="info"]//text()')
    b = ''.join(a)
    c = b.replace(' ', '')
    d = re.sub(r'\n+', '\\n', c)
    e = d.split('\n')
    keys = [i.split(':')[0] for i in e[1:-1]]
    values = [i.split(':')[1] for i in e[1:-1]]
    work.update(dict(zip(keys, values)))
    work['作品名称'] = r_info_html.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
    work['年份'] = r_info_html.xpath('//*[@id="content"]/h1/span[2]/text()')[0]

    try:
        work['评分'] = r_info_html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
        work['评价数'] = r_info_html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')[0]
    except:
        pass

    works.append(work)

df = pd.DataFrame(works)
df.to_excel(r'007.xlsx',index=None)
