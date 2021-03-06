# -*- coding: utf-8 -*-

# Scrapy settings for resource_monitor project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'resource_monitor'

SPIDER_MODULES = ['resource_monitor.spiders']
NEWSPIDER_MODULE = 'resource_monitor.spiders'

_MONGOURI_TEST = 'mongodb://127.0.0.1:27017'
_MONGOURI_PROD = 'mongodb://meteor:redhat@10.66.10.22/meteordb?authMechanism=SCRAM-SHA-1'
MONGO_URI = _MONGOURI_PROD

MONGO_DATABASE = 'meteordb'

ITEM_PIPELINES = {
    'resource_monitor.pipelines.RhevmAppliancePipeline': 300,
}

SPIDER_NAME_COLLECTION = {
    'cockpit_ovirt': 'resources.cockpit_ovirt',
    'rhevm_appliance': 'resources.rhevm_appliance',
    'rhevh7': 'resources.rhevh7',
    'rhevh6': 'resources.rhevh6',
    'ovirt_node': 'resources.ovirt_node',
    'vdsm': 'resources.vdsm',
    'rhevm35': 'resources.rhevm35',
    'rhevm36': 'resources.rhevm36',
    'rhevm40': 'resources.rhevm40',
    'rhevm42': 'resources.rhevm42',
    'rhevh36ngn': 'resources.rhevh36ngn',
    'ovirtnodengn36': 'resources.ovirtnodengn36',
    'ovirtnodengn40': 'resources.ovirtnodengn40',
    'ovirtnodengnmaster': 'resources.ovirtnodengnmaster',
    'rhvh4_iso': 'resources.rhvh4_iso'
}


SPIDER_MAP = {
    'rhevh7': 'RhevhSpider',
    'rhevh6': 'Rhevh6Spider',
    'ovirt': 'OvirtNodeSpider',
    'vdsm': 'VDSMSpider',
    'rhevm35': 'Rhevm35',
    'rhevm36': 'Rhevm36',
    'rhevm40': 'Rhevm40',
    'rhevm42': 'Rhevm42',
    'rhevh36ngn': 'RhevhNGN36Spider',
    'ovirtnodengn36': 'OvirtNodeNgN36Spider',
    'ovirtnodengn40': 'OvirtNodeNgN40Spider',
    'ovirtnodengnmaster': 'OvirtNodeNgNMasterSpider',
    'rhvh4_iso': 'Rhvh4ISO'
}


PROJECT_ROOT = base_path = '/'.join(__file__.split(os.path.sep)[:-2])

# CRITICAL - for critical errors (highest severity)
# ERROR - for regular errors
# WARNING - for warning messages
# INFO - for informational messages
# DEBUG - for debugging messa
LOG_LEVEL = 'INFO'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'resource_monitor (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'resource_monitor.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'resource_monitor.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'resource_monitor.pipelines.SomePipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
