FROM alpine:latest

RUN apk add --no-cache bash curl

COPY setupscript.sh /setupscript.sh
COPY clickhouse-connect.json /clickhouse-connect.json

RUN chmod +x /setupscript.sh

CMD ["bash", "/setupscript.sh"]
