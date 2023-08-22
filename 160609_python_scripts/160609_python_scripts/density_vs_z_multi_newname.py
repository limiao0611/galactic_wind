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
    return filen

def _z_den_flux(field,data):
    return (data['density']*data['z-velocity'])


def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()
#   hot = ad.cut_region("obj['temperature']>3e4")
   
   prof = yt.create_profile(ad,'z','density',units = {'z':'kpc'}, weight_field='cell_volume') 
   z=prof.x.value
   z_flux = prof['density'].value

#   prof_hot = yt.create_profile(hot,'z','z_den_flux',units={'z':'kpc'},weight_field='cell_volume')
#   z_hot = prof_hot.x.value
#   z_hot_flux = prof_hot['z_den_flux'].value


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
      ln = 'T1-CR0'
   if (i==10):
      ln = 'T1-CR0-PPM'
   plt.plot(z,z_flux,label=ln,lw=2,c=cc[n])
#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n])
   global n
   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')


def n_HI(z):
    return 0.57*( 0.7*exp( -(z/0.127)**2 ) +0.19*exp( -(z/0.318)**2) + 0.11*exp(-abs(z)/0.413 ) )*1.67e-24
def n_HII(z):
    return 0.014*exp(-abs(z)/1.4)*1.67e-24
def n_all(z):
    return n_HI(z)+n_HII(z)
n_Hi=[]
n_tot=[]
z1=arange(0.05,2.5,0.05)
for i in range(len(z1)):
   n_Hi.append(n_HII(z1[i]))
   n_tot.append(n_all(z1[i]))

num = [3,4,5,6,7,8,10]
#num = [1000]
fig=plt.figure()
for i in num:
    see(i)

#plt.plot([0,2.5],[0.015,0.015],':',label='SF rate',lw=3.5,c='blue')
#plt.xlim(0,3)

plt.plot(z1,n_tot,'--',lw=2,color='purple',label='MW H_all')
plt.plot(z1,n_Hi,':',lw=2,color='purple',label='MW HII')
plt.xlabel('z [kpc]')
plt.ylabel('density  [g/cm^3]')
plt.yscale('log')
#plt.ylim(1e-3,1)
plt.legend(loc=1)
    
plt.savefig('density_vs_z_across'+str(num)+'.png')


