import requests
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from resource_monitor.items import RhevhItem, RhevhNgnItem
from resource_monitor.usr_general_helpers import get_competent_version, get_all_names_from_db
from resource_monitor.settings import SPIDER_NAME_COLLECTION


class RhevhSpider(CrawlSpider):
    name = 'rhevh7'
    allowed_domains = ['brewweb.engineering.redhat.com',
                       'download.eng.bos.redhat.com',
                       'download.devel.redhat.com',
                       'download.engineering.redhat.com']

    start_urls = ['https://brewweb.engineering.redhat.com/brew/packageinfo?packageID=36140', ]

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=('//a[contains(@href, "buildinfo")]', )),
             callback='parse_single_build_page'),)

    def __init__(self, *args, **kwargs):
        super(RhevhSpider, self).__init__(*args, **kwargs)
        self.all_names = get_all_names_from_db(SPIDER_NAME_COLLECTION[self.name], 'build_name')

    def formatted_log(self, msg):
        length = len(msg)
        self.log('=' * length)
        self.log(msg)
        self.log('=' * length)

    def parse_single_build_page(self, response):
        item = RhevhItem()

        self.formatted_log('Start to parsing page: %s' % response.url)

        item['build_name'] = response.xpath('//h4/a/text()').extract()[0]
        if item['build_name'] in self.all_names:
            self.log("%s has been already downloaded" % item['build_name'])
            return

        item['build_status'] = response.xpath('//th[text()="State"]/following-sibling::td[1]/text()') \
            .extract()[0].strip()
        if item['build_status'] == 'complete':
            item['build_tag'] = response.xpath('//a[contains(@href, "taginfo?tagID")]/text()').extract()[0]
            item['build_iso'] = response.xpath('//a[text()="download"]/@href').re('(.+\.iso|.+\.noarch.rpm)')[0]
            build_log_url = response.xpath('//a[text()="build logs"]/@href').extract()[0]

            request = Request(build_log_url, callback=self.parse_mock_log)
            request.meta['item'] = item

            yield request
        else:
            item['build_tag'] = 'No Tag Found'
            item['build_iso'] = 'No ISO available, due to build status is not complete'
            return

    def parse_mock_log(self, response):
        self.formatted_log('Start to parsing page: %s' % response.url)
        item = response.meta['item']

        mock_log_url = response.url + 'mock_output.log'

        ret = get_competent_version(requests.get(mock_log_url).text)

        item['build_ovirt_node_version'] = ret[0]
        item['build_vdsm_version'] = ret[1]
        item['build_downloaded'] = False

        yield item


class Rhevh6Spider(RhevhSpider):
    name = 'rhevh6'
    start_urls = ['https://brewweb.engineering.redhat.com/brew/packageinfo?packageID=33636', ]


class RhevhNGN36Spider(RhevhSpider):
    name = "rhevh36ngn"
    start_urls = ['https://brewweb.engineering.redhat.com/brew/packageinfo?packageID=58439', ]

    def parse_single_build_page(self, response):
        item = RhevhNgnItem()

        self.formatted_log('Start to parsing page: %s' % response.url)

        item['build_name'] = response.xpath('//h4/a/text()').extract()[0]
        if item['build_name'] in self.all_names:
            self.log("%s has been already downloaded" % item['build_name'])
            return

        item['build_status'] = response.xpath('//th[text()="State"]/following-sibling::td[1]/text()') \
            .extract()[0].strip()
        if item['build_status'] == 'complete':
            item['build_tag'] = response.xpath('//a[contains(@href, "taginfo?tagID")]/text()').extract()[0]
            item['build_update_rpm'] = response.xpath('//a[text()="download"]/@href').re('(.+\.iso|.+\.noarch.rpm)')[0]
            item['build_ks'] = response.xpath('//a[text()="download"]/@href').re('(.+\.ks)')
            item['build_squashfs_img'] = response.xpath('//a[text()="download"]/@href').re('(.+\.squashfs)')[0]
            item['build_downloaded'] = False

            yield item
        else:
            item['build_tag'] = 'No Tag Found'
            item['build_squashfs_img'] = 'No ISO available, due to build status is not complete'
            return
