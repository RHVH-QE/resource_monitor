from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from resource_monitor.items import CockpitOvirtItem
from resource_monitor.usr_general_helpers import get_all_names_from_db
from resource_monitor.settings import SPIDER_NAME_COLLECTION


class CockpitOvirt(CrawlSpider):
    name = 'cockpit-ovirt'
    allowed_domains = [
        'brewweb.engineering.redhat.com', 'download.engineering.redhat.com'
    ]

    #start_urls = ['https://brewweb.engineering.redhat.com/brew/packageinfo?packageID=48429']
    start_urls = [
        'https://brewweb.engineering.redhat.com/brew/packageinfo?packageID=57864'
    ]

    rules = (Rule(
        LxmlLinkExtractor(restrict_xpaths=(
            '//a[contains(@href, "buildinfo")]', )),
        callback='parse_single_build_page'), )

    def __init__(self, *args, **kwargs):
        super(CockpitOvirt, self).__init__(*args, **kwargs)
        self.all_names = get_all_names_from_db(
            SPIDER_NAME_COLLECTION[self.name], 'build_name')

    def parse_single_build_page(self, response):

        item = CockpitOvirtItem()

        item['build_name'] = response.xpath('//h4/a/text()').extract()[0]

        if item['build_name'] in self.all_names:
            self.log("%s has been already downloaded" % item['build_name'])
            return

        item['build_status'] = response.xpath('//th[text()="State"]/following-sibling::td[1]/text()') \
            .extract()[0].strip()

        if item['build_status'] == 'complete':

            item['build_tag'] = response.xpath(
                '//a[contains(@href, "taginfo?tagID")]/text()').extract()

            if item['build_tag']:
                item['build_tag'] = item['build_tag'][0]
            else:
                item['build_tag'] = "No Tags Found"

            item['build_rpm_url'] = response.xpath(
                '//a[text()="download"]/@href').re('(.+\.noarch.rpm)')[0]

            item['build_downloaded'] = False

            yield item


