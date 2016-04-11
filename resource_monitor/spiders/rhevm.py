import re
from itertools import dropwhile
import requests
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from resource_monitor.items import Rhevm35Item, Rhevm36Item
from resource_monitor.usr_general_helpers import get_all_names_from_db
from resource_monitor.settings import SPIDER_NAME_COLLECTION


def get_rhevm_release_status(*args):
    status_link_1 = 'http://bob.eng.lab.tlv.redhat.com/builds/%s/%s/release_status.txt'
    status_link_2 = 'http://bob.eng.lab.tlv.redhat.com/builds/%s/release_status.txt'
    if len(args) == 2:
        resp = requests.get(status_link_1 % (args[0], args[1]))
    else:
        resp = requests.get(status_link_2 % args[0])

    status = resp.content.split('\n')[0].split(':')[-1].strip()

    if status == 'Ready':
        return True
    else:
        return False


class Rhevm35(CrawlSpider):
    name = 'rhevm35'
    allowed_domains = ['bob.eng.lab.tlv.redhat.com', ]

    start_urls = ['http://bob.eng.lab.tlv.redhat.com/builds',]

    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths=('//a[starts-with(@href, "vt")]',)),
            callback='parse_single_build_page'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(Rhevm35, self).__init__(*args, **kwargs)
        self.all_names = get_all_names_from_db(SPIDER_NAME_COLLECTION[self.name], 'build_name')

    def parse_single_build_page(self, response):

        item = Rhevm35Item()

        item['build_name'] = response.xpath('//title/text()').extract()[0].split('/')[-1].strip()

        if 'bad' in response.url \
                or 'old' in response.url \
                or 'bak' in response.url \
                or item['build_name'] in self.all_names:
            return

        if not get_rhevm_release_status(item['build_name']):
            return

        request = Request("%sel6" % response.url, callback=self.get_repo_links)
        request.meta['item'] = item

        yield request

    @staticmethod
    def get_repo_links(response):
        item = response.meta['item']
        item['build_links'] = ','.join(dropwhile(lambda x: x.startswith('?'), response.xpath('//a/@href').extract()))
        item['build_pkg'] = re.findall(r'(rhevm-\d\.\d.+?\.rpm)', item['build_links'])[0]
        item['build_downloaded'] = False

        yield item


class Rhevm36(CrawlSpider):

    name = 'rhevm36'
    allowed_domains = ['bob.eng.lab.tlv.redhat.com', ]

    start_urls = ['http://bob.eng.lab.tlv.redhat.com/builds/3.6/', ]

    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths=('//a[starts-with(@href, "3")]',)),
            callback='parse_single_build_page'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(Rhevm36, self).__init__(*args, **kwargs)
        self.all_names = get_all_names_from_db(SPIDER_NAME_COLLECTION[self.name], 'build_name')

    def parse_single_build_page(self, response):

        item = Rhevm36Item()
        item['build_name'] = response.url.split('/')[-2]

        if 'bad' in response.url \
                or 'bak' in response.url \
                or 'old' in response.url \
                or item['build_name'] in self.all_names:
            return

        if not get_rhevm_release_status('3.6', item['build_name']):
            return

        request = Request("%sel6/noarch/" % response.url, callback=self.get_repo_links)
        request.meta['item'] = item

        yield request

    def get_repo_links(self, response):
        item = response.meta['item']
        item['build_links'] = ','.join(dropwhile(lambda x: x.startswith('?'), response.xpath('//a/@href').extract()))
        item['build_pkg'] = re.findall(r'(rhevm-\d\.\d.+?\.rpm)', item['build_links'])[0]
        item['build_downloaded'] = False

        yield item


if __name__ == '__main__':
    print get_rhevm_release_status('3.6', '3.6.0-22')