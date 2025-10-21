from netCDF4 import Dataset
import matplotlib.pylab as plt
import numpy as np
import matplotlib
from mycolorpy import colorlist as mcp
from matplotlib import cm
import matplotlib.colors as colors

from datetime import datetime
import matplotlib

import matplotlib.pyplot as plt
import numpy as np

path="C:\\Users\\grzegorczyk\\AWACA\\COSP\\COSPv2.0\\driver\\data\\my_outputs\\"
plt.rcParams['font.size'] = 13

## ECMWF
from netCDF4 import Dataset
import csv

nc_file = "C:\\Users\\grzegorczyk\\AWACA\\COSP\\COSPv2.0\\driver\\data\\inputs\\UKMO\\cosp_input_um.nc"
nc_data = Dataset(nc_file, "r")

output_file = "C:\\Users\\grzegorczyk\\AWACA\\COSP\\COSPv2.0\\driver\\data\\my_outputs\\cosp_input_um_names.csv"
# Write to CSV
# Prepare list of (variable_name, standard_name)
variable_standard_list = []
for long_name in nc_data.variables:
    print(long_name)
    var = nc_data.variables[long_name]
    if 'long_name' in var.ncattrs():
        variable_standard_list.append((long_name, var.getncattr('long_name')))


with open(output_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Variable', 'Standard_Name'])  # Header
    writer.writerows(variable_standard_list)

print(f"Saved {len(variable_standard_list)} entries to {output_file}")

lon = nc_data.variables['lon'][:]
lat = nc_data.variables['lat'][:]
Alt = nc_data.variables['height'][:] #2d and probably terrain following coordinates
qv = nc_data.variables['qv'][:]
t = nc_data.variables['t'][:]
year = nc_data.variables['year'][:]
month = nc_data.variables['month'][:]
orography=nc_data.variables['orography'][:]
Reff=nc_data.variables['Reff'][:]
tca=nc_data.variables['tca'][:]#total cloud amount, cloud fraction ?
fl_ccsnow=nc_data.variables['fl_ccsnow'][:]#flux conv snow
fl_ccrain=nc_data.variables['fl_ccrain'][:]#flux conv rain
fl_lsgrpl=nc_data.variables['fl_lsgrpl'][:]#flux large scale graupel

fl_lssnow=nc_data.variables['fl_lssnow'][:]#flux large scale snow
fl_lsrain=nc_data.variables['fl_lsrain'][:]#flux large scale rain

mr_lsliq=nc_data.variables['mr_lsliq'][:] #mixing_ratio_large_scale_cloud_liquid
mr_lsice=nc_data.variables['mr_lsice'][:] #mixing_ratio_large_scale_cloud_ice

mr_ccice=nc_data.variables['mr_ccice'][:]# convective mixing ratio of cloud ice
mr_ccliq=nc_data.variables['mr_ccliq'][:]# convective mixing ratio of cloud liquid
# UKMO Feb 2007

# model_level_number = nc_data.variables['model_level_number'][:]
lon_mesh = np.tile(lon, (Alt.shape[0], 1))


from matplotlib.colors import ListedColormap, BoundaryNorm

# plot position
plt.figure('Vertical cross section profile', figsize=(10,4))
sc = plt.scatter(lon, lat, c=np.arange(1, len(lon)+1), cmap=custom_cmap, norm=norm)
plt.xlabel('lon')
plt.ylabel('lat')
plt.title('Vertical cross section profile')
plt.colorbar(sc, label='Data points')
indices_to_label = [100, 200, 300, 400,500,600,700,800,900,1000,1100,1200]  # choose your indices here
for i in indices_to_label:
    plt.text(lon[i], lat[i], str(i),
             fontsize=9, fontweight='bold',
             color='black',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig(path+"Cloud_fraction.png",dpi=600)
plt.show()




#Ice
plt.figure('Ice mixing ratios',figsize =(12,8))

plt.subplot(311)
plt.title("convective mixing ratio of cloud ice")
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000, mr_ccice*1000,cmap=cmap,vmax=0.5,vmin=0.01)  # Alt in km
plt.ylim(0,15)
plt.xlabel('Grid')
plt.ylabel('Altitude [km]')
plt.colorbar(label='Ice mixing ratio g kg-1')

plt.subplot(312)
plt.title('mixing_ratio_large_scale_cloud_ice')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000, mr_lsice*1000,cmap=cmap,vmax=0.5,vmin=0.01)  # Alt in km
plt.ylim(0,15)
plt.xlabel('Grid')
plt.ylabel('Altitude [km]')
plt.colorbar(label='Ice mixing ratio g kg-1')

plt.subplot(313)
plt.title('Total: conv + large scale ice')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000, mr_lsice*1000+mr_ccice*1000,cmap=cmap,vmax=0.5,vmin=0.01)  # Alt in km
plt.ylim(0,15)
plt.xlabel('Grid')
plt.ylabel('Altitude [km]')

plt.colorbar(label='Ice mixing ratio g kg-1')
plt.tight_layout()
plt.savefig(path+"Ice_mixing_ratios.png",dpi=600)

plt.show()

#Water

