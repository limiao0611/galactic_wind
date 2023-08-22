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
    a0=''
    if (i<10):
      a0='000'
    if (10<=i<100):
      a0='00'
    if (100<=i<999):
      a0='0'
    filen='DD'+a0+str(i)+'/sb_'+a0+str(i)
    return filen
def _z_ek_flux(field,data):
    return abs(0.5*data['density']*data['z-velocity']*   (data['x-velocity']*data['x-velocity'] + data['y-velocity']*data['y-velocity'] +data['z-velocity']*data['z-velocity'] ))

def _z_eth_flux(field,data):
    return abs(data['density']*data["GasEnergy"]*data['z-velocity'])

def _z_etot_flux(field,data):
    return abs( data['density']*data["GasEnergy"]*data['z-velocity']) + abs(0.5*data['density']*data['z-velocity']*   (data['x-velocity']*data['x-velocity'] + data['y-velocity']*data['y-velocity'] +data['z-velocity']*data['z-velocity'] ))

def _z_metal_flux(field,data):
    return abs(data['SN_Colour']*data['z-velocity'])

def _z_den_flux(field,data):
    return abs(data['density']*data['z-velocity'])

def see(i):
   f=open('loading.dat','a')
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()
#   halo = (ad.cut_region("obj['z']>0.2") and ad.cut_region("obj['z']<-0.2"))
#   halo1 = ad.cut_region("obj['z']>0.2")
#   halo1 = ad.cut_region("obj['z']< -0.2")
   halo1 = ds.box([0,0,-0.5],[ds.domain_width[0], ds.domain_width[1],-0.2])
   halo2 = ds.box([0,0,0.2],[ds.domain_width[0], ds.domain_width[1],0.5])


   halo1_out = halo1.cut_region("obj['z-velocity']<0")
   halo2_out = halo2.cut_region("obj['z-velocity']>0")

   halo1_out_hot = halo1.cut_region(" (obj['z-velocity'].in_units('km/s')<0.) & (obj['temperature'].in_units('K')>3e5  )")
   halo2_out_hot = halo2.cut_region("  (obj['z-velocity'].in_units('km/s')>0. ) & (obj['temperature'].in_units('K')>3e5 )")

#   all_vol = ad.quantities.total_quantity('cell_volume')
#   total_vol = halo.quantities.total_quantity('cell_volume')
   total_vol1 = halo1.quantities.total_quantity('cell_volume')
   total_vol2 = halo2.quantities.total_quantity('cell_volume')
   total_vol =  total_vol1 +  total_vol2
   total_mass1 = halo1.quantities.total_quantity('cell_mass')
   total_mass2 = halo2.quantities.total_quantity('cell_mass')
   total_mass = total_mass1+total_mass2

#   print 'all_vol=',all_vol
   print 'total_vol=',total_vol
   print 'total_vol1=',total_vol1
   print 'total_vol2=',total_vol2

   f_V_out =  (halo1_out.quantities.total_quantity('cell_volume')+ halo2_out.quantities.total_quantity('cell_volume'))/total_vol
   print 'f_V_out=',f_V_out

   f_V_out_hot =  (halo1_out_hot.quantities.total_quantity('cell_volume')+ halo2_out_hot.quantities.total_quantity('cell_volume'))/total_vol
   print 'f_V_out_hot=',f_V_out_hot


#   print 'all_vol=',all_vol
   print 'total_vol=',total_vol
   print 'total_vol1=',total_vol1
   print 'total_vol2=',total_vol2



#   hot = halo.cut_region("obj['temperature']>3e5")
   hot1=halo1.cut_region("obj['temperature']>3e5")
   hot2=halo2.cut_region("obj['temperature']>3e5")

   cold1 = halo1.cut_region("obj['temperature']<1e3")
   cold2 = halo2.cut_region("obj['temperature']<1e3")

   hot_vol1 = hot1.quantities.total_quantity('cell_volume')
   hot_vol2 = hot2.quantities.total_quantity('cell_volume')
   cold_vol1 = cold1.quantities.total_quantity('cell_volume')
   cold_vol2 = cold2.quantities.total_quantity('cell_volume')


   hot_mass1 = hot1.quantities.total_quantity('cell_mass')
   hot_mass2 = hot2.quantities.total_quantity('cell_mass')
   cold_mass1 = cold1.quantities.total_quantity('cell_mass')
   cold_mass2 = cold2.quantities.total_quantity('cell_mass')


   fVh= (hot_vol1+ hot_vol2)/total_vol
   fVc= (cold_vol1+cold_vol2)/total_vol
   fVw= 1-fVh-fVc

   fmh= (hot_mass1+hot_mass2)/total_mass
   fmc= (cold_mass1+cold_mass2)/total_mass
   fmw= 1-fmh-fmc


   metal_inject=10**-2.2*204.4 # 204.4 * SFR density, in unit of Msun/yr/kpc^2
   energy_inject=0.00349* (10**-1.4) #case, in unit of erg/s/cm**2
   SF_density = 10**-2.2

   global z_ml,z_el,z_mel

