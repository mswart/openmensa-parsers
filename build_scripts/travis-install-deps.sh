#!/bin/bash
set -ex
apt-get update -qq
apt-get install -qq python3 python3-setuptools python3-bs4 python3-lxml python3-pytest python3-requests-mock uwsgi uwsgi-plugin-python3 devscripts debhelper
