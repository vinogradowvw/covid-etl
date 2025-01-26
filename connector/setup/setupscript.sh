#!/bin/bash

until $(curl --output /dev/null --silent --head --fail http://localhost:8083/connectors); do
  sleep 5
done

curl -X POST -H 'Content-Type: application/json' \
  --data @clickhouse-connect.json \
  http://localhost:8083/connectors
