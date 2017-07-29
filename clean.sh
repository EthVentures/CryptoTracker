#!/bin/bash
docker stop cryptotracker_app_1 cryptotracker_kibana_1 cryptotracker_elasticsearch_1
docker rm cryptotracker_app_1 cryptotracker_kibana_1 cryptotracker_elasticsearch_1
docker-compose build && docker-compose up
