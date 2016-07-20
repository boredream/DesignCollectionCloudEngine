# -*- coding: gbk -*-

from cloudspider.items import UiItem
import urllib2
from cloudspider.sqlhelper import SqliteHelper
import re

sql_helper = SqliteHelper()
all_urls = {}

# ui china
ui_china_tag = 'UI China'
ui_china_host = 'http://www.ui.cn'
for page in range(1, 2):
    url = ui_china_host + '/list.html?p=%d&tag=0&r=edit&subcatid=0&catid=0' % page
    if ui_china_tag not in all_urls:
        all_urls[ui_china_tag] = []
    all_urls[ui_china_tag].append(url)

# dribbble
dribbble_tag = 'Dribbble'
dribbble_host = 'https://dribbble.com'

for page in range(1, 2):
    url = dribbble_host + '/shots?&page=%d&per_page=12' % page
    if dribbble_tag not in all_urls:
        all_urls[dribbble_tag] = []
    all_urls[dribbble_tag].append(url)


def parse_content(url, content):
    if url.startswith(ui_china_host):
        pattern = re.compile('[\\s\\S]*?(<div class="cover pos">[\\s\\S]*?</div>)[\\s\\S]*?')
        for sel in pattern.findall(content):
            if '<div class="cover pos">' not in sel:
                continue

            name = ''
            pattern = re.compile('[\\s\\S]*?<a .*?title="(.*?)".*?>')
            matcher = pattern.match(sel)
            if matcher:
                name = matcher.group(1)

            imgUrl = ''
            pattern = re.compile('[\\s\\S]*?<img .*?data-original="(.*?)".*?>')
            matcher = pattern.match(sel)
            if matcher:
                imgUrl = matcher.group(1)

            desc = ''
            srcTag = ui_china_tag

            link = ''
            pattern = re.compile('[\\s\\S]*?<a .*?href="(.*?)".*?>')
            matcher = pattern.match(sel)
            if matcher:
                link = matcher.group(1)
            if not link.startswith('http://'):
                link = ui_china_host + link

            isAdd = '0'

            item = UiItem(name, imgUrl, desc, srcTag, link, isAdd)
            sql_helper.process_item(item)

    elif url.startswith(dribbble_host):
        pattern = re.compile('[\\s\\S]*?(<li id="screenshot-[\\s\\S]*?</li>)[\\s\\S]*?')
        for sel in pattern.findall(content):
            if '<div class="dribbble-img">' not in sel:
                continue

            over = ''
            pattern = re.compile('[\\s\\S]*?(<a class="dribbble-over"[\\s\\S]*?</a>)')
            matcher = pattern.match(sel)
            if matcher:
                over = matcher.group(1)

            name = ''
            pattern = re.compile('[\\s\\S]*?<strong>([\\s\\S]*?)</strong>')
            matcher = pattern.match(sel)
            if matcher:
                name = matcher.group(1)

            imgUrl = ''
            pattern = re.compile('[\\s\\S]*?<div .*?data-src="(.*?)".*?>')
            matcher = pattern.match(sel)
            if matcher:
                imgUrl = matcher.group(1)

            desc = ''
            pattern = re.compile('[\\s\\S]*?<span .*?>([\\s\\S]*?)</span>')
            matcher = pattern.match(sel)
            if matcher:
                desc = matcher.group(1).replace('\n\n', '\n')

            link = ''
            pattern = re.compile('[\\s\\S]*?<a .*?href="(.*?)".*?>')
            matcher = pattern.match(sel)
            if matcher:
                link = matcher.group(1)
            if not link.startswith('http://'):
                link = dribbble_host + link

            srcTag = dribbble_tag
            isAdd = '0'

            item = UiItem(name, imgUrl, desc, srcTag, link, isAdd)
            sql_helper.process_item(item)


def get_str(sel, xpath):
    strs = sel.xpath(xpath).extract()
    if len(strs) == 0:
        return ''
    else:
        return strs[0].strip()


def execute(srcTag):
    urls = all_urls.get(srcTag)
    for url in urls:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
        }
        request = urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(request).read()
        parse_content(url, content)
    sql_helper.close_spider()


if __name__ == '__main__':
    execute()
