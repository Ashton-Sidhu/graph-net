#!/bin/bash

docker pull docker.elastic.co/kibana/kibana:7.5.2
sudo sysctl -w vm.max_map_count=262144
cd elastic; docker-compose up -d;
docker run -d --link es03:elasticsearch -p 5601:5601 --restart always --net elastic_elastic docker.elastic.co/kibana/kibana:7.5.2

