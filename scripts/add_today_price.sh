#!/bin/bash
# 매일 오후 4시에 실행하는 스크립트. 
source /root/42Stock/.env
export VIR_APP_KEY=$VIR_APP_KEY
export VIR_APP_SECRET=$VIR_APP_SECRET
export VIR_VTS=$VIR_VTS
/root/.local/share/virtualenvs/42Stock-r1nxr-dj/bin/python /root/42Stock/scripts/daily_data.py
