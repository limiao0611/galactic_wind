import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *
from yt import YTQuantity
from scipy.interpolate import interp1d

font = {'family' : 'optima',
#        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

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


T_wh=array(      [1,  0.99e4,  1e4, 3e5, 3.001e5, 1e12 ])
filter_wh= array([0.,  0.,     1.,  1.,  0. ,     0.,  ])
f_filter_wh = interp1d(T_wh, filter_wh)
def _wh_filter(field,data):
    return f_filter_wh(data['temperature'])

T_w=array(      [1,  0.99e3,  1e3, 1e4, 1.001e5, 1e12 ])
filter_w= array([0.,  0.,     1.,  1.,  0. ,     0.,  ])
f_filter_w = interp1d(T_w, filter_w)
def _w_filter(field,data):
    return f_filter_w(data['temperature'])

def _bernoulli(field,data):
    return 0.5* (data['x-velocity']*data['x-velocity'] + data['y-velocity']*data['y-velocity'] +data['z-velocity']*data['z-velocity'] ) + 2.5*data['pressure']/data['density']
def _v_ber(field,data):
    return data['bernoulli']**0.5

def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   bx1 = ds.box([0,0, -0.5],[ds.domain_dimensions[0],ds.domain_dimensions[1],-0.2])
   bx2= ds.box([0,0, 0.2],[ds.domain_dimensions[0],ds.domain_dimensions[1],0.5])

   bx3 = ds.box([0,0, -0.2],[ds.domain_dimensions[0],ds.domain_dimensions[1],-0.1])
   bx4 =  ds.box([0,0, 0.1],[ds.domain_dimensions[0],ds.domain_dimensions[1],0.2])

   bx1_h = bx1.cut_region("obj['temperature']>3e5")
   bx1_wh = bx1.cut_region("obj['wh_filter']> 0.5 ")
   bx1_w = bx1.cut_region("obj['w_filter']> 0.5 ")

   v1_h = (bx1_h.quantities.weighted_average_quantity(fields='z-velocity',weight = 'cell_mass' )).in_units('km/s')
   v1_h_B = bx1_h.quantities.weighted_average_quantity(fields='v_ber',weight = 'cell_mass' )
   v1_wh = (bx1_wh.quantities.weighted_average_quantity(fields='z-velocity',weight = 'cell_volume' )).in_units('km/s')
   v1_wh_B = bx1_wh.quantities.weighted_average_quantity(fields='v_ber',weight = 'cell_volume' )
   v1_w = (bx1_w.quantities.weighted_average_quantity(fields='z-velocity',weight = 'cell_mass' )).in_units('km/s')
   v1_w_B = bx1_w.quantities.weighted_average_quantity(fields='v_ber',weight = 'cell_mass' )

   bx2_h = bx2.cut_region("obj['temperature']>3e5")
   bx2_wh = bx2.cut_region("obj['wh_filter']> 0.5 ")
   bx2_w = bx2.cut_region("obj['w_filter']> 0.5 ")

   v2_h = (bx2_h.quantities.weighted_average_quantity(fields='z-velocity',weight = 'cell_mass' )).in_units('km/s')
   v2_h_B = bx2_h.quantities.weighted_average_quantity(fields='v_ber',weight = 'cell_mass' )
   v2_wh = (bx2_wh.quantities.weighted_average_quantity(fields='z-velocity',weight = 'cell_volume' )).in_units('km/s')
   v2_wh_B = bx2_wh.quantities.weighted_average_quantity(fields='v_ber',weight = 'cell_volume' )
   v2_w = (bx2_w.quantities.weighted_average_quantity(fields='z-velocity',weight = 'cell_mass' )).in_units('km/s')
   v2_w_B = bx2_w.quantities.weighted_average_quantity(fields='v_ber',weight = 'cell_mass' )



   f=open('v_vber.dat','a')
   print >>f, i, v1_h,v1_h_B , v1_wh,v1_wh_B, v1_w,v1_w_B,'    ', v2_h,v2_h_B, v2_wh,v2_wh_B, v2_w,v2_w_B
   f.close()

yt.add_field('bernoulli',function=_bernoulli, units  = 'km**2/s**2')
yt.add_field('v_ber',function=_v_ber, units  = 'km/s')
yt.add_field('wh_filter',function=_wh_filter, units  = '')
yt.add_field('w_filter',function=_w_filter, units  = '')


num=range(160,340,20)
for i in num:
    see(i)

