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
    filen='RN_1500_'+str(i)+'/sb_1500'
    if (i==11):
       filen='RN_1460_'+str(i)+'/sb_0146'
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
   dz= 0.02
   z1=-0.5
   z2 = z1+dz
   while (z2<0.5):
     bx=ds.box([0,0,z1],[0.1,0.1,z2])
     total_vol = bx.quantities.total_quantity('cell_volume')
     hot = bx.cut_region("obj['temperature']>3e4")
     hot_vol = hot.quantities.total_quantity('cell_volume')
     fh= hot_vol*1.0/total_vol
     fvh.append(fh)
     z.append((z1+z2)/2.*5)   
     z1=z1+dz
     z2=z1+dz


   time=round(ds.current_time.in_units('Myr'),1)
#   cc = (i/1600., 0.4,0.2)
   cc=['g','r','c','m','y','k','orange','crimson','pink']
   ln='T1-CR1-k2'+str(i)
   if (i==3):
      ln = 'T0-CR1-k27'    
   if (i==4):
      ln = 'T0-CR1-k28'
   if (i==5):
      ln = 'T1-CR1-k0'
   if (i==9):
      ln = 'T1-CR0-ZEUS'
   if (i==10):
      ln = 'T1-CR0-PPM'
   if (i==11):
      ln='T1-CR0-ZEUS-2pc'
   plt.plot(z,fvh,label=ln,lw=2,c=cc[n])
#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n])
   global n
   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num = [5,6,7,8,9,11,10]
#num = [1000]
fig=plt.figure()
for i in num:
    see(i)

#plt.plot([0,2.5],[0.015,0.015],':',label='SF rate',lw=3.5,c='blue')
#plt.xlim(0,3)
plt.xlabel('z [kpc]')
plt.ylabel('f_V,hot')
#plt.yscale('log')
plt.ylim(0,1)
#plt.legend(loc=1)
plt.legend(loc='best', fancybox=True, framealpha=0.4)

plt.savefig('z_fvhot_across_5kpc_fancy'+str(num)+'.png')