#   ml=  (mean(halo1["z_den_flux"])+ mean(halo2["z_den_flux"] ) ) / 2. / SF_density
#   el=  (mean(halo1["z_etot_flux"]) + mean(halo2["z_etot_flux"] ))/2./energy_inject
#   mel= ( mean(halo1["z_metal_flux"])  +  mean(halo2["z_metal_flux"]) ) /2. /metal_inject

   ml=  (mean(halo1_out["z_den_flux"])+ mean(halo2_out["z_den_flux"] ) ) / 2. / SF_density *  f_V_out
   el=  (mean(halo1_out["z_etot_flux"]) + mean(halo2_out["z_etot_flux"] ))/2./energy_inject*  f_V_out
   mel= ( mean(halo1_out["z_metal_flux"])  +  mean(halo2_out["z_metal_flux"]) ) /2. /metal_inject*  f_V_out

   ml_hot=  (mean(halo1_out_hot["z_den_flux"])+ mean(halo2_out_hot["z_den_flux"] ) ) / 2. / SF_density *  f_V_out_hot
   el_hot=  (mean(halo1_out_hot["z_etot_flux"]) + mean(halo2_out_hot["z_etot_flux"] ))/2./energy_inject *  f_V_out_hot
   mel_hot= ( mean(halo1_out_hot["z_metal_flux"])  +  mean(halo2_out_hot["z_metal_flux"]) ) /2. /metal_inject *  f_V_out_hot

   print 'ml_hot,el_hot,mel_hot = ', ml_hot,el_hot,mel_hot


   z_ml.append(ml)
   z_el.append(el)
   z_mel.append(mel)

   z_ml_hot.append(ml_hot)
   z_el_hot.append(el_hot)
   z_mel_hot.append(mel_hot)


   Vh.append(fVh)
   Vw.append(fVw)
   Vc.append(fVc)
   mh.append(fmh)
   mw.append(fmw)
   mc.append(fmc)

   time  = round(ds.current_time.in_units('Myr'),2 )
   print >>f, i, time, ml,el,mel, fVh, fVw, fVc, fmh, fmw, fmc
   print z_ml, mean(z_ml),std(z_ml)
   print z_el, mean(z_el),std(z_el)
   print z_mel, mean(z_mel), std(z_mel)

   f.close()

n=0
yt.add_field('z_metal_flux',function = _z_metal_flux,units = 'Msun/kpc**2/yr')
yt.add_field('z_ek_flux',function=_z_ek_flux, units  = 'erg/s/cm**2')
yt.add_field('z_eth_flux',function=_z_eth_flux, units  = 'erg/s/cm**2')
yt.add_field('z_etot_flux',function=_z_etot_flux, units  = 'erg/s/cm**2')
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')

z_ml=[] #mass loading
z_el=[]  # energy loading
z_mel=[]  # metal loading



z_ml_hot=[] #mass loading
z_el_hot=[]  # energy loading
z_mel_hot=[]  # metal loading

Vh=[]
Vw=[]
Vc=[]
mh=[]
mw=[]
mc=[]


num=range(180,290,10)
for i in num:
    see(i)

f=open('loading.dat','a')
print >>f, z_ml
print >>f, z_el
print >>f, z_mel



print >>f, mean(z_ml), mean(z_el), mean(z_mel)
print >>f, std(z_ml),std(z_el), std(z_mel)



print >>f, 'mean(z_ml_hot), mean(z_el_hot), mean(z_mel_hot)=', mean(z_ml_hot), mean(z_el_hot), mean(z_mel_hot)
print >>f, 'std(z_ml_hot),std(z_el_hot), std(z_mel_hot)=', std(z_ml_hot),std(z_el_hot), std(z_mel_hot)



print >>f, 'Vh=', mean(Vh),std(Vh)
print >>f, 'Vw=', mean(Vw),std(Vw)
print >>f, 'Vc=', mean(Vc),std(Vc)
print >>f, 'mh=', mean(mh),std(mh)
print >>f, 'mw=', mean(mw),std(mw)
print >>f, 'mc=', mean(mc),std(mc)

f.close()

