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

   fmw=[]
   fmh=[]
   z=[]
   dz= 0.02
   z1=-1.0
   z2 = z1+dz
   while (z2<1.0):
     bx=ds.box([0,0,z1],[0.1,0.1,z2])
     total_mass = bx.quantities.total_quantity('cell_mass')
     hot = bx.cut_region("obj['temperature']>3e4")
     not_hot = bx.cut_region("obj['temperature']<3e4")
     warm = not_hot.cut_region("obj['temperature']>5e2")

     hot_mass = hot.quantities.total_quantity('cell_mass')
     warm_mass = warm.quantities.total_quantity('cell_mass')
#     warm_mass1 = warm.total_mass()
     hot_mass2 = sum(hot['cell_mass'])
     warm_mass2 = sum(warm['cell_mass'])
 
     fm_h = hot_mass2*1.0/total_mass
     fm_w = warm_mass2*1.0/total_mass
     
     fmh.append(fm_h)
     fmw.append(fm_w)
     z.append((z1+z2)/2.*5)   
     z1=z1+dz
     z2=z1+dz
     print >>f, (z1+z2)/2.*5,hot_mass,hot_mass2,warm_mass,warm_mass2,total_mass, fm_h,fm_w
   print >>f ,'--------------------------------'

   time=round(ds.current_time.in_units('Myr'),1)
#   cc = (i/1600., 0.4,0.2)
   cc=['g','r','c','m','y','k','orange','crimson','pink']
   plt.plot(z,fmh,label=str(time)+'Myr hot',lw=2,c=cc[n])
#   plt.plot(z,fmw,'--',lw=2,c=cc[n])

#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n])
   global n
   n=n+1



fn="mass_fraction.dat"
f=open(fn,'a')

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num = range(70,110,10)
num=[180,200,220,240]
#num = [1000]
fig=plt.figure()
for i in num:
    see(i)

#plt.plot([0,2.5],[0.015,0.015],':',label='SF rate',lw=3.5,c='blue')
#plt.xlim(0,3)
plt.xlabel('z [kpc]')
plt.ylabel('f_m,hot')
#plt.yscale('log')
plt.ylim(-0.1,1.1)
#plt.legend(loc=1)
plt.legend(loc='best', fancybox=True, framealpha=0.4)

plt.savefig('z_fm_5kpc_fancy'+str(num)+'.png')


