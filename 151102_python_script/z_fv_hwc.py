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
   fvw=[]
   fvc=[]
   z=[]
   dz= 0.04
   z1=-0.5
   z2 = z1+dz
   fn='fv_hwc_'+str(i)+'.dat'
   f=open(fn,'w')

   while (z2<=0.5):
     bx=ds.box([0,0,z1],[0.1,0.1,z2])
     total_vol = bx.quantities.total_quantity('cell_volume')

     hot = bx.cut_region("obj['temperature']>3e5")
#     warm = (bx.cut_region("obj['temperature']<3e5")).cut_region("obj['temperature']>1e3")
     cold = bx.cut_region("obj['temperature']<1e3")

     hot_vol = hot.quantities.total_quantity('cell_volume')
#     warm_vol = warm.quantities.total_quantity('cell_volume')
     cold_vol = cold.quantities.total_quantity('cell_volume')
     #warm_vol=1.-hot_vol - cold_vol

     fh= hot_vol*1.0/total_vol
     fvh.append(fh)

     fc= cold_vol*1.0/total_vol
     fvc.append(fc)

     fw= 1-fh-fc
     fvw.append(fw)



     z.append((z1+z2)/2.*5)
     z1=z1+dz
     z2=z1+dz
     print >> f, (z1+z2)/2.*5, fh,fw,fc

   time=round(ds.current_time.in_units('Myr'),1)
#   cc = (i/1600., 0.4,0.2)
#   cc=['g','r','c','m','y','k','orange','crimson','pink']
   fig=plt.figure()
   plt.plot(z,fvh,'-',lw=2,c='r',label='T>3e5K')
   plt.plot(z,fvw,'-',color='orange',lw=2,label='1e3<T<3e5K')
   plt.plot(z,fvc,'-',color='blue',lw=2,label='T<1e3K')
   plt.title(str(time)+ 'Myr' )
   plt.xlabel('z [kpc]')
   plt.ylabel('f_V,hot')
   plt.legend(loc='best', fancybox=True, framealpha=0.4)
#plt.yscale('log')
   plt.ylim(0,1)
   plt.savefig('z_fv_hwc_'+str(i)+'.png')

#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n])
   global n
   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num=[180,200,220,240]
for i in num:

