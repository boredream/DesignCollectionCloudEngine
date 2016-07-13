# -*- coding: gbk -*-

from cloudspider.items import UiItem
import urllib2
from cloudspider.sqlhelper import SqliteHelper

sql_helper = SqliteHelper()
start_urls = []

# ui china
ui_china_host = 'http://www.ui.cn'
for page in range(1, 2):
    url = ui_china_host + '/list.html?p=%d&tag=0&r=edit&subcatid=0&catid=0' % page
    start_urls.append(url)

# dribbble
dribbble_host = 'https://dribbble.com'

for page in range(1, 2):
    url = dribbble_host + '/shots?&page=%d&per_page=12' % page
    start_urls.append(url)

from lxml import etree


def parse_content(url, content):
    response = etree.HTML(content)
    if url.startswith(ui_china_host):
        for sel in response.xpath('//ul/li/div[@class="cover pos"]/a'):
            name = sel.get('title')
            imgUrl = sel[0].get('data-original')
            desc = ''
            srcTag = 'UI China'
            link = sel.get('href')
            if not link.startswith('http://'):
                link = ui_china_host + link
            isAdd = '0'

            item = UiItem(name, imgUrl, desc, srcTag, link, isAdd)
            sql_helper.process_item(item)

    elif url.startswith(dribbble_host):
        for sel in response.xpath('//ol/li/div/div/div'):
            if len(sel) < 2:
                continue

            link = sel[0]
            over = sel[1]

            name = over[0].text
            imgUrl = link[0][1].get('data-src')
            desc = over[1].text
            srcTag = 'Dribbble'
            link = link.get('href')
            if not link.startswith('http://'):
                link = ui_china_host + link
            isAdd = '0'

            item = UiItem(name, imgUrl, desc, srcTag, link, isAdd)
            sql_helper.process_item(item)


def get_str(sel, xpath):
    strs = sel.xpath(xpath).extract()
    if len(strs) == 0:
        return ''
    else:
        return strs[0].strip()


def execute():
    global url
    for url in start_urls:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
        }
        request = urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(request).read()
        parse_content(url, content)
    sql_helper.close_spider()


if __name__ == '__main__':
    execute()
