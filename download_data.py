#!/usr/bin/env python3

"""
Downloads the Pensacola forecasts.
"""

from datetime import datetime, timedelta
import os
import subprocess

cwd = os.getcwd()

start_time = datetime(2019, 11, 11)
end_time = datetime(2019, 11, 26, 12)
time = start_time

while time <= end_time:
    
    forecast_name = time.strftime('PNS_%Y%m%d%H')
    dirname = 'data/' + forecast_name
    
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass
    
    os.chdir(dirname)
    
    subprocess.call(['cloudrun-downloader', '-nc', forecast_name])
    subprocess.call(['unzip', forecast_name + '_cloudrun.zip'])
    
    os.chdir(cwd)
    
    time += timedelta(hours=12)
