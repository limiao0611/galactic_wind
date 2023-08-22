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


def _z_den_flux(field,data):
    return (data['density']*data['z-velocity'])


def see(i):
   fn = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   fvh=[]
   fvw=[]
   fvc=[]
   nbar=[]
   nbar_h=[]
   nbar_w=[]
   nbar_c=[]
   z=[]
   dz= 0.04
   z1=-0.5
   z2 = z1+dz
   fn='fv_hwc_'+str(i)+'.dat'
   f=open(fn,'w')

   while (z2<=0.5):
     bx=ds.box([0,0,z1],[ds.domain_dimensions[0],ds.domain_dimension[1],z2])
     total_vol = bx.quantities.total_quantity('cell_volume')

     hot = bx.cut_region("obj['temperature']>3e5")
#     warm = (bx.cut_region("obj['temperature']<3e5")).cut_region("obj['temperature']>1e3")
     cold = bx.cut_region("obj['temperature']<1e3")

     hot_vol = hot.quantities.total_quantity('cell_volume')
#     warm_vol = warm.quantities.total_quantity('cell_volume')
     cold_vol = cold.quantities.total_quantity('cell_volume')
     #warm_vol=1.-hot_vol - cold_vol

     nbar0 = bx.quantities.weighted_average_quantity(fields='density',weight='cell_volume')
     nbar.append(nbar0)

     fh= hot_vol*1.0/total_vol
     fvh.append(fh)
     nbar_h0 = hot.quantities.weighted_average_quantity(fields="density", weight='cell_volume')
     nbar_h.append(nbar_h0)
     nbar_c0 = cold.quantities.weighted_average_quantity(fields="density", weight='cell_volume')
     if ( (nbar_c0 > 0)== False ): nbar_c0= YTQuantity(0.0, 'g/cm**3')
     nbar_c.append(nbar_c0)

     fc= cold_vol*1.0/total_vol
     fvc.append(fc)

     fw= 1-fh-fc
     fvw.append(fw)

     nbar_w0 = (nbar0- nbar_h0*fh - nbar_c0*fc)/fw
     nbar_w.append( nbar_w0  )

     print 'nbar=',nbar0, nbar_h0, nbar_w0, nbar_c0

     z.append((z1+z2)/2.*5)
     z1=z1+dz
     z2=z1+dz
     print >> f, (z1+z2)/2.*5, fh,fw,fc

   time=round(ds.current_time.in_units('Myr'),1)


   fig=plt.figure(figsize=(10,15))
   plt.subplot(211)
   plt.plot(z,fvh,'-',lw=2,c='r',label='T>3e5K')
   plt.plot(z,fvw,'-',color='orange',lw=2,label='1e3<T<3e5K')
   plt.plot(z,fvc,'-',color='blue',lw=2,label='T<1e3K')
   plt.title('t='+str(time)+ 'Myr' )
   plt.xlabel('z [kpc]')
   plt.ylabel('Volume fraction')
#   plt.legend(loc='best', fancybox=True, framealpha=0.4)
#plt.yscale('log')
   plt.ylim(0,1)

   plt.subplot(212)
   plt.plot(z,nbar,'-',lw=2.5,c='black',label='all')
   plt.plot(z,nbar_h,'-',lw=2.0,c='red',label='T>3e5K')
   plt.plot(z,nbar_w,'-',lw=2.0,c='orange', label='1e3<T<3e5K')
   plt.plot(z,nbar_c,'-',lw=2.0,c='blue',label='T<1e3K')
   plt.xlabel('z [kpc]')
   plt.ylabel('Mean density [g/cc]')
   plt.ylim(1e-28,1e-23)
   plt.yscale('log')
   plt.legend(loc='best', fancybox=True, framealpha=0.4,prop={'size':18})
   plt.savefig('z_fv_nbar_hwc_'+str(i)+'vertical.png')

   global n
   n=n+1

n=0
yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
num=[180,200,220,240]
for i in num:
    see(i)



