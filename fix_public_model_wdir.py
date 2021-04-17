"""
There was an erroneous minus sign in the postproc script
of the public model GRIB data. Fix it here.
"""

import glob
import numpy as np
import xarray as xr

def fix_gfs_nam_wind_direction(ds):
     ux = - np.sin(- ds['wind_dir'] * np.pi / 180)
     vx = - np.cos(- ds['wind_dir'] * np.pi / 180)
     ds['wind_dir'][:] = np.arctan2(- ux, - vx) * 180 / np.pi
     ds['wind_dir'][np.where(ds['wind_dir'] < 0)] += 360

for model in ['GFS', 'NAM']:
    filenames = glob.glob('processed_ncei/' + model + '/*')
    for filename in filenames:
        print('Fixing ', filename)
        ds = xr.open_dataset(filename)
        fix_gfs_nam_wind_direction(ds)
        ds.to_netcdf(filename[:-5], 'w', 'NETCDF4')
