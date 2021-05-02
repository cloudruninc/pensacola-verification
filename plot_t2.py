from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from netCDF4 import Dataset
import numpy as np
import os

cities = {
    'Pensacola': (30.4737409,-87.1888577)
}

plt.rcParams.update({'font.size': 10})

start_time = datetime(2019, 11, 12, 0)
end_time = datetime(2019, 11, 26, 23)

init_time = start_time - timedelta(days=1)

filename = init_time.strftime('data/PNS_%Y%m%d%H/') + start_time.strftime('cloudrun_d01_%Y-%m-%d_%H:%M:%S.nc')

with Dataset('data/wrfout_d01_2019-11-11_00_00_00') as nc:
    xland = nc.variables['XLAND'][0,:,:]

with Dataset(filename) as nc:
    lon = nc.variables['longitude'][:,:]
    lat = nc.variables['latitude'][:,:]

time = start_time
while time <= end_time:
    init_time = time - timedelta(days=1)
    if init_time.hour >= 12:
        init_time = datetime(init_time.year, init_time.month, init_time.day, 12)
    else:
        init_time = datetime(init_time.year, init_time.month, init_time.day)
    print(init_time, time)
    filename = init_time.strftime('data/PNS_%Y%m%d%H/') + time.strftime('cloudrun_d01_%Y-%m-%d_%H:%M:%S.nc')
    with Dataset(filename) as nc:
        t2 = nc.variables['air_temperature_2m'][0,:,:] - 273.15
        t2 = np.clip(t2, 4.0001, 25.9999)

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111, aspect='equal', xlim=(np.min(lon) + 0.05, np.max(lon) - 0.05), ylim=(np.min(lat) + 0.05, np.max(lat) - 0.05))
    plt.contourf(lon, lat, t2, np.arange(4, 26.1, 0.1), cmap=cm.Spectral_r)
    colorbar = plt.colorbar(shrink=0.7, extend='both', ticks=range(5, 30, 5))
    plt.contour(lon, lat, xland, [1.5], colors='k', linewidths=0.5)
    for city in cities.keys():
        clat, clon = cities[city]
        plt.plot(clon, clat, 'k.', ms=5)
        plt.text(clon, clat, city, va='top', ha='left', fontsize=10)
    plt.xticks([])
    plt.yticks([])
    plt.title(r'2-m air temperature [$^o$C], ' + time.strftime('%Y-%m-%d %H%M UTC'))
    plt.text(0.02, -0.02, 'Cloudrun @ 1 km resolution (https://cloudrun.co)', va='top', ha='left', transform=ax.transAxes, fontsize=10)
    fig.subplots_adjust(left=0.05, bottom=0.0, right=1, top=1)
    plt.savefig('t2_' + time.strftime('%Y-%m-%d_%H:%M:%S') + '.png', dpi=300)
    plt.close(fig)
    
    time += timedelta(hours=1)
