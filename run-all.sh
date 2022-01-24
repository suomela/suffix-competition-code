#!/bin/bash

set -e

git submodule init
git submodule update

cd type-ratio
./build.sh
cd ..

export PYTHONPATH=type-ratio

./calculate-100.py "$@"
./calculate-50.py "$@"
./calculate-legal.py "$@"
