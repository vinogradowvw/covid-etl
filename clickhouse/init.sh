#!/bin/bash

clickhouse-client -u ${CLICKHOUSE_ADMIN_USER} --password ${CLICKHOUSE_ADMIN_PASSWORD} --query="CREATE DATABASE IF NOT EXISTS covid;"

clickhouse-client -u ${CLICKHOUSE_ADMIN_USER} --password ${CLICKHOUSE_ADMIN_PASSWORD} --query="CREATE TABLE IF NOT EXISTS covid.covid (
    date DateTime,
    cases Int32,
    deaths Int32
) ENGINE = MergeTree()
ORDER BY date;"
