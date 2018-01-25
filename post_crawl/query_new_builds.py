#!/home/dracher/Projects/vEnvs/vScrapy/bin/python
# -*- coding: utf-8 -*
import os
import time
import xmlrpclib
import pymongo

import smtplib

# Here are the email package modules we'll need

from email.mime.multipart import MIMEMultipart


def send_mail(v, s):
    to_list = ['dguo@redhat.com', 'rhvh-qe@redhat.com']
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'New rhevm %s is %s' % (v, s)

    msg['From'] = "yaniwang@redhat.com"
    msg['To'] = ', '.join(to_list)

    s = smtplib.SMTP('smtp.corp.redhat.com')
    s.sendmail("yaniwang@redhat.com", to_list, msg.as_string())
    s.quit()


_MONGOURI_TEST = 'mongodb://127.0.0.1:27017'
_MONGOURI_PROD = 'mongodb://meteor:redhat@10.66.10.22/meteordb?authMechanism=SCRAM-SHA-1'
MONGO_URI = _MONGOURI_PROD

MONGO_DATABASE = 'meteordb'

ANSIBLE_PLAY_BOOK = '/home/dracher/Projects/vEnvs/vScrapy/bin/ansible-playbook'
ANSIBLE_PLAY_BOOK_LOCAL = '/home/dracher/Projects/vEnvs/vAnsible/bin/ansible-playbook'
RHEVM_UPGRADE = "%s -e rhevm35_version='%s' -e rhevm36_version='%s' pb_upgrade_rhevm_%s.yml > /tmp/rhevm%s_upgrade.log"

SPIDER_NAME_COLLECTION = sac = {
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
    'ngn36': 'resources.ovirtnodengn36',
    'ngn40': 'resources.ovirtnodengn40',
    'ngnmaster': 'resources.ovirtnodengnmaster',
    'rhvh_iso': 'resources.rhvh4_iso'
}

REMOTE_PATH_PREFIX = '/var/www/html/monitor/rhevh_build/%s/vdsm%s/%s'


def add_download_job(url, opts=None):
    s = xmlrpclib.ServerProxy("http://10.66.10.22:6800/rpc")
    if not opts:
        opts = {"dir": "/var/www/builds/tmppmt"}
    s.aria2.addUri([
        url,
    ], opts)


class PostCrawlJob(object):
    """"""

    def __init__(self):
        self.cli = pymongo.MongoClient(MONGO_URI)
        self.db = self.cli[MONGO_DATABASE]
        self.rhevh6 = self.db[sac['rhevh6']]
        self.rhevh7 = self.db[sac['rhevh7']]
        self.rhevma = self.db[sac['rhevm_appliance']]
        self.ovirt_node = self.db[sac['ovirt_node']]
        self.vdsm = self.db[sac['vdsm']]
        self.rhevm35 = self.db[sac['rhevm35']]
        self.rhevm36 = self.db[sac['rhevm36']]
        self.rhevm40 = self.db[sac['rhevm40']]
        self.rhevm42 = self.db[sac['rhevm42']]
        self.rhevms = self.db['rhevms']
        self.ngn36 = self.db[sac['ngn36']]
        self.ngn40 = self.db[sac['ngn40']]
        self.rhevh36ngn = self.db[sac['rhevh36ngn']]
        self.ngnmaster = self.db[sac['ngnmaster']]
        self.rhvh_iso = self.db[sac['rhvh_iso']]

    @staticmethod
    def get_new_builds_by_collection(collection, rhevh67=True):
        ret = collection.find({"build_downloaded": False})

        if ret.count() == 0:
            return False

        finals = []

        if not rhevh67:
            for i in ret:
                finals.append(i)
            return finals

        for i in ret:
            if i['build_ovirt_node_version'] == 'No oVirt-Node version found':
                i.update({u'extra_rpms': False})
                finals.append(i)
                continue

            i.update({u'extra_rpms': True})
            finals.append(i)

        return finals

    @staticmethod
    def get_new_rhevm_appliance(collection):
        ret = collection.find({"build_downloaded": False})

        if ret.count() == 0:
            return False

        finals = []

        for i in ret:
            finals.append(i)

        return finals

    @staticmethod
    def get_new_rhevm(collection):
        ret = collection.find({"build_downloaded": False})

        if ret.count() == 0:
            return False

        finals = []

        for i in ret:
            finals.append(i)

        return finals

    @staticmethod
    def get_new_ngn(collection):
        ret = collection.find({"build_downloaded": False})

        if ret.count() == 0:
            return False
        finals = []
        for i in ret:
            finals.append(i)

        return finals

    @staticmethod
    def get_new_rhvh_iso(collection):
        ret = collection.find({"build_downloaded": False})
        if ret.count() == 0:
            return False
        finals = []
        for i in ret:
            finals.append(i)

        return finals

    @staticmethod
    def mark_downloaded_true(collection, build_name):
        collection.update({
            "build_name": build_name
        }, {
            "$set": {
                "build_downloaded": True
            }
        })

    def update_rhevms_host_info(self, tag, x, y):
        self.rhevms.update_many({
            'tag': tag
        }, {
            "$set": {
                "rhevm_version": x,
                "package_version": y
            }
        })


