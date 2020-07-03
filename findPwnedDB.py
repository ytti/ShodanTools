#!/usr/bin/env python
# findPwnedDB.py
#
# Last update: 1/13/2020
#
# Added: 
#       CassandraDB support
#       Additional DBs
#       Docker XMR mining flags (Thanks Unit42!)
#       https://unit42.paloaltonetworks.com/graboid-first-ever-cryptojacking-worm-found-in-images-on-docker-hub/
#
# Dependencies:
# - shodan
#
# Installation:
# sudo easy_install shodan
#
# Usage:
# 1. Download a json.gz file from Shodan; either for specific DB solutions or "tag:database"
#    Example:
#       shodan download --limit -1 USA_DB country:US tag:database
#       OR
#       shodan download --limit -1 USA_DB country:US product:MongoDB
# 2. Run the tool on the file:
#        ./findPwnedDB.py USA_DB.json.gz
#
from sys import argv
import json
from shodan.helpers import iterate_files, get_ip

pwnedDBs = {'Attention', 'Backup1', 'trojan4', 'DB_HAS_BEEN_DROPPED', 'README_MISSING_DATABASES', 'README_YOU_DB_IS_INSECURE', 'abafaeeee/monero-miner', 'topkek112', 'your_data_has_been_backed_up', 'README', 'Backup2', 'crackit', 'docker.io/pocosow/centos:7.6.1810', 'How_to_restore', 'gakeaws/nginx:v8.9', 'jackposv2', 'ReadmePlease', 'WARNING_ALERT', 'REQUEST_YOUR_DATA', 'trojan3', 'docker.io/gakeaws/nginx:v8.9', 'jackposprivate12', 'JUST_READ_ME', 'DB_DELETED', 'kannix/monero-miner', 'WRITE_ME', 'pocosow/centos:7.6.1810', 'Warn', 'PLEASE_READ_ME_XYZ', 'Warning', 'PLEASE_README', 'DB_H4CK3D', 'WARNING', 'alpine', 'Readme', 'WE_HAVE_YOUR_DATA', 'readme', 'how_to_recover', 'PLEASE_READ', 'timonmat/xmr-stak-cpu', 'pleaseread', 'DB_DROPPED', 'warning', 'university_cybersec_experiment', 'PLEASE_READ_ME', 'jackposv1', 'NODATA4U_SECUREYOURSHIT', 'PLEASEREAD', 'gakeaws/nginx:v2.0', 'SECUREYOURSHIT', 'jackpos', 'trojan2', 'PLEASE_SECURE_THIS_INSTALLATION', 'trojan1', 'REQUEST_ME', 'please_read', 'DATA_HAS_BEEN_BACKED_UP', 'Aa1_Where_is_my_data', 'pleasereadthis', 'send_bitcoin_to_retrieve_the_data', 'hacked_by_unistellar', 'CONTACTME', 'RECOVER', 'db_has_been_backed_up', 'docker.io/gakeaws/nginx:v2.0', 'HACKED_BY_MARSHY', 'PWNED_SECURE_YOUR_STUFF_SILLY', 'RECOVERY', 'alina', 'docker.io/gakeaws/mysql:5.6', 'Backup3', 'gakeaws/mysql:5.6', 'jacpos', 'BACKUP_DB', 'arayan/monero-miner'}

for banner in iterate_files(argv[1:]):
    ip = get_ip(banner)
    org = banner['org']
    try:
        product = banner['product']
    except:
        pass
    try:
        key = None
        if product == "MongoDB":
            data = banner['data'].replace('MongoDB Server Information\n', '').split('\n},\n')[2]
            data = json.loads(data + '}')['databases']
            key = 'name'
        elif product == "Elastic":
            data = banner['elastic']['indices']
        elif product == "Cassandra":
            data = banner['cassandra']['keyspaces']
        elif product == "HDFS NameNode":
            data = banner['opts']['hdfs-namenode']['Files']
            key = 'pathSuffix'
        elif product == "CouchDB":
            data = banner['opts']['couchdb']['dbs']
        elif product == "Redis key-value store":
            data = banner['redis']['keys']['data']
        elif product == "Docker":
            data = banner['docker']['Containers']
            key = 'Image'
        else:
            continue

        for db in data:
            db = db[key] if key else db
            if db in pwnedDBs:
               print('{}:{}:{}:{}'.format(ip, org, db, product))
    except:
        pass
