from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from resource_monitor.usr_general_helpers import get_all_names_from_db
from resource_monitor.settings import SPIDER_NAME_COLLECTION
from resource_monitor.items import Rhvh4ISOItem


class Rhvh4ISO(CrawlSpider):
    name = "rhvh4_iso"
    allowed_domains = ["download-node-02.eng.bos.redhat.com", ]

    start_urls = ["http://download-node-02.eng.bos.redhat.com/devel/candidate-trees/", ]

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=("//a[starts-with(@href, 'RHVH-4.0')]", ),),
             callback='parse_link',),
    )

    def __init__(self, *args, **kwargs):
        super(Rhvh4ISO, self).__init__(*args, **kwargs)
        self.all_names = get_all_names_from_db(SPIDER_NAME_COLLECTION[self.name], 'build_name')

    def parse_link(self, response):
        # links = [link.extract().strip('/')
        #          for link in response.xpath("//a[starts-with(@href, 'RHVH-4.0')]/text()")]
        item = Rhvh4ISOItem()
        url = response.url

        item['build_name'] = url.strip('/').split('/')[-1]
        if item['build_name'] in self.all_names:
            self.log("%s has been already downloaded" % item['build_name'])
            return

        item['build_downloaded'] = False

        yield item
