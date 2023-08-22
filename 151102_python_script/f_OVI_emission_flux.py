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

def _cool_rate1(field,data):
    return data["density"]*data["GasEnergy"]/data["cooling_time"]



T2=array(     [1.,     1.99e5,     2e5,   4e5,  4.01e5,     1e12])
filter2=array([1e-100, 1e-100,     1.,    1.,   1e-100,     1e-100 ])
f_linear_filter=interp1d(T2,filter2)

def filter(T):
      return f_linear_filter(T)


def _emission_flux_1032_crude(field,data):  # cm^-3 s^-1 rad^-1
   return filter(data['temperature'])* data["density"]*data["GasEnergy"]/data["cooling_time"]/ (h*c/wl)/solid_angle * (1./3.) # 1/3 is the fraction of OVI that emits 1032, instead of 1038


def _emission_1032_crude(field,data):
   return data['emission_flux_1032_crude']*data['cell_volume']

T_fit=array(           [0.0, 5.0,  5.05,  5.20,   5.40,    5.45,  5.90 , 6.35,   7.15  , 7.5,  12. ])
fOVI_log10_fit = array( [100., 10., 6.099, 3.070,  0.801,  0.657,  2.254, 2.826,  6.891, 10,   100. ] )
f_linear=interp1d(T_fit, fOVI_log10_fit)

def OVI_fraction(T):
    return pow(10,-f_linear(log10(T) ))

def _f_OVI(field,data):
    return OVI_fraction(data['temperature'])


def collision_rate_coeff_1032(T): # cm^3 s^-1, collisional excitation rate
    delta_e = h*c/wl
    Omega = 5.00 # collision strength, for OVI 2P - 2S transition; ref: AGN^2, p60, Table 3.6
    ome1 = 2.  #  how many states at the lower level 2S_1/2,   2J+1 = 2
    ome2_1032=4.
    ome2_1038=2.
    ome2 = ome2_1032+ome2_1038  #  how many states at the higher lever 2P_1/2,3/2,  2J+1=2, 2J+1 = 4, mJ=3/2.1/2,-1/2. -3/2

    c21 =  8.629e-6 * Omega /ome2/T**0.5     * YTQuantity(1, 'K**0.5*cm**3/s') # cm^-3 s^-1, collisional de-excitation rate q21 = n_e*n_OVI *c21
    c12 = ome2/ome1 *c21 * exp (- delta_e/(k * T) )  # cm^3 s^-1, collisional excitation rate
    c12_1032 = c12 * ome2_1032/ome2
    return c12_1032

def _OVI_collision_rate_1032(field,data):
    f_O = 5e-4
#    mu = YTQuantity(1.67e-24, 'g')*0.609  #n_He/n_H = 0.1, fully ionized
    n_e =  data['density']/YTQuantity(1.67e-24, 'g')*11./13
    n_H = n_e * 9./11
    n_OVI = n_H * f_O * data['f_OVI']
    return n_e * n_OVI *  collision_rate_coeff_1032(data['temperature'])
#    return data['density']**2/miu**2* f_O * data['f_OVI'] * collision_rate_coeff(data['temperature'])

def _emission_flux_OVI_1032(field,data):
    return data['OVI_collision_rate_1032']/solid_angle

def _emission_OVI_1032(field,data):
    return data['emission_flux_OVI_1032']*data['cell_volume']

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


def see(i):
  fn = get_fn(i)

  ds = yt.load(fn)
  ad =  ds.all_data()

  print ad['f_OVI']
  print 'ad["OVI_collision_rate_1032"]=', ad['OVI_collision_rate_1032']

  c1 = [ds.domain_width[0], ds.domain_width[1], 0.0]


  f='f_OVI'
  slc = yt.ProjectionPlot(ds, 'x',  fields=f,center=c1,weight_field='cell_volume')
  slc.set_zlim(f,1e-8,1)
  slc.set_log(f,log)
#  slc.set_cmap('f_OVI','rainbow')
  slc.save()


#  f=['emission_flux_OVI']
  f='emission_flux_OVI_1032'
  slc = yt.ProjectionPlot(ds, 'x',  fields=f,center=c1)
  slc.set_zlim(f,1,1e7)
  slc.set_log(f,log)
#  slc.set_cmap('emission_flux_OVI','rainbow')
  slc.save()


  slc = yt.ProjectionPlot(ds, 'z',  fields=f,center=c1)
  slc.set_zlim(f,1,1e7)
  slc.set_log(f,log)
#  slc.set_cmap('emission_flux_OVI','rainbow')
  slc.save()


#  f='emission_flux_1032_crude'
#  slc = yt.ProjectionPlot(ds, 'x',  fields=f,center=c1)
#  slc.set_zlim(f,1,1e7)
#  slc.set_log(f,log)
#  slc.set_cmap('emission_flux_OVI','rainbow')
#  slc.save()


#  slc = yt.ProjectionPlot(ds, 'z',  fields=f,center=c1)
#  slc.set_zlim(f,1,1e7)
#  slc.set_log(f,log)
#  slc.set_cmap('emission_flux_OVI','rainbow')
#  slc.save()


def phase_diagram(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   print "ad.quantities.total_quantity(['emission_OVI_1032']) = ", ad.quantities.total_quantity(['emission_OVI_1032'])
   print "ad.quantities.total_quantity(['emission_1032_crude']) = ", ad.quantities.total_quantity(['emission_1032_crude'])


   a= "temperature"
   b=  "density"
   c = "emission_OVI_1032"
   d=None

   plot = PhasePlot(ad,a,b ,[c] ,weight_field=d)
   plot.set_zlim(c,1e34,1e44)
   plot.set_title(c,"ad.quantities.total_quantity(['emission_flux_OVI'])="+str (ad.quantities.total_quantity(['emission_OVI_1032']))  )
   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+'.png')

#   c = "emission_1032_crude"

#   plot = PhasePlot(ad,a,b ,[c] ,weight_field=d)
#   plot.set_zlim(c,1e34,1e44)
#   plot.set_title(c,"ad.quantities.total_quantity(['emission_1032_crude'])="+str (ad.quantities.total_quantity(['emission_1032_crude']))  )
#   plot.save(a+'_'+b+'_'+c+'_all_'+str(i)+'.png')


#yt.add_field('cool_rate1',function=_cool_rate1,units="erg/s/cm**3")
yt.add_field('emission_flux_1032_crude',function=_emission_flux_1032_crude,units="1/s/cm**3/rad")
yt.add_field('emission_1032_crude',function=_emission_1032_crude,units="1/s/rad")
yt.add_field('f_OVI',function=_f_OVI,units='')
yt.add_field('OVI_collision_rate_1032',function=_OVI_collision_rate_1032,units='1/cm**3/s')
yt.add_field('emission_flux_OVI_1032',function=_emission_flux_OVI_1032,units='1/cm**3/s/rad')
yt.add_field('emission_OVI_1032',function=_emission_OVI_1032,units='1/s/rad')

num=[243,403]
for i in num:
#   see(i)
  phase_diagram(i)

