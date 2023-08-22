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
f3=open("3phases.dat",'a')
num = range(0,1000)
#num = range(1349,1352)
for i  in num:
    filen = get_fn(i)
    print filen
    ds = yt.load(filen)
    ad = ds.all_data()
    print ds.current_time, ds.time_unit,ds.mass_unit,ds.length_unit
    print >>f1, ds.field_list
    print >>f2, ds.derived_field_list
    print ad["gas","density"]
    print ad["enzo","TotalEnergy"] #total energy density
    print ad["enzo","GasEnergy"]   # thermal energy density
    print ad["gas",'pressure']
    print ad["enzo",'Temperature']
    print ad["enzo",'x-velocity']
    a = ds.current_time
    b= ds.time_unit
    print 'a*b=',a*b
    print 'b/second=',b/second
    print size(ad["enzo","TotalEnergy"])
    print ds.domain_dimensions[0]
    num_cells = ds.domain_dimensions[0]*ds.domain_dimensions[1]*ds.domain_dimensions[2]
    print num_cells
    c =sum(ad["enzo","TotalEnergy"][0:num_cells]) 
    print 'c=',c
    energy_density_unit = ds.mass_unit/ds.length_unit/ds.time_unit**2
    print energy_density_unit
    total_energy= energy_density_unit * c* (ds.length_unit/ds.domain_dimensions[0])**3
#    total_energy = 0. 
#    thermal_energy = 0. 
    specific_energy_unit = ds.length_unit**2/ds.time_unit**2
    print '############'
    print  ad["enzo","TotalEnergy"][0:2] * ad["gas","density"][0:2]

#    for i in range(num_cells):
    total_energy=sum(ad["enzo","TotalEnergy"][0:num_cells]*specific_energy_unit * ad["gas","density"][0:num_cells] * (ds.length_unit/ds.domain_dimensions[0])**3 )
    thermal_energy= sum(ad["enzo","GasEnergy"][0:num_cells]*specific_energy_unit * ad["gas","density"][0:num_cells] * (ds.length_unit/ds.domain_dimensions[0])**3 )

#    d = sum(ad["enzo","GasEnergy"][0:num_cells])
#    thermal_energy= energy_density_unit * d* (ds.length_unit/ds.domain_dimensions[0])**3
    time = a*b/second/3.15e7 
    pressure_total = sum( ad["gas",'pressure'][0:num_cells])*(ds.length_unit/ds.domain_dimensions[0])**3*1.5
    kinetic_energy = sum( ad["gas",'kinetic_energy'][0:num_cells])*(ds.length_unit/ds.domain_dimensions[0])**3
    print 'kinetic_energy=',kinetic_energy

    f_vh=0.
    hot = ad["temperature"].in_units('K') > 2e5
    warm =  (ad["temperature"].in_units('K') < 2e5) & ( ad["temperature"].in_units('K') >1e3)
    cold =  ad["temperature"].in_units('K') <1e3
    num_hot = size(ad['temperature'][hot])
    num_warm = size(ad['temperature'][warm])
    num_cold = size(ad['temperature'][cold])
    f_vh =num_hot*1.0/num_cells
    f_vw =num_warm*1.0/num_cells
    f_vc =num_cold*1.0/num_cells
    print 'f_vh',f_vh
    print 'den_hot=',ad['density'][hot]
    mass_tot = sum(ad['gas','density'][0:num_cells])*  (ds.length_unit/ds.domain_dimensions[0])**3/2e33
    mass_hot = sum(ad['gas','density'][hot])*  (ds.length_unit/ds.domain_dimensions[0])**3/2e33
    mass_warm = sum(ad['gas','density'][warm])*  (ds.length_unit/ds.domain_dimensions[0])**3/2e33
    mass_cold = sum(ad['gas','density'][cold])*  (ds.length_unit/ds.domain_dimensions[0])**3/2e33

    kinetic_energy = sum( ad["gas",'kinetic_energy'][0:num_cells])*(ds.length_unit/ds.domain_dimensions[0])**3
    print 'kinetic_energy=',kinetic_energy
    f_mh = mass_hot/mass_tot
    f_mw = mass_warm/mass_tot
    f_mc = mass_cold/mass_tot

    pres_hot = mean(ad["gas",'pressure'][hot])/1.38e-16
    pres_warm = mean(ad["gas",'pressure'][warm])/1.38e-16
    pres_cold = mean(ad["gas",'pressure'][cold])/1.38e-16

    den_hot = mean( ad['gas','density'][hot])/1.67e-24
    den_warm = mean( ad['gas','density'][warm])/1.67e-24
    den_cold = mean( ad['gas','density'][cold])/1.67e-24
  
    T_hot = mean(ad['temperature'][hot])
    T_warm = mean(ad['temperature'][warm])
    T_cold = mean(ad['temperature'][cold])

    mach_hot = mean((ad["gas",'pressure'][hot]/ad['gas','density'][hot])**0.5)
    mach_warm = mean((ad["gas",'pressure'][warm]/ad['gas','density'][warm])**0.5)
    mach_cold = mean((ad["gas",'pressure'][cold]/ad['gas','density'][cold])**0.5)
    print>>f3, time, total_energy, thermal_energy, kinetic_energy,f_mh,f_mw,f_mc,f_vh,f_vw,f_vc,pres_hot,pres_warm,pres_cold,den_hot,den_warm,den_cold,T_hot,T_warm,T_cold, mach_hot, mach_warm, mach_cold
