#!/bin/bash
jq --arg user ${CLICKHOUSE_USER} --arg pass ${CLICKHOUSE_PASSWORD} \
   '.config.username = $user | .config.password = $pass' clickhouse-connect.json > temp-clickhouse-connect.json

until $(curl --output /dev/null --silent --head --fail http://localhost:8083/connectors); do
  sleep 5
done

curl -X POST -H 'Content-Type: application/json' \
  --data @temp-clickhouse-connect.json \
  http://localhost:8083/connectors
