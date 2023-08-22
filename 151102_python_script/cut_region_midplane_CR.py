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

def _CR_Energy_Density(field,data):
    return data['CREnergyDensity']* data.ds.mass_unit/data.ds.length_unit/data.ds.time_unit**2


def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()
#   hot = ad.cut_region("obj['temperature']>3e4")
   cr0 =  ad.cut_region("obj['z']<0.06")
   cr =  cr0.cut_region("obj['z']>-0.06")
#   cr_hot=cr.cut_region("obj['temperature']>3e4")
#   cr_nothot=cr.cut_region("obj['temperature']<3e4")
#   cr_warm = cr_nothot.cut_region("obj['temperature']>1e3")


#   print 'len(cr)=',len(cr['temperature'])
#   print 'len(cr_hot)=',len(cr_hot['temperature'])
#  print  'mean(cr_hot[z-velocity])', mean(cr_hot['z-velocity'])*ds.length_unit/ds.time_unit
#  print "cr['temperature']=", cr['temperature']  
   print >>f,i 
   e_CR= mean(cr['CR_Energy_Density'])
   e_std = std(cr['CR_Energy_Density'])
#len(cr_hot['temperature'])*1.0/len(cr['temperature'])
   print >>f,e_CR
   print >>f,e_std
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
   global eCR,estd
   eCR.append(e_CR)
   estd.append(e_std)


yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
yt.add_field('CR_Energy_Density',function=_CR_Energy_Density, units  = 'erg/cm**3')
n=0
eCR=[]
estd=[]
num = [3,4,5,6,7,8]
#num = [1000]
fig=plt.figure()
f1='cut_region_numbers_midplane_CR.dat'
f=open(f1,'a')
for i in num:
    see(i)

f.close()
#plt.plot([0,2.5],[0.015,0.015],':',label='SF rate',lw=3.5,c='blue')
#plt.xlim(0,3)
#plt.xlabel('')
num.append(9)
eCR.append(1e-16)
estd.append(1e-16)
#plt.scatter(num,eCR,s=60)
plt.errorbar(num,eCR,yerr=estd,fmt='o',ms=10)
e_obs=2.88e-12
plt.plot([2,10],[e_obs,e_obs],'g--',label='obs: >~ 1.8ev/cc',lw=2.5)
plt.arrow(7,e_obs,0.,7e-13,head_width=0.05,head_length=1e-13, ec='g',fc='g')
plt.ylabel('Midplane (|z|<300pc) e_CR [erg/cm^3]')
plt.yscale('log')
plt.xlim(2,10)
plt.ylim(3e-13,8e-12)
plt.legend(loc=1)
    
plt.savefig('cut_region_midplane_CR'+str(num)+'.png')


