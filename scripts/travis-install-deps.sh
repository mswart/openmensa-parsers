#!/bin/bash
set -ex
rm -f /etc/apt/sources.list.d/travis_ci_zeromq3-source.list
apt-get update -qq
apt-get install -qq python3 python3-bs4 uwsgi uwsgi-plugin-python3 uwsgi-plugin-http devscripts
