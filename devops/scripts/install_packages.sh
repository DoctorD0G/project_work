#!/bin/sh
set -e

cd /opt/project/app

if [ "$DEV_ENV" = true ]
then
  poetry install --with dev --no-root
else
  poetry install --with prod --no-root
fi
