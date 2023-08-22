import yt
import matplotlib
import matplotlib.pyplot as plt
from yt.units import second, gram, parsec,centimeter, erg
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

f1=open("yt_field_list",'w')
f2=open("yt_derived_field_list",'w')
f3=open("e_t1.dat",'a')
num = range(56,60)
num=[300,301]
num=[298,299]
num=range(300,410,10)
for i  in num:
    filen = get_fn(i)
    print filen
    ds = yt.load(filen)
    ad = ds.all_data()
    hot = ad["temperature"].in_units('K') > 3e4
    cold = ad["temperature"].in_units('K') < 1e3
    warm = (ad["temperature"].in_units('K') > 1e3) &  (ad["temperature"].in_units('K') < 3e4)

    specific_energy_unit = ds.length_unit**2/ds.time_unit**2
    a = ds.current_time
    b= ds.time_unit
    time = a*b/second/3.15e7
    mass_all = sum(ad['cell_mass'])
    mass_h = sum(ad['cell_mass'][hot])
    mass_w = sum(ad['cell_mass'][warm])
    mass_c = sum(ad['cell_mass'][cold])
    total1 = sum(ad["enzo","TotalEnergy"]*ad['cell_mass']*specific_energy_unit).in_units('erg')
    thermal1 = sum(ad["enzo","GasEnergy"]*ad['cell_mass']).in_units('erg')
    print>>f3,i, time,total1,thermal1,mass_all,mass_h, mass_w, mass_c
    print time,total1,thermal1, mass_all, mass_h, mass_w, mass_c

f1.close()
f2.close()
f3.close()

