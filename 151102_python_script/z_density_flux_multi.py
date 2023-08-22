import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *


def get_fn(i):
    a0=''
    if (i<10):
      a0='000'
    if (10<=i<100):
      a0='00'
    if (100<=i<999):
      a0='0'
    filen='DD'+a0+str(i)+'/sb_'+a0+str(i)
    return filen

def _z_den_flux(field,data):
    return (data['density']*data['z-velocity'])


def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()
   
   prof = yt.create_profile(ad,'z','z_den_flux',units = {'z':'kpc'}, weight_field='cell_volume')
 
   z=prof.x.value
   z_flux = prof['z_den_flux'].value
   time=round(ds.current_time.in_units('Myr'),1)
   plt.plot(z,z_flux,label='t='+str(time)+'Myr',lw=2)

yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num = [100,400,700,1000,1300,1500]
fig=plt.figure()
for i in num:
    see(i)

plt.plot([0,2.5],[0.015,0.015],'--',label='SF rate',lw=2.5)
plt.xlabel('z [kpc]')
plt.ylabel('z-density flux  [Msun/kpc^2/yr]')
plt.yscale('log')
plt.legend(loc=4)
    
plt.savefig('z_den_flux_evolution'+str(num)+'.png')


