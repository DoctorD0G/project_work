#!/bin/sh

#### Инжектим меременные среды в /usr/share/nginx/html/assets/config.js
TARGET_PATH=/usr/share/nginx/html/assets/config.js
VARS=$(env | grep VITE_)

CONTENT="var config = (() => ({"

for var in ${VARS}
do
    CONTENT=${CONTENT}$(echo ${var} | awk -F'=' '{ printf $1; printf ":\""; printf $2; printf "\","; next }1' -)
done

CONTENT="${CONTENT} }))();"
echo ${CONTENT} > ${TARGET_PATH}

nginx -g 'daemon off;'
