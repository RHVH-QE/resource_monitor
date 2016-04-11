from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from resource_monitor.items import VDSMItem
from resource_monitor.usr_general_helpers import get_all_names_from_db
from resource_monitor.settings import SPIDER_NAME_COLLECTION


class VDSMSpider(CrawlSpider):
    name = 'vdsm'

    allowed_domains = ['brewweb.engineering.redhat.com',
                       'download.eng.bos.redhat.com',
                       'download.devel.redhat.com',
                       'download.engineering.redhat.com']

    start_urls = ['https://brewweb.engineering.redhat.com/brew/packageinfo?packageID=10943']

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=('//a[contains(@href, "buildinfo")]', )),
             callback='parse_single_build_page'),
    )

    def __init__(self, *args, **kwargs):
        super(VDSMSpider, self).__init__(*args, **kwargs)
        self.all_names = get_all_names_from_db(SPIDER_NAME_COLLECTION[self.name], 'build_name')

    def formatted_log(self, msg):
        length = len(msg)
        self.log('=' * length)
        self.log(msg)
        self.log('=' * length)

    def parse_single_build_page(self, response):
        item = VDSMItem()

        self.formatted_log('Start to parsing page: %s' % response.url)

        item['build_name'] = response.xpath('//h4/a/text()').extract()[0]
        if item['build_name'] in self.all_names:
            self.log("%s has been already downloaded" % item['build_name'])
            return

        item['build_status'] = response.xpath('//th[text()="State"]/following-sibling::td[1]/text()') \
            .extract()[0].strip()
        if item['build_status'] == 'complete':
            try:
                item['build_tag'] = response.xpath('//a[contains(@href, "taginfo?tagID")]/text()').extract()[0]
            except IndexError:
                item['build_tag'] = "This one should have a Tag, but actually no Tag found in brew page"
        else:
            item['build_tag'] = 'No Tag Found'

        yield item
