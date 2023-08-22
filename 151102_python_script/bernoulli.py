import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *

font = {'family' : 'optima',
#        'weight' : 'bold',
        'size'   : 22}


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

def _bernoulli(field,data):
    return 0.5* (data['x-velocity']*data['x-velocity'] + data['y-velocity']*data['y-velocity'] +data['z-velocity']*data['z-velocity'] ) + 2.5*data['pressure']/data['density']

def see(i):
   f=open('loading.dat','a')
   fn = get_fn(i)
   ds = yt.load(fn)
#   ad = ds.all_data()

   box1 = ds.box([0,0,0.07],[ds.domain_dimensions[0],ds.domain_dimensions[1],0.095])
   box2 = ds.box([0,0,0.16],[ds.domain_dimensions[0],ds.domain_dimensions[1],0.19])
   box3 = ds.box([0,0,0.225],[ds.domain_dimensions[0],ds.domain_dimensions[1],0.245])

   box1_w = box1.cut_region("obj['temperature']< 3e4") #  & obj['temperature']>1e3")
   box1_h = box1.cut_region("obj['temperature']> 3e4")
   box2_w = box2.cut_region("obj['temperature']< 3e4") #  & obj['temperature']>1e3")
   box2_h = box2.cut_region("obj['temperature']> 3e4")
   box3_w = box3.cut_region("obj['temperature']< 3e4") #  & obj['temperature']>1e3")
   box3_h = box3.cut_region("obj['temperature']> 3e4")


   ber_hot1 = box1_h.quantities.weighted_average_quantity(fields='bernoulli',weight='cell_mass')
   ber_warm1 = box1_w.quantities.weighted_average_quantity(fields='bernoulli',weight='cell_mass')
   ber_hot2 = box2_h.quantities.weighted_average_quantity(fields='bernoulli',weight='cell_mass')
   ber_warm2 = box2_w.quantities.weighted_average_quantity(fields='bernoulli',weight='cell_mass')
   ber_hot3 = box3_h.quantities.weighted_average_quantity(fields='bernoulli',weight='cell_mass')
   ber_warm3 = box3_w.quantities.weighted_average_quantity(fields='bernoulli',weight='cell_mass')


   ber_h1.append(ber_hot1**0.5)
   ber_w1.append(ber_warm1**0.5)
   ber_h2.append(ber_hot2**0.5)
   ber_w2.append(ber_warm2**0.5)
   ber_h3.append(ber_hot3**0.5)
   ber_w3.append(ber_warm3**0.5)

   time  = round(ds.current_time.in_units('Myr'),2 )
   t.append(time)

n=0
yt.add_field('bernoulli',function=_bernoulli, units  = 'km**2/s**2')


ber_h1=[]
ber_w1=[]

ber_h2=[]
ber_w2=[]

ber_h3=[]
ber_w3=[]


t=[]


num=range(150,250,10)
for i in num:
    see(i)


f=open('ber.dat','a')
print >>f,'ber_h1=',ber_h1
print >>f, 'ber_w1=',ber_w1
print >>f,'ber_h2=',ber_h2
print >>f, 'ber_w2=',ber_w2
print >>f,'ber_h3=',ber_h3
print >>f, 'ber_w3=',ber_w3
f.close()

fig=plt.figure(figsize=(10,10))
plt.plot(t,ber_h1,'r-',lw=2,label='T>3e4K')
plt.plot(t,ber_h2,'r--',lw=2)
plt.plot(t,ber_h3,'r:',lw=2)
plt.plot(t,ber_w1,'b-',lw=2,label='T<3e4K')
plt.plot(t,ber_w2,'b--',lw=2)
plt.plot(t,ber_w3,'b:',lw=2)
plt.xlabel('time  [Myr]')
plt.ylabel('sqrt(v^2/2 + 2.5*P/rho)  [km/s]')
plt.legend(loc='best')
plt.savefig('ber.png')


