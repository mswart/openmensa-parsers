#!/bin/bash
set -ex
debi
echo "  http: 127.0.0.1:9090" >> /etc/uwsgi/apps-enabled/openmensa-parsers.yml
/etc/init.d/uwsgi restart openmensa-parsers
