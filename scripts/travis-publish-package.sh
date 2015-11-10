#!/bin/bash
set -ex
tar --create ../openmensa-parsers_* | openssl enc -aes-256-cbc -e -pass env:TRANSFER_KEY > upload.bin
wget --post-file upload.bin --output-document=- http://apt.dxtt.de/travis-upload/openmensa-parsers
