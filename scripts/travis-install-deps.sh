#!/bin/bash
set -ex
apt-get update -qq
apt-get install -qq python3 python3-bs4 uwsgi uwsgi-plugin-python3 uwsgi-plugin-http devscripts
