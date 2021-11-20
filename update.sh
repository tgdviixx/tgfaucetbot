#!/bin/sh
. ./n
GIT_LOC=https://github.com/tgdviixx/tgfaucetbot
VERSION=$(cat version)
increment_version $VERSION > version
VERSION=$(cat version)
gitpush

