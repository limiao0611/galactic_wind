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

k= YTQuantity(1.3806485e-16,'erg/K')
h = YTQuantity(6.6261e-27,'erg*s')
c = YTQuantity(3e10,"cm/s")
wl = YTQuantity(1032,'angstrom')
solid_angle=YTQuantity(4*3.14159265,'rad')

#def _GasEnergy(field,data):
#    return data['TotalEnergy'] - 0.5* (data['x-velocity']*data['x-velocity'] + data['y-velocity']*data['y-velocity'] +data['z-velocity']*data['z-velocity'] )

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

def _cool_rate(field,data):
    return data["cell_mass"]*data["GasEnergy"]/data["cooling_time"]

def _cool_time_inv(field,data):
    return 1./data["cooling_time"]

T2=array(     [1.,     1.99e5,     2e5,   4e5,  4.01e5,     1e12])
filter2=array([1e-100, 1e-100,     1.,    1.,   1e-100,     1e-100, ])
f_linear_filter=interp1d(T2,filter2)

def filter(T):
      return f_linear_filter(T)


def _emission_flux_1032(field,data):  # cm^-3 s^-1 rad^-1
   return filter(data['temperature'])* data["density"]*data["GasEnergy"]/data["cooling_time"]/ (h*c/wl)/solid_angle


T_fit=array(           [0.0, 5.0,  5.05,  5.20,   5.40,    5.45,  5.90 , 6.35,   7.15  , 7.5, 12. ])
fOVI_log10_fit = array( [100., 10., 6.099, 3.070,  0.801,  0.657,  2.254, 2.826,  6.891, 10,  100. ] )
f_linear=interp1d(T_fit, fOVI_log10_fit)

def OVI_fraction(T):
    return pow(10,-f_linear(log10(T) ))

def _f_OVI(field,data):
    return OVI_fraction(data['temperature'])


def collision_rate_coeff(T): # cm^3 s^-1
    delta_e = h*c/wl
    Omega = 5.00 # for OVI 2P - 2S transition; ref: AGN^2, p60, Table 3.6
    ome1 = 1.  # !!!!!!!!!!check
    ome2 = 3.  # !!!!!!!!!! check

    c21 =  8.629e-6 * Omega /ome2/T**0.5     * YTQuantity(1, 'K**0.5*cm**3/s') # cm^-3 s^-1
    c12 = ome2/ome1 *c21 * exp (- delta_e/(k * T) )  # cm^3 s^-1
    return c12

def _OVI_collision_rate(field,data):
    f_O = 5e-4
    miu = YTQuantity(1.67e-24, 'g') #!!!!!!!!!!!!! check
    return data['density']**2/miu**2* f_O * data['f_OVI'] * collision_rate_coeff(data['temperature'])

def _emission_flux_OVI(field,data):
    return data['OVI_collision_rate']/solid_angle

def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   print "GasEnergy=",ad['GasEnergy']
   print "TotalEnergy=",ad['TotalEnergy']
   print "ad.quantities.total_quantity(['emission_flux_OVI']) = ", ad.quantities.total_quantity(['emission_flux_OVI'])
   print "ad.quantities.total_quantity(['emission_flux_1032']) = ", ad.quantities.total_quantity(['emission_flux_1032'])


   a= "temperature"
   b=  "density"
   c = "emission_flux_OVI"
   d=None
#   hot = ad.cut_region("obj['temperature']>3e4")
#   midplane = ad.cut_region("obj['z']<0.1 and obj['z']>-0.1")
#   midplane = ad.cut_region("obj['z']<0.1") and ad.cut_region("obj['z']>-0.1")
   midplane = ds.box([0,0,-0.1],[0.24,0.24,0.1])
   halo = ad.cut_region("obj['z']>0.2") and ad.cut_region("obj['z']<-0.2")

   plot = PhasePlot(ad,a,b ,[c] ,weight_field=d)
   plot.set_zlim(c,1e-20,1e-10)
   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+d+'-weighted.png')

   plot = PhasePlot(midplane,a,b,c,weight_field=d)
   plot.set_zlim(c,1e-20,1e-10)
   plot.save(a+'_'+b+'_'+c+'_midplane1_'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'_midplane1_'+str(i)+d+'-weighted.png')

   plot = PhasePlot(halo,a,b,c,weight_field=d)
   plot.set_zlim(c,1e-20,1e-10)
   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+d+'-weighted.png')

   c = "emission_flux_1032"

   plot = PhasePlot(ad,a,b ,[c] ,weight_field=d)
   plot.set_zlim(c,1e-20,1e-10)
   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+d+'-weighted.png')

   plot = PhasePlot(midplane,a,b,c,weight_field=d)
   plot.set_zlim(c,1e-20,1e-10)
   plot.save(a+'_'+b+'_'+c+'_midplane1_'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'_midplane1_'+str(i)+d+'-weighted.png')

   plot = PhasePlot(halo,a,b,c,weight_field=d)
   plot.set_zlim(c,1e-20,1e-10)
   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+'.png')
#   plot.save(a+'_'+b+'_'+c+'halo'+str(i)+d+'-weighted.png')





yt.add_field('metallicity',function=_metallicity)
yt.add_field('cool_rate',function=_cool_rate,units="erg/s")
yt.add_field('cool_time_inv',function=_cool_time_inv,units="1/s")
#yt.add_field('GasEnergy',function=_GasEnergy,units="erg/g")
yt.add_field('emission_flux_1032',function=_emission_flux_1032,units="1/s/cm**3/rad")
yt.add_field('f_OVI',function=_f_OVI,units='')
yt.add_field('OVI_collision_rate',function=_OVI_collision_rate,units='1/cm**3/s')
yt.add_field('emission_flux_OVI',function=_emission_flux_OVI,units='1/cm**3/s/rad')


num=[205,240,410]
for i in num:
    see(i)


