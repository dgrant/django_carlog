#!/bin/sh
rm -rf env
virtualenv --distribute --no-site-packages env
env/bin/pip3 install -r requirements.txt
