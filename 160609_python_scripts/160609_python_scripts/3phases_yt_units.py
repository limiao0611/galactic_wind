import yt
import matplotlib
import matplotlib.pyplot as plt
from yt.utilities.physical_constants import kboltz
from yt.units import second, gram, parsec,centimeter, erg,cm,K
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
f3=open("3phases_yt_units.dat",'a')
num = range(1,2)
#num = range(1349,1352)
gamma =  5./3.
for i  in num:
    
    filen = get_fn(i)
    print filen
    ds = yt.load(filen)
    ad = ds.all_data()
    time =ds.current_time.in_units('Myr')
    print ds.current_time, ds.time_unit,ds.mass_unit,ds.length_unit
    print >>f1, ds.field_list
    print >>f2, ds.derived_field_list
    print ad["gas","density"]
    print ad["enzo","TotalEnergy"] #total energy density
    print ad["enzo","GasEnergy"]  
    print ad["enzo","GasEnergy"].in_cgs() 
    print ad["gas","cell_mass"] 
    print ad["gas","cell_mass"].in_cgs()
    print ad["gas","cell_mass"].in_units('Msun')
    print ad['gas','kinetic_energy']
    print ad['gas','kinetic_energy'].in_cgs()
    print ad['index','cell_volume']
    print ad['index','cell_volume'].in_units('pc**3')

    specific_energy_unit = ds.length_unit**2/ds.time_unit**2
    total_energy = sum(ad["enzo","TotalEnergy"]* specific_energy_unit*ad["gas","cell_mass"] ).in_units('erg')
    print 'total_energy=',total_energy   

    thermal_energy = sum(ad["enzo","GasEnergy"]*ad["gas","cell_mass"]).in_units('erg')
    print 'thermal_energy=',thermal_energy

    kinetic_energy= sum( ad['index','cell_volume']*ad['gas','kinetic_energy']).in_units('erg')
    print 'kinetic_energy=',kinetic_energy


########
    num_cells = ds.domain_dimensions[0]*ds.domain_dimensions[1]*ds.domain_dimensions[2]

    hot = ad["temperature"].in_units('K') > 2e5
    warm =  (ad["temperature"].in_units('K') < 2e5) & ( ad["temperature"].in_units('K') >1e3)
    cold =  ad["temperature"].in_units('K') <1e3

    num_hot = size(ad['temperature'][hot])
    num_warm = size(ad['temperature'][warm])
    num_cold = size(ad['temperature'][cold])
    f_vh =num_hot*1.0/num_cells * K/K
    f_vw =num_warm*1.0/num_cells *K/K
    f_vc =num_cold*1.0/num_cells *K/K
   
    mass_tot = sum(ad['gas','cell_mass']).in_units('msun')
    mass_hot = sum(ad['gas','cell_mass'][hot]).in_units('msun')
    mass_warm = sum(ad['gas','cell_mass'][warm]).in_units('msun')
    mass_cold = sum(ad['gas','cell_mass'][cold]).in_units('msun')

    f_mh = mass_hot/mass_tot
    f_mw = mass_warm/mass_tot
    f_mc = mass_cold/mass_tot

    pres_hot=pres_warm = pres_cold = den_hot= den_warm= den_cold = T_hot=T_warm=T_cold = mach_hot =mach_warm = mach_cold = mach_hot1 = mach_warm1 = mach_cold1 = 1e-9

    pres_hot=pres_warm = pres_cold = 1e-9 * cm**(-3)*K
    den_hot= den_warm= den_cold = 1e-9 * cm**(-3)
    T_hot=T_warm=T_cold = 1e-9*K
    mach_hot =mach_warm = mach_cold = mach_hot1 = mach_warm1 = mach_cold1 = 1e-9 * K/K


    if (num_hot>0):
       pres_hot = (mean(ad["gas",'pressure'][hot])/kboltz).in_units('cm**(-3)*K')
       den_hot = mean( ad['gas','density'][hot])/1.67e-24/gram
       mach_hot=mean(ad['gas','mach_number'][hot])      
       mach_hot1 =  mean( (ad['gas','kinetic_energy'][hot]/gamma/ad["gas",'pressure'][hot])**0.5).in_units('dimensionless')
       T_hot = mean(ad['temperature'][hot])


    if (num_warm>0):
       pres_warm = (mean(ad["gas",'pressure'][warm])/kboltz).in_units('cm**(-3)*K')
       den_warm = mean( ad['gas','density'][warm])/1.67e-24/gram
       mach_warm=mean(ad['gas','mach_number'][warm])
       mach_warm1 =  mean( (ad['gas','kinetic_energy'][warm]/gamma/ad["gas",'pressure'][warm])**0.5).in_units('dimensionless')
       T_warm = mean(ad['temperature'][warm])



    if (num_cold>0):
       pres_cold = (mean(ad["gas",'pressure'][cold])/kboltz).in_units('cm**(-3)*K')
       den_cold = mean( ad['gas','density'][cold])/1.67e-24/gram
       mach_cold=mean(ad['gas','mach_number'][cold])
       mach_cold1 =  mean( (ad['gas','kinetic_energy'][cold]/gamma/ad["gas",'pressure'][cold])**0.5).in_units('dimensionless')
       T_cold = mean(ad['temperature'][cold])
   
    print>>f3, time, total_energy, thermal_energy, kinetic_energy,f_mh,f_mw,f_mc,f_vh,f_vw,f_vc,pres_hot,pres_warm,pres_cold,den_hot,den_warm,den_cold,T_hot,T_warm,T_cold, mach_hot, mach_warm, mach_cold, mach_hot1, mach_warm1, mach_cold1
              
