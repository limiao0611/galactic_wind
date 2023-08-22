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
from scipy.interpolate import interp1d


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

num=range(240,370,10)
h_gas=[]
for i  in num:
    f3=open("z_mass.dat",'a')
    filen = get_fn(i)
    print filen
    ds = yt.load(filen)
    ad = ds.all_data()
    mass_all = ad.quantities.total_quantity('cell_mass')
    print 'mass_all',mass_all
    time = (ds.current_time).in_units('Myr')

    for z_max in range(5,200,10):
        z1_pc= YTQuantity(z_max,'pc')
        z1 = z1_pc/YTQuantity(5,'kpc')
        box1 = ds.box([0,0,-z1],[ds.domain_width[0], ds.domain_width[1], z1 ])
        mass_total= box1.quantities.total_quantity('cell_mass')
        print 'z1,mass_total=', z1_pc, mass_total
        if (mass_total/mass_all > 0.8):
            print >>f3, time, z1_pc, mass_total/mass_all, mass_total
            print time, z1_pc, mass_total/mass_all, mass_total
            h_gas.append(z1_pc)
            break
    f3.close()

f3=open("z_mass.dat",'a')
print >>f3, 'mean(h_gas), std(h_gas)', mean(h_gas), std(h_gas)
f3.close()

