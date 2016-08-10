#!/home/dracher/Projects/vEnvs/vScrapy/bin/python
# -*- coding: utf-8 -*
import os
import re
import sys
import logging
import logging.config
import glob
import subprocess as sp
import pymongo
import yaml
import time
from mongohelper import MongoHelper

KS_MAUAUL_TPL = '''
liveimg --url=%s

graphical

'''

KS_AUTO_TPL = '''
liveimg --url=%s

clearpart --all

autopart --type=thinp

rootpw --plaintext redhat

timezone --utc Asia/Harbin

zerombr

text

reboot

%%post --erroronfail
imgbase layout --init
imgbase --experimental volume --create /var 4G
%%end

'''

KSM = '/var/www/builds/rhevh/ngn/latest/ngm.ks'
KSN = '/var/www/builds/rhevh/ngn/latest/ngn.ks'

PATH_PREFIX = '/var/www/builds'

log_conf = yaml.load(open('/etc/py_logger.yml'))
logging.config.dictConfig(log_conf['logging'])

log = logging.getLogger('aria2_hook')
m = MongoHelper()


def build_tag(x, y):
    log.debug('with params %s %s' % (x, y))

    ret = None
    if x.startswith('6'):
        ret = m.rhevh6.find_one({'build_name': y})
        m.rhevh6.update_one({'build_name': y}, {'$set': {'build_downloaded': True}})
    if x.startswith('7'):
        ret = m.rhevh7.find_one({'build_name': y})
        m.rhevh7.update_one({'build_name': y}, {'$set': {'build_downloaded': True}})

    pattern = re.compile(r'-(\d.\d)-')
    tag = '00'
    if ret:
        tag = pattern.findall(ret['build_tag'])
        if tag:
            log.info('return %s' % tag)
            tag = tag[0]

    return tag


def prepare_dir(name, name_trim):
    dir1 = 'rhevh'
    dir2, dir3 = name_trim.split('-')[-2:]
    log.debug('name, name_trim are %s, %s' % (name, name_trim))

    tag = build_tag(dir2, name_trim)

    dest = os.path.join(PATH_PREFIX, dir1, dir2, '%s-%s' % (dir3, tag))
    log.debug('dest is %s' % dest)

    os.system('mkdir -p %s' % dest)

    return dest, name.endswith('rpm')


def make_pxe(src, dest, pxe):
    log.info('start to making pxe profile')
    os.system('mv %s %s' % (src, dest))

    if pxe:
        os.chdir(dest)
        sp.call('rpm2cpio *.rpm | cpio -idmv', shell=True)
        sp.call('find . -name "*.iso" | xargs mv -t .', shell=True)

        r = glob.glob('r*.iso')
        if len(r) == 1:
            sp.call('sudo livecd-iso-to-pxeboot %s' % os.path.join(dest, r[0]), shell=True)
            a = dest.rstrip('/').split('/')
            a1, a2 = a[-2], a[-1]
            sp.call('/home/dracher/bin/createpxe.sh %s %s' % (a1, a2), shell=True)


def rhevh_action(build):
    build_name = os.path.basename(build)

    build_name_trim = build_name.replace('.noarch.rpm', '').replace('.iso', '')

    dest, pxe = prepare_dir(build_name, build_name_trim)

    make_pxe(build, dest, pxe)


def rhevh_ngn36_action(build):

    http_link = 'http://10.66.10.22:8090/rhevh/rhevh7-ng-36/%s/%s'
    

    tmp = build.split('/')
    link = http_link % (tmp[-2], tmp[-1])
    log.debug("squashfs link is %s", link)
    ks_manual = KS_MAUAUL_TPL % link
    ks_auto = KS_AUTO_TPL % link

    with open(KSM, 'w') as fp:
        fp.write(ks_manual)

    with open(KSN, 'w') as fp:
        fp.write(ks_auto)

    

