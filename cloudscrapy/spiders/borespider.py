# -*- coding: gbk -*-

from scrapy.spider import BaseSpider
from cloudscrapy.items import UiItem


class UiSpider(BaseSpider):
    name = "ui"

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

    def parse(self, response):

        if response.url.startswith(self.ui_china_host):
            for sel in response.xpath('//ul/li'):
                a = sel.xpath('div[@class="cover pos"]/a')
                if len(a) == 0:
                    continue

                item = UiItem()

                item['name'] = get_str(a[0], '@title')
                item['imgUrl'] = get_str(a[0], 'img/@src')
                item['desc'] = ''
                item['srcTag'] = 'UI China'

                link = get_str(a[0], '@href')
                if not link.startswith('http://'):
                    link = self.ui_china_host + link
                item['srcLink'] = link

                yield item

        elif response.url.startswith(self.dribbble_host):
            for sel in response.xpath('//ol/li'):
                links = sel.xpath('div/div/div/a[@class="dribbble-link"]')
                overs = sel.xpath('div/div/div/a[@class="dribbble-over"]')
                if len(links) == 0 or len(overs) == 0:
                    continue

                item = UiItem()

                item['name'] = get_str(overs[0], 'strong/text()')
                item['imgUrl'] = get_str(links[0], 'div/div[2]/@data-src')
                item['desc'] = get_str(overs[0], 'span/text()')
                item['srcTag'] = 'Dribble'

                link = get_str(links[0], '@href')
                if not link.startswith('http://'):
                    link = self.ui_china_host + link
                item['srcLink'] = link

                yield item



def get_str(sel, xpath):
    strs = sel.xpath(xpath).extract()
    if len(strs) == 0:
        return ''
    else:
        return strs[0].strip()

        # scrapy crawl ui
