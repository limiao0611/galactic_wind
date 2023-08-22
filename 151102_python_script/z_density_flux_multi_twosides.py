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
#   T0=3e4
#   hot = ad.cut_region("obj['temperature']>3e4")
#   print 'total_quantities=',ad.quantities.total_quantity('temperature')

   fvh=[]
   z=[]
   z_flux=[]
   z_flux_hot=[]
   dz= 0.02
   z1=-0.5
   z2 = z1+dz
   fn='z_den_flux_'+str(i)+'.dat'
   f=open(fn,'w')

   while (z2<=0.5):
     bx=ds.box([0,0,z1],[0.03,0.03,z2])
     hot = bx.cut_region("obj['temperature']>3e4")
     zflux = bx.quantities.weighted_average_quantity('z_den_flux','cell_volume')
     zflux_hot = hot.quantities.weighted_average_quantity('z_den_flux','cell_volume')
     z_flux.append(zflux)
     z_flux_hot.append(zflux_hot)
     z.append((z1+z2)/2.*5)   
     z1=z1+dz
     z2=z1+dz
     print >> f, (z1+z2)/2.*5, zflux, zflux_hot

   time=round(ds.current_time.in_units('Myr'),1)
#   cc = (i/1600., 0.4,0.2)
   cc=['g','r','c','m','y','k','orange','crimson','pink']
   plt.plot(z,z_flux,label=str(time)+'Myr',lw=2,c=cc[n])
   plt.plot(z,z_flux_hot,label='T>3e4 K')
#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n])
   global n
   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num=[200,250,300,360]
#num = [1000]
fig=plt.figure()
for i in num:
    see(i)

plt.xlabel('z [kpc]')
plt.ylabel('z_den_flux [Msun/yr/kpc**2]')
#plt.yscale('log')
plt.ylim(-0.2,0.2)
#plt.legend(loc=1)
plt.legend(loc='best', fancybox=True, framealpha=0.4)

plt.savefig('z_den_flux_twosides_1_'+str(num)+'.png')


