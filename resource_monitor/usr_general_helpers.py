import re
import pymongo
from settings import MONGO_URI, MONGO_DATABASE


def get_competent_version(body, tags=None):
    ovirt_node_pattern = re.compile(r'/(ovirt-node-\d.+.rpm)')
    vdsm_pattern = re.compile(r'/(vdsm-\d.+.rpm)')

    res1 = ovirt_node_pattern.findall(body)
    res2 = vdsm_pattern.findall(body)

    if res1:
        res1 = res1[0]
    else:
        res1 = "No oVirt-Node version found"
    if res2:
        res2 = res2[0]
    else:
        res2 = "No VDSM version found"

    return res1, res2


def get_all_names_from_db(collection_name, field_name):
    cli = pymongo.MongoClient(MONGO_URI)
    db = cli[MONGO_DATABASE]

    ret = [i['build_name']
           for i in db[collection_name].find({},
                                             projection=[field_name])]
    cli.close()

    return ret
