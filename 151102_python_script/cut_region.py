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
#   hot = ad.cut_region("obj['temperature']>3e4")
   cr =  ad.cut_region("obj['z']>0.3")
   cr_hot=cr.cut_region("obj['temperature']>3e4")
   cr_nothot=cr.cut_region("obj['temperature']<3e4")
   cr_warm = cr_nothot.cut_region("obj['temperature']>1e3")
#   print 'len(cr)=',len(cr['temperature'])
#   print 'len(cr_hot)=',len(cr_hot['temperature'])
#  print  'mean(cr_hot[z-velocity])', mean(cr_hot['z-velocity'])*ds.length_unit/ds.time_unit
#  print "cr['temperature']=", cr['temperature']  
   print >>f,i 
   print >>f,'f_Vhot=',len(cr_hot['temperature'])*1.0/len(cr['temperature'])
   print >>f,'v_hot=', ( mean(cr_hot['z-velocity']) ).in_units('km/s')
   print >>f,'v_warm=',( mean(cr_warm['z-velocity'])).in_units('km/s')
   print >>f,'z_den_flux=', mean(cr['z_den_flux'])
   print >>f,'-----------------------------------------------' 
  
   prof = yt.create_profile(ad,'z','z_den_flux',units = {'z':'kpc'}, weight_field='cell_volume') 
   z=prof.x.value
   z_flux = prof['z_den_flux'].value

#   prof_hot = yt.create_profile(cr,'z','z_den_flux',units={'z':'kpc'},weight_field='cell_volume')
#   z_hot = prof_hot.x.value
#   z_hot_flux = prof_hot['z_den_flux'].value


   time=round(ds.current_time.in_units('Myr'),1)
#   cc = (i/1600., 0.4,0.2)
   cc=['g','r','c','m','y','k','orange','crimson','pink']
   plt.plot(z,z_flux,label='t='+str(time)+'Myr',lw=2,c=cc[n])
#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n],label='cut_region')
   global n
   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num = [1400,1500,1600]
#num = [1000]
fig=plt.figure()
f1='cut_region_numbers.dat'
f=open(f1,'a')
for i in num:
    see(i)

f.close()
plt.plot([0,2.5],[0.015,0.015],':',label='SF rate',lw=3.5,c='blue')
#plt.xlim(0,3)
plt.xlabel('z [kpc]')
plt.ylabel('z-density flux  [Msun/kpc^2/yr]')
plt.yscale('log')
plt.legend(loc=4)
    
plt.savefig('cut_region'+str(num)+'.png')


