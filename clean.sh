#!/bin/bash
docker stop cryptotrack_app_1 cryptotrack_kibana_1 cryptotrack_elasticsearch_1
docker rm cryptotrack_app_1 cryptotrack_kibana_1 cryptotrack_elasticsearch_1
docker-compose build && docker-compose up
