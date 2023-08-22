import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
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

SF_density = 10**-3.9

def _z_den_flux(field,data):
    return abs(data['density']*data['z-velocity'])

def _mass_loading(field,data):
    return abs(data['density']*data['z-velocity'])/SF_density


def see(i):
   profiles =[]
   labels=[]

   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()
   hot = ad.cut_region("obj['temperature']>3e4")
#   outflow = ((ad.cut_region("obj['z']<0.")).cut_region("obj['z-velocity']<0."))   and ((ad.cut_region("obj['z']>0")).cut_region("obj['z-velocity']>0."))


#   outflow_up = ((ad.cut_region("obj['z']>0")).cut_region("obj['z-velocity']>0."))
   outflow_up = ad.cut_region("obj['z-velocity']>0.")
   outflow_down = ad.cut_region("obj['z-velocity']<0.")


#   print outflow['z']
   profiles.append( create_profile(outflow_up,'z',['mass_loading'], units = {'z':'kpc'},weight_field='cell_volume',logs=None) )
   profiles.append( create_profile(outflow_down,'z',['mass_loading'], units = {'z':'kpc'},weight_field='cell_volume',logs=None) )
#   profiles.append( create_profile(outflow_up,'z',['z_den_flux'], weight_field=None,logs=None) )
#   prof = yt.create_profile(outflow,'z','z_den_flux',units = {'z':'kpc'}, weight_field=None,logs=None)
#   print prof.x
   labels.append('z-vel>0')
   labels.append('z-vel<0')
#   labels.append('z>0')
   plot =ProfilePlot.from_profiles(profiles=profiles , labels=labels)
   plot.x_log=False
   plot.set_xlim(-2.5,2.5)
#   plot.y_title='Mass loading'
   plot.save('mass_loading_net'+str(i)+'.png')

#   z=prof.x.value
#   z_flux = prof['z_den_flux'].value
#   prof_hot = yt.create_profile(hot,'z','z_den_flux',units={'z':'kpc'},weight_field='cell_volume')
#   z_hot = prof_hot.x.value
#   z_hot_flux = prof_hot['z_den_flux'].value
#   time=round(ds.current_time.in_units('Myr'),1)
#   cc=['g','r','c','m','y','k','orange','crimson','pink']
#   plt.plot(z,z_flux,label='t='+str(time)+'Myr',lw=2,c=cc[n])
#   plt.plot(z_hot,z_hot_flux,'--',lw=2.,c=cc[n])
#   global n
#   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
yt.add_field('mass_loading',function=_mass_loading, units  = 'Msun/yr/kpc**2')
num = [40,58]
num=[80,100,130,160,190,210,250,276]
num = [130,180,230,260,295]
num=[200,300,350,400,450,500,527]
#num = [1000]
num=[20,30,40,50,53]
num=[1,30,50,70,90,110,137]
num=[50,60,70,80]
num=[150,180,200,230,259]
num=[150,200,240]
#fig=plt.figure()
for i in num:
    see(i)

