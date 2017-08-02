#!/bin/bash
curl -XPUT -D- 'http://localhost:9200/.kibana/index-pattern/eth.*.ticker' \
    -H 'Content-Type: application/json' \
    -d '{"title" : "eth.*.ticker", "timeFieldName": "tracker_time", "notExpandable": true}'


curl -XPUT -D- 'http://localhost:9200/.kibana/index-pattern/btc.*.ticker' \
        -H 'Content-Type: application/json' \
        -d '{"title" : "btc.*.ticker", "timeFieldName": "tracker_time", "notExpandable": true}'

curl -XPUT -D- 'http://localhost:9200/.kibana/index-pattern/*.*.ticker' \
        -H 'Content-Type: application/json' \
        -d '{"title" : "*.*.ticker", "timeFieldName": "tracker_time", "notExpandable": true}'

curl -XPUT -D- 'http://localhost:9200/.kibana/config/5.5.0' \
            -H 'Content-Type: application/json' \
            -d '{"defaultIndex": "eth.*.ticker"}'

python load_dashboards.py objects_visualizations.json 'http://localhost:9200'
