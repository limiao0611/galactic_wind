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
    filen='RN_1500_'+str(i)+'/sb_1500'
    return filen

def _z_den_flux(field,data):
    return (data['density']*data['z-velocity'])


def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()
#   hot = ad.cut_region("obj['temperature']>3e4")
   cr0 =  ad.cut_region("obj['z']<0.06")
   cr =  cr0.cut_region("obj['z']>-0.06")
   cr_hot=cr.cut_region("obj['temperature']>3e4")
   cr_nothot=cr.cut_region("obj['temperature']<3e4")
   cr_warm = cr_nothot.cut_region("obj['temperature']>1e3")
#   print 'len(cr)=',len(cr['temperature'])
#   print 'len(cr_hot)=',len(cr_hot['temperature'])
#  print  'mean(cr_hot[z-velocity])', mean(cr_hot['z-velocity'])*ds.length_unit/ds.time_unit
#  print "cr['temperature']=", cr['temperature']  
   print >>f,i 
   ff_h=len(cr_hot['temperature'])*1.0/len(cr['temperature'])
   print >>f,ff_h
#   print >>f,'v_hot=', ( mean(cr_hot['z-velocity']) ).in_units('km/s')
 #  print >>f,'v_warm=',( mean(cr_warm['z-velocity'])).in_units('km/s')
#   print >>f,'z_den_flux=', mean(cr['z_den_flux'])
   print >>f,'-----------------------------------------------' 
  
#   prof = yt.create_profile(ad,'z','z_den_flux',units = {'z':'kpc'}, weight_field='cell_volume') 
#   z=prof.x.value
#   z_flux = prof['z_den_flux'].value

#   prof_hot = yt.create_profile(cr,'z','z_den_flux',units={'z':'kpc'},weight_field='cell_volume')
#   z_hot = prof_hot.x.value
#   z_hot_flux = prof_hot['z_den_flux'].value


   time=round(ds.current_time.in_units('Myr'),1)
#   cc = (i/1600., 0.4,0.2)
   cc=['g','r','c','m','y','k','orange','crimson','pink']
#   plt.plot(z,z_flux,label='t='+str(time)+'Myr',lw=2,c=cc[n])
#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n],label='cut_region')
   global n
   n=n+1
   global fvhot
   fvhot.append(ff_h)

n=0
fvhot=[]
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num = [3,4,5,6,7,8,9,10]
#num = [1000]
fig=plt.figure()
f1='cut_region_numbers_fvhot.dat'
f=open(f1,'a')
for i in num:
    see(i)

f.close()
#plt.plot([0,2.5],[0.015,0.015],':',label='SF rate',lw=3.5,c='blue')
#plt.xlim(0,3)
#plt.xlabel('')
plt.scatter(num,fvhot,s=60)
plt.ylabel('Midplane (|z|<300pc) f_V,hot')
#plt.yscale('log')
plt.ylim(0,1.)
plt.legend(loc=4)
    
plt.savefig('cut_region_fvhot'+str(num)+'.png')