plt.figure('Liq mixing ratios',figsize =(12,8))

plt.subplot(311)
plt.title("convective mixing ratio of liquid cloud")
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000, mr_ccliq*1000,cmap=cmap,vmax=0.5,vmin=0.01)  # Alt in km
plt.ylim(0,15)
plt.xlabel('Grid')
plt.ylabel('Altitude [km]')
plt.colorbar(label='Ice mixing ratio g kg-1')

plt.subplot(312)
plt.title('mixing_ratio_large_scale_cloud_liquid')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000, mr_lsliq*1000,cmap=cmap,vmax=0.5,vmin=0.01)  # Alt in km
plt.ylim(0,15)
plt.xlabel('Grid')
plt.ylabel('Altitude [km]')
plt.colorbar(label='Ice mixing ratio g kg-1')

plt.subplot(313)
plt.title('Total: conv + large scale liquid water')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000, mr_lsliq*1000+mr_ccliq*1000,cmap=cmap,vmax=0.5,vmin=0.01)  # Alt in km
plt.ylim(0,15)
plt.xlabel('Grid')
plt.ylabel('Altitude [km]')

plt.colorbar(label='Ice mixing ratio g kg-1')
plt.tight_layout()
plt.savefig(path+"Water_mixing_ratios.png",dpi=600)
plt.show()





#Precipitation

plt.figure('Rain precipitation flux',figsize =(8,5))

plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000, fl_lsrain,cmap=cmap,vmin=10**-8,vmax=0.5*10**-3)  # Alt in km
plt.ylim(0,15)
plt.xlabel('Grid')
plt.ylabel('Altitude (km)')
plt.colorbar(label='Rain flux kg m^-2 s^-1')

plt.tight_layout()
plt.savefig(path+"Rain_flux.png",dpi=600)
plt.show()


# plot profiles
fl_ccsnow=nc_data.variables['fl_ccsnow'][:]#flux conv snow
fl_ccrain=nc_data.variables['fl_ccrain'][:]#flux conv rain
fl_lsgrpl=nc_data.variables['fl_lsgrpl'][:]#flux large scale graupel

fl_lssnow=nc_data.variables['fl_lssnow'][:]#flux large scale snow
fl_lsrain=nc_data.variables['fl_lsrain'][:]#flux large scale rain

mr_lsliq=nc_data.variables['mr_lsliq'][:] #mixing_ratio_large_scale_cloud_liquid
mr_lsice=nc_data.variables['mr_lsice'][:] #mixing_ratio_large_scale_cloud_ice







## Analyze outputs from cosp
nc_out = "C:\\Users\\grzegorczyk\\AWACA\\COSP\\COSPv2.0\\driver\\data\\my_outputs\\Output.nc"
nc_out = Dataset(nc_out, "r")
output_file = "C:\\Users\\grzegorczyk\\AWACA\\COSP\\COSPv2.0\\driver\\data\\my_outputs\\variable_out_standard_names.csv"

# Prepare list of (variable_name, standard_name)
variable_standard_list = []
for var_name in nc_out.variables:
    var = nc_out.variables[var_name]
    if 'standard_name' in var.ncattrs():
        variable_standard_list.append((var_name, var.getncattr('standard_name')))


# Write to CSV
with open(output_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Variable', 'Standard_Name'])  # Header
    writer.writerows(variable_standard_list)

print(f"Saved {len(variable_standard_list)} entries to {output_file}")



DBZ_cloudsat=np.array(nc_out.variables['dbze94'][:])
DBZ_cloudsat=np.array(nc_out.variables['dbze94'][:])
DBZ_cloudsat_cfad=np.array(nc_out.variables['cfadDbze94'][:])
clgrLidar532=np.array(nc_out.variables['clgrLidar532'][:])
cltgrLidar532=np.array(nc_out.variables['cltgrLidar532'][:])
atb532gr=np.array(nc_out.variables['atb532gr'][:])
DBZ_cloudsat[DBZ_cloudsat<-30]=np.nan
fontsize_title=15

cmap = plt.get_cmap('jet', 14)
cmap.set_under('white')
vmin_x = -30
vmax_x = 20

plt.figure('Cloudsat Radar DBZ (Mean over subcolumns)',figsize =(15,5))
plt.title('Nan mean cloudsat reflectivity')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0][::-1]/1000,np.nanmean(DBZ_cloudsat,1),cmap=cmap,vmax=30,vmin=-30)  # Alt in km
plt.ylim(0,18)
plt.colorbar(label='Cloudsat Reflectivity (dBZ)')
plt.tight_layout()
plt.savefig(path+"Cloudsat_reflectivity.png",dpi=600)
plt.show()



plt.figure('Cloudsat Radar DBZ (Mean over subcolumns)',figsize =(15,5))
plt.title('Nan mean cloudsat reflectivity')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0][::-1]/1000,DBZ_cloudsat[:,np.int16(np.random.random(1236)*100),:],cmap=cmap,vmax=30,vmin=-30)  # Alt in km
plt.ylim(0,18)
plt.colorbar(label='Cloudsat Reflectivity (dBZ)')
plt.tight_layout()
plt.savefig(path+"Cloudsat_reflectivity.png",dpi=600)
plt.show()



