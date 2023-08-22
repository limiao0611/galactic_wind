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

def _z_den_flux(field,data):
    return (data['density']*data['z-velocity'])


def see(i):

   profiles=[]
   labels=[]
   plot_specs=[]

   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()
   cr1 =  ad.cut_region("obj['temperature']>3e5")
   cr2 =  ad.cut_region("obj['temperature']<3e5").cut_region("obj['temperature']>1e3")
   cr3 =  ad.cut_region("obj['temperature']<1e3")
#   cr = ad.cut_region("obj['z-velocity']<0.") and ad_cutregion("obj['z']>-0.")

   profiles.append(create_profile(ad,"z-velocity",["cell_mass"],weight_field=None, logs=None, fractional=True))
   profiles.append(create_profile(cr1,"z-velocity",["cell_mass"],weight_field=None , logs=None,fractional=True ))
   profiles.append(create_profile(cr2,"z-velocity",["cell_mass"],weight_field=None, logs=None,fractional=True ))
   profiles.append(create_profile(cr3,"z-velocity",["cell_mass"],weight_field=None, logs=None,fractional=True ))

   labels.append('all')
   labels.append('T>3e5K')
   labels.append('1e3<T<3e5K')
   labels.append('T<1e3K')

   plot_specs.append(dict(linestyle="-", alpha=1.0,color='green',linewidth=2.5))
   plot_specs.append(dict(linestyle="-", alpha=1.0,color='red',linewidth=2.0))
   plot_specs.append(dict(linestyle="-", alpha=1.0,color='orange',linewidth=2.0))
   plot_specs.append(dict(linestyle="-", alpha=1.0,color='blue',linewidth=2.0))
#   plot = yt.ProfilePlot(cr,"z-velocity",["cell_mass"],weight_field=None,x_log=False)

   plot = ProfilePlot.from_profiles(profiles, labels=labels, plot_specs=plot_specs)

   plot.set_unit('z-velocity','km/s')
   plot.set_unit('cell_mass','msun')
   plot.x_log = False
   plot.set_xlim(-600.,600)
#   plot.grid()
   plot.save('z_velocity_dist_multiphase_'+str(i)+'.png')

labels=[]
plot_specs=[]

num=[1]
num = [150,200,240]
for i in num:
    see(i)

