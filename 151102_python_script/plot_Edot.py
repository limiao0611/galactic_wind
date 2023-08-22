from numpy import *
#from scipy import *
#from scipy.integrate import quad
#from scipy.integrate import romberg
#from matplotlib import *
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt


from matplotlib  import cm

fn = 'Edot_t.dat'
f=open(fn,'r')
i,time, Edot_wind, Edot_rad, Edot_tot_allgas, Edot_all_minus, Edot_SN, Edot_PEH , Etot,Eth,Ek = loadtxt(f,usecols=(0,1,3,5,7,9,11,13,15,17,19),unpack=True)
#i,time,E=loadtxt(f,usecols=(0,1,3),unpack=True)
f.close()
print time
print Edot_PEH

plt.plot(time,Edot_wind,'b',label='Edot_wind',lw=2.)
plt.plot(time,Edot_rad,'r',label='Edot_rad',lw=2.)
plt.plot(time,Edot_tot_allgas,'g',label='Edot_gas',lw=1.5)
plt.plot(time,Edot_SN,'c',label='Edot_SN',lw=2.)
plt.xlabel('time (Myr)')
plt.ylabel('E_dot (erg/s)')
plt.yscale('log')
plt.legend(loc=3)
plt.savefig('Edot_t.png')
#plt.show()
