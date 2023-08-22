import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *
#import yt.units.yt_array.YTArray

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
#   cr =  ad.cut_region("obj['z']>0.3")
   cr_hot=ad.cut_region("obj['temperature']>3e4")
   cr_shocked=ad.cut_region("obj['z-velocity']>1e-6")
#   cr_nothot=cr.cut_region("obj['temperature']<3e4")
#   cr_warm = cr_nothot.cut_region("obj['temperature']>1e3")
   N_hot=len(cr_hot['temperature'])
   R_hot=(3*N_hot/4/3.14)**0.3333333*500./256
   N_shocked = len(cr_shocked['temperature'])
   R_shocked = (3*N_shocked/4/3.14)**0.3333333*500./256

   time=round(ds.current_time.in_units('Myr'),3)

   print >>f,"%d	%f	%f	%f"%(i,time,R_hot,R_shocked)

#   print >>f,i 
#   print >>f,'f_Vhot=',len(cr_hot['temperature'])*1.0/len(cr['temperature'])
#   print >>f,'v_hot=', ( mean(cr_hot['z-velocity']) ).in_units('km/s')
#   print >>f,'v_warm=',( mean(cr_warm['z-velocity'])).in_units('km/s')
#   print >>f,'z_den_flux=', mean(cr['z_den_flux'])
#   print >>f,'-----------------------------------------------' 


   global n
   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num = range(100,900,100)
num = [1,5,10]+range(20,100,20)+ range(100,900,100)
#num = [1000]
f1='R_hot_R_shocked_vs_time.dat'
f=open(f1,'a')
for i in num:
    see(i)

f.close()

