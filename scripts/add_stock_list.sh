#!/bin/bash
source /root/42Stock/.env
export VIR_APP_KEY=$VIR_APP_KEY
export VIR_APP_SECRET=$VIR_APP_SECRET
export VIR_VTS=$VIR_VTS
/root/.local/share/virtualenvs/42Stock-r1nxr-dj/bin/python /root/42Stock/dart/dart_code.py
