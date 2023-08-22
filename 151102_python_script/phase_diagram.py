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

def _metallicity(field,data):
    return data["SN_Colour"]/data["density"]

def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   a= "temperature"
   b=  "density"
   c = "cell_mass"
#   hot = ad.cut_region("obj['temperature']>3e4")
#   midplane = ad.cut_region("obj['z']<0.1 and obj['z']>-0.1")
#   midplane = ad.cut_region("obj['z']<0.1") and ad.cut_region("obj['z']>-0.1")
   midplane = ds.box([0,0,-0.1],[ds.domain_dimensions[0],ds.domain_dimensions[1],0.1])
   halo = ad.cut_region("obj['z']>0.2") and ad.cut_region("obj['z']<-0.2")

   plot = PhasePlot(ad,a,b ,[c] ,weight_field=None)
   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+'.png')

   plot = PhasePlot(midplane,a,b,c,weight_field=None)
   plot.save(a+'_'+b+'_'+c+'_midplane1_'+str(i)+'.png')

   plot = PhasePlot(halo,a,b,c,weight_field=None)
   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+'.png')

yt.add_field('metallicity',function=_metallicity)
num=[180,210]
for i in num:
    see(i)