#LIDAR! cloud area fraction

plt.figure('Ground_lidar_cloud_area_fraction',figsize =(15,5))
plt.title('Lidar cloud area fraction')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0][::-1]/1000,clgrLidar532,cmap=cmap,vmin=0,vmax=100)  # Alt in km
plt.ylim(0,18)
plt.colorbar(label='Cloud_area_fraction')
plt.xlabel('Grid')
plt.ylabel('Altitude (km)')
plt.tight_layout()
plt.savefig(path+"Ground_lidar_cloud_area_fraction.png",dpi=600)
plt.show()


# Cloud cover
plt.figure('Ground_lidar_cloud_cover',figsize =(15,5))
plt.title('Lidar cloud cover')
plt.plot(np.arange(0,len(cltgrLidar532),1),cltgrLidar532)
plt.tight_layout()
plt.xlabel('Grid points')
plt.ylabel('Cloud cover')
plt.tight_layout()
plt.savefig(path+"Ground_lidar_cloud_cover.png",dpi=600)
plt.show()

#Beta lidar
cmap = plt.get_cmap('jet', 14)
cmap.set_under('white')
colors.LogNorm(vmin=10**-2,vmax=1)


import matplotlib.colors as colors

plt.figure('Ground_lidar_cloud_area_fraction',figsize =(15,5))
plt.title('Lidar attenuated backscatter coefficient')
plt.pcolor(np.arange(0,len(lon),1), Alt[:,0]/1000,np.mean(atb532gr,1),cmap=cmap,norm=colors.LogNorm(vmin=10**-8,vmax=10**-4))  # Alt in km
plt.ylim(0,15)
plt.colorbar(label='Attenuated backscatter coefficient')
plt.xlabel('Grid')
plt.ylabel('Altitude (km)')
plt.tight_layout()
plt.savefig(path+"Ground_lidar_beta.png",dpi=600)
plt.show()



## Data vs cosp

grid_pt=1044-4
grid_pt=471-10-15

plt.figure('Rain profile',figsize =(8.5,8.5))

plt.subplot(221)
plt.title("Cloud fraction")
plt.plot(tca[:,grid_pt],Alt[:,0]/1000)
plt.ylabel('Altitude (km)')
plt.xlabel('Cloud fraction')
plt.ylim(0,15)
plt.xlim(0,1)

plt.subplot(222)
plt.title("Mixing ratios")
plt.plot(mr_ccice[:,grid_pt]*1000,Alt[:,0]/1000,color='b',linestyle='--',label="conv ice cloud")
plt.plot(mr_ccliq[:,grid_pt]*1000,Alt[:,0]/1000,color='r',linestyle='--',label="conv liquid cloud")
plt.plot(mr_lsliq[:,grid_pt]*1000,Alt[:,0]/1000,color='r',label="Large scale liquid cloud")
plt.plot(mr_lsice[:,grid_pt]*1000,Alt[:,0]/1000,color='b',label="Large scale ice cloud")
plt.legend()
plt.ylabel('Altitude (km)')
plt.xlabel('Mixing ratio (g kg-1)')
plt.ylim(0,15)

plt.subplot(223)
plt.title("Rain flux")
plt.plot(fl_lsrain[:,grid_pt],Alt[:,0]/1000,color='orange',label="Large scale rainflux")
plt.ylabel('Altitude (km)')
plt.xlabel('Rain flux (kg m^-2 s^-1)')
plt.legend()
plt.ylim(0,15)
plt.xlim(0,1.1*np.max(fl_lsrain[:,grid_pt]))

plt.subplot(224)
plt.title("Relfectivity subcolumns")
plt.pcolormesh(np.arange(len(DBZ_cloudsat[0,:,grid_pt])),Alt[:,0][::-1]/1000, DBZ_cloudsat[:,:,grid_pt],vmax=30,vmin=-30,cmap=cmap)
plt.ylabel("Altitude (km)")
plt.xlabel('Subcolumn number')
plt.colorbar(label='Cloudsat Reflectivity (dBZ)')
plt.ylim(0,15)

plt.tight_layout()
plt.savefig(path+"Rain_and_cloud profile"+str(lat[grid_pt])+"deg_"+str(grid_pt)+"_grid_pt"+".png",dpi=600)
plt.show()

#beta subcolumns
plt.figure('Beta subcolum profile',figsize =(6,5))
plt.title("Relfectivity subcolumns")
plt.pcolormesh(np.arange(len(DBZ_cloudsat[0,:,grid_pt])),Alt[:,0]/1000, atb532gr[:,:,grid_pt],cmap=cmap,norm=colors.LogNorm(vmin=10**-8,vmax=10**-4))
plt.ylabel("Altitude (km)")
plt.xlabel('Subcolumn number')
plt.colorbar(label='Cloudsat Reflectivity (dBZ)')
plt.ylim(0,15)

plt.tight_layout()
plt.savefig(path+"Beta_subgrid_"+str(lat[grid_pt])+"deg_"+str(grid_pt)+"_grid_pt"+".png",dpi=600)
plt.show()