def rhevh_ngn36_update_action(build):
    updates_rpm_dir = '/var/www/builds/rhvhupgrade/updates'
    build_name = os.path.basename(build)
    update_repo_dir = '/var/www/builds/rhvhupgrade/rhvh/4/os/Packages'

    update_rpm_path = os.path.join(updates_rpm_dir, build_name)

    cmd = 'mv %s %s' % (build, updates_rpm_dir)
    log.debug("run cmd: %s", cmd)
    sp.call(cmd, shell=True)

    os.chdir(update_repo_dir)
    cmd2 = "ln -sf %s redhat-virtualization-host-image-update-latest.rpm" % update_rpm_path
    sp.call(cmd2, shell=True)
    sp.call('rm -rf repodata && createrepo .', shell=True)


def rhevma_action(build):
    build_name = os.path.basename(build)
    version = '00'
    ret = m.rhevm_appliance.find_one({'build_rpm_url': re.compile(build_name)})
    if ret:
        version = re.findall(r'-(\d\.\d)-', ret['build_tag'])[0]

    log.debug('version is %s' % version)

    build_new = build_name.replace('rhevm-appliance-', '').replace('.x86_64', '').replace('noarch', version)
    log.debug('new rhevma build name is %s' % build_new)

    renamed_build = os.path.join(os.path.dirname(build), build_new)
    log.debug('new rhevma build full path is %s' % renamed_build)

    log.warning('start to renmae old build')
    os.system('mv %s %s' % (build, renamed_build))


def rhevm_action(build):
    """build e.g.:

    /var/www/builds/rhevm/3.5/vt18.3/el6/a.rpm
    /var/www/builds/rhevm/3.6/3.6.0-22/el6/b.rpm

    """
    log.debug('build is %s' % build)
    log.debug('%s' % build.strip().split('/'))

    version = build.strip().split('/')[-3]
    log.debug('version is %s' % version)

    ansible_playbook = '/home/dracher/Projects/vEnvs/vScrapy/bin/ansible-playbook'
    ansible_project = '/home/dracher/Projects/ansible-project/'

    cmd = 'at now + 1 min <<< "{ansible_playbook} -e rhevm35_version=\'{ver35}\' ' \
          '-e rhevm36_version=\'{ver36}\'  -i /home/dracher/bin/rhevmhosts ' \
          '{ansible_project}pb_upgrade_rhevm_{ver}.yml"'

    # the biggest rpm      
    check = 'jasperreports' in build

    if check:
        log.info("all rhevm packages have been downloaded")
        log.warning('>' * 40)
        log.warning("%s" % build.strip().split('/'))
        sp.call("/usr/bin/createrepo %s" % os.path.dirname(build), shell=True)

        if '3.5' in build:
            cmd_ = cmd.format(ansible_playbook=ansible_playbook,
                              ver35=version, ver36='',
                              ansible_project=ansible_project,
                              ver=35)
            log.debug('cmd_ is %s' % cmd_)
            sp.call(cmd_, shell=True, executable='/bin/bash')
        if '3.6' in build:
            cmd_ = cmd.format(ansible_playbook=ansible_playbook,
                              ver35='', ver36=version,
                              ansible_project=ansible_project,
                              ver=36)
            log.debug('cmd_ is %s' % cmd_)
            sp.call(cmd_, shell=True, executable='/bin/bash')


if __name__ == '__main__':
    build = sys.argv[-1]
    log.debug('arg build is { %s }', build)

    try:
        os.remove(build + '.aria2')
    except OSError:
        log.warning("can not find .aria2 file")

    time.sleep(3)

    if 'tmppmt' in build:
        log.info('rhevh action start')
        rhevh_action(build)

    elif 'appliance' in build:
        log.info('rhevma action start')
        rhevma_action(build)

    elif 'rhevm' in build:
        log.info('rhevm action start')
        rhevm_action(build)

    elif build.endswith('squashfs'):
        log.info('rhevh ngn36 action start')
        rhevh_ngn36_action(build)

    elif "image-update" in build and build.endswith('.rpm'):
        log.info("rhevh_ngn36_update_action start")
        rhevh_ngn36_update_action(build)
    else:
        pass

    m.close()
