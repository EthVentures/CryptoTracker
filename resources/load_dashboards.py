#!/bin/env python

help = """
Load kibana dashboards or visualizations exported as json via the kibana ui on the command line.

Example:

    $ python load_dashboards.py objects_visualizations.json 'http://localhost:9200'
    Posting: Per-node-doc-count (visualization)
    {"_index":".kibana","_type":"visualization","_id":"Per-node-doc-count","_version":2,"_shards":{"total":1,"successful":1,"failed":0},"created":false}
    Posting: Thread-pool-bulk-rejected (visualization)
    {"_index":".kibana","_type":"visualization","_id":"Thread-pool-bulk-rejected","_version":2,"_shards":{"total":1,"successful":1,"failed":0},"created":false}
"""

import json
import commands
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description=help, formatter_class=RawTextHelpFormatter)
parser.add_argument('filename', action='store', help='The json file containing the object definitions.')
parser.add_argument('es_base_url', action='store', help='The base of the elasticsearch url to use, with auth included; e.g, "https://un:pw@localhost:9200"')
parser.add_argument('--fake', action='store_true', help='Set this flag to fake the upload and instead just list actions.')
options = parser.parse_args()

# Expects file to be a json array
with open(options.filename, 'r') as f:
    d = json.load(f)

full_url = "%s/.kibana" % (options.es_base_url)

for item in d:
    item_src = item['_source']
    print("Posting: %s (%s)" % (
        item['_id'],
        item['_type']
    ))
    if options.fake:
        continue
    print(commands.getoutput("""curl -s -k -X POST '%s/%s/%s' -d'%s' """ % (
        full_url,
        item['_type'],
        item['_id'],
        json.dumps(item_src)
    )))
