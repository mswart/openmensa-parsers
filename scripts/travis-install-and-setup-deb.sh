#!/bin/bash
set -ex
dpkg -i ../*.deb
echo "    http: 127.0.0.1:9090" >> /etc/uwsgi/apps-enabled/openmensa-parsers.yml
/etc/init.d/uwsgi restart openmensa-parsers
