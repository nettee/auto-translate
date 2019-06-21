#!/bin/bash

echo 'Setting proxy...'
export http_proxy=127.0.0.1:8118
export https_proxy=127.0.0.1:8118

echo 'Trying to connect translate.google.com ...'
wget -o /dev/null -q --delete-after --timeout=5 --tries=3 google.com 

if [ $? -ne 0 ]; then
    echo 'Failed to connect translate.google.com'
    exit 1
fi

python main.py $@

