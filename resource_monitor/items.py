# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RhevmApplianceItem(scrapy.Item):
    build_name = scrapy.Field()
    build_tag = scrapy.Field()
    build_status = scrapy.Field()
    build_ova_url = scrapy.Field()
    build_downloaded = scrapy.Field()
    build_rpm_url = scrapy.Field()


class RhevhItem(scrapy.Item):
    build_name = scrapy.Field()
    build_iso = scrapy.Field()
    build_tag = scrapy.Field()
    build_status = scrapy.Field()

    build_ovirt_node_version = scrapy.Field()
    build_vdsm_version = scrapy.Field()
    build_vdsm_tag = scrapy.Field()

    ovirt_node_tag = scrapy.Field()
    edit_node_tools_url = scrapy.Field()
    minimizer_url = scrapy.Field()
    ipmi_url = scrapy.Field()
    puppet_url = scrapy.Field()

    build_downloaded = scrapy.Field()


class RhevhNgnItem(scrapy.Item):
    build_name = scrapy.Field()
    build_tag = scrapy.Field()
    build_status = scrapy.Field()
    build_ks = scrapy.Field()
    build_update_rpm = scrapy.Field()
    build_squashfs_img = scrapy.Field()

    build_downloaded = scrapy.Field()


class OvirtNodeItem(scrapy.Item):
    build_name = scrapy.Field()
    build_tag = scrapy.Field()
    build_status = scrapy.Field()
    build_edit_node_url = scrapy.Field()
    build_ovirt_node_minimizer_url = scrapy.Field()
    build_ovirt_node_plugin_ipmi_url = scrapy.Field()
    build_ovirt_node_plugin_puppet_url = scrapy.Field()


class VDSMItem(scrapy.Item):
    build_name = scrapy.Field()
    build_tag = scrapy.Field()
    build_status = scrapy.Field()


class Rhevm35Item(scrapy.Item):
    build_name = scrapy.Field()
    build_pkg = scrapy.Field()
    build_links = scrapy.Field()
    build_downloaded = scrapy.Field()


class Rhevm36Item(scrapy.Item):
    build_name = scrapy.Field()
    build_pkg = scrapy.Field()
    build_links = scrapy.Field()
    build_downloaded = scrapy.Field()


class Rhevm40Item(scrapy.Item):
    build_name = scrapy.Field()
    build_links = scrapy.Field()
    build_downloaded = scrapy.Field()


class Rhevm42Item(scrapy.Item):
    build_name = scrapy.Field()
    build_status = scrapy.Field()


class OvirtNodeNgnItem(scrapy.Item):
    ngn_tag = scrapy.Field()
    ngn_squash_url = scrapy.Field()
    build_name = scrapy.Field()
    ngn_iso_url = scrapy.Field()
    ngn_tools_url = scrapy.Field()
    ngn_manifest_url = scrapy.Field()
    ngn_image_url = scrapy.Field()
    build_downloaded = scrapy.Field()


class Rhvh4ISOItem(scrapy.Item):
    build_name = scrapy.Field()
    build_downloaded = scrapy.Field()