if __name__ == '__main__':

    pcj = PostCrawlJob()
    ret6 = pcj.get_new_builds_by_collection(pcj.rhevh6)
    ret7 = pcj.get_new_builds_by_collection(pcj.rhevh7)
    retrma = pcj.get_new_rhevm_appliance(pcj.rhevma)
    ret_rhevm35 = pcj.get_new_rhevm(pcj.rhevm35)
    ret_rhevm36 = pcj.get_new_rhevm(pcj.rhevm36)
    ret_rhevm40 = pcj.get_new_rhevm(pcj.rhevm40)
    ret_rhevm42 = pcj.get_new_rhevm(pcj.rhevm42)
    ret_ngn36 = pcj.get_new_ngn(pcj.ngn36)
    ret_ngn40 = pcj.get_new_ngn(pcj.ngn40)
    ret_ngnmaster = pcj.get_new_ngn(pcj.ngnmaster)
    ret_ngn = (ret_ngn36, ret_ngn40, ret_ngnmaster)
    ret_rhevh36ngn = pcj.get_new_builds_by_collection(
        pcj.rhevh36ngn, rhevh67=False)
    ret_rhvh_iso = pcj.get_new_rhvh_iso(pcj.rhvh_iso)

    if ret6:
        for i in ret6:
            add_download_job(i['build_iso'])
            pcj.mark_downloaded_true(pcj.rhevh6, i['build_name'])

    if ret7:
        for i in ret7:
            add_download_job(i['build_iso'])
            pcj.mark_downloaded_true(pcj.rhevh7, i['build_name'])

    if ret_rhevh36ngn:
        for i in ret_rhevh36ngn:
            dst_dir = {
                "dir":
                "/var/www/builds/rhvh_ngn/squashimg/%s" % i['build_name']
            }
            add_download_job(i['build_update_rpm'], opts=dst_dir)
            add_download_job(i['build_squashfs_img'], opts=dst_dir)
            for ks in i['build_ks']:
                add_download_job(ks, opts=dst_dir)
            pcj.mark_downloaded_true(pcj.rhevh36ngn, i['build_name'])

    if retrma:
        for i in retrma:
            add_download_job(
                i['build_rpm_url'],
                opts={
                    "dir": "/var/www/builds/rhevm-appliance"
                })
            pcj.mark_downloaded_true(pcj.rhevma, i['build_name'])

    if ret_rhevm35:
        url_link = "http://bob.eng.lab.tlv.redhat.com%sel6/%s"
        for i in ret_rhevm35:
            links = i['build_links'].split(',')
            prefix = links[0]

            opts = {
                "dir":
                "/var/www/builds/rhevm/3.5/%s/el6" %
                prefix.rstrip('/').replace('/builds/', '')
            }

            for url in links[1:]:
                if url.startswith('rhevm-appliance') or url.endswith('.html'):
                    continue
                add_download_job(url_link % (prefix, url), opts)
                time.sleep(0.5)

            pcj.mark_downloaded_true(pcj.rhevm35, i['build_name'])
            pcj.update_rhevms_host_info('35', i['build_name'],
                                        i["build_pkg"].replace(
                                            '.noarch.rpm', ''))

    if ret_rhevm36:
        url_link = "http://bob.eng.lab.tlv.redhat.com%snoarch/%s"
        for i in ret_rhevm36:
            links = i['build_links'].split(',')
            prefix = links[0]

            opts = {
                "dir":
                "/var/www/builds/rhevm/%s" % prefix.rstrip('/').replace(
                    '/builds/', '')
            }

            for url in links[1:]:
                if url.startswith('rhevm-appliance'):
                    continue
                add_download_job(url_link % (prefix, url), opts)
                time.sleep(0.5)

            pcj.mark_downloaded_true(pcj.rhevm36, i['build_name'])
            pcj.update_rhevms_host_info('36', i['build_name'],
                                        i["build_pkg"].replace(
                                            '.noarch.rpm', ''))

    if ret_rhevm40:
        tower_cli = "/home/dracher/Projects/vEnvs/vScrapy/bin/tower-cli"

        for i in ret_rhevm40:
            os.system("%s job launch --job-template=25" % tower_cli)
            pcj.mark_downloaded_true(pcj.rhevm40, i['build_name'])

    for ngn in ret_ngn:
        if ngn:
            for i in ngn:
                opts = {
                    "dir":
                    "/var/www/builds/rhvh_ngn/squashimg/%s" % i['build_name']
                }
                add_download_job(i['ngn_iso_url'], opts)
                time.sleep(0.5)
                add_download_job(i['ngn_tools_url'], opts)
                time.sleep(0.5)
                add_download_job(i['ngn_squash_url'], opts)
                time.sleep(0.5)
                add_download_job(i['ngn_image_url'], opts)
                time.sleep(0.5)
                add_download_job(i['ngn_manifest_url'], opts)
                time.sleep(0.5)

                pcj.mark_downloaded_true(pcj.ngn36, i['build_name'])

                pcj.mark_downloaded_true(pcj.ngn40, i['build_name'])

                pcj.mark_downloaded_true(pcj.ngnmaster, i['build_name'])

    if ret_rhvh_iso:
        iso_url_tpl = ("http://download-ipv4.eng.brq.redhat.com/"
                       "devel/candidate-trees/{}/compose/RHVH/"
                       "x86_64/iso/{}-RHVH-x86_64-dvd1.iso")
        dst_dir = {"dir": "/var/www/builds/rhvh_ngn/iso/"}
        for i in ret_rhvh_iso:
            add_download_job(
                iso_url_tpl.format(i['build_name'], i['build_name']),
                opts=dst_dir)
            pcj.mark_downloaded_true(pcj.rhvh_iso, i['build_name'])

    if ret_rhevm42:
        for i in ret_rhevm42:
            send_mail(i.get('build_name'), i.get('build_status'))
            pcj.mark_downloaded_true(pcj.rhevm42, i['build_name'])
