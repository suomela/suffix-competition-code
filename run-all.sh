#!/bin/bash

set -e

git submodule init
git submodule update

cd type-ratio
./build.sh
cd ..
