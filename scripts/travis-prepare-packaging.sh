#!/bin/bash
set -ex
export DEBEMAIL=packages@devtation.de
export DEBFULLNAME='Travis CI Build VM'
dch --distribution trusty --newversion=1.1+b$TRAVIS_BUILD_NUMBER-0 "Package commit `git log -1 --oneline $TRAVIS_COMMIT`"
sed -i '/Maintainer/a \
Uploaders: '"$DEBFULLNAME <$DEBEMAIL>" debian/control
