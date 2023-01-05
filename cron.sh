#!/bin/bash
source "$(pwd)/env/bin/activate"
python "$(pwd)/src/manage.py" runcrons > "$(pwd)/cronjob.log"
