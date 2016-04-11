import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from resource_monitor.items import OvirtNodeNgnItem
from resource_monitor.usr_general_helpers import get_all_names_from_db
from resource_monitor.settings import SPIDER_NAME_COLLECTION

class OvirtNodeNgN36Spider(CrawlSpider):
    name = "ovirtnodengn36"
    allowed_domains = ['ovirt.org']
    start_urls = ["http://jenkins.ovirt.org/job/ovirt-node-ng_ovirt-3.6_build-artifacts-fc22-x86_64/lastSuccessfulBuild/artifact/exported-artifacts/"]

    def __init__(self):
        self.all_names = get_all_names_from_db(SPIDER_NAME_COLLECTION[self.name], 'build_name')
        print self.all_names


    def make_requests_from_url(self, url):
        return scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        base_url = response.url

        str_image_update = ".*ovirt-node-ng-image-update.*"
        str_manifest = r".*manifest.*"
        str_squashfs = r".*squashfs.*"
        str_installer = r".*ovirt-node-ng-installer.*"
        str_tools = r".*ovirt-node-ng-tools.*"
        sel = Selector(response)
        item = OvirtNodeNgnItem()

        for i in sel.xpath('//a'):
            if len(i.xpath('text()').re(str_image_update)) != 0:
                item['ngn_image_url'] = base_url + \
                    i.xpath('@href').extract()[0]
                tag_min = i.xpath('text()').extract()[0]
                tag_list = tag_min.split("-")
                tag_list.append('36')
                item['ngn_tag'] = "-".join(tag_list[-2:])
                item['build_downloaded'] = False
            elif len(i.xpath('text()').re(str_manifest)) != 0:
                item['ngn_manifest_url'] = base_url + \
                    i.xpath('@href').extract()[0]
            elif len(i.xpath('text()').re(str_squashfs)) != 0:
                item['ngn_squash_url'] = base_url + \
                    i.xpath('@href').extract()[0]
            elif len(i.xpath('text()').re(str_installer)) != 0:
                item['build_name'] = i.xpath('@href').extract()[0]
                item['ngn_iso_url'] = base_url + \
                    i.xpath('@href').extract()[0]
            elif len(i.xpath('text()').re(str_tools)) != 0:
                item['ngn_tools_url'] = base_url + i.xpath('@href').extract()[0]
            else:
                pass
        if item['build_name'] in self.all_names:
            return
        else:
            yield item
