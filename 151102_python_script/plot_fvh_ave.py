import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *


num = range(80,115,5)
fvh=[]
#for i in range(len(num)):
#   fvh.append([])

j=0
for i in num:
   f = open('fvh_'+str(i)+'.dat','r')
   z,fv = loadtxt(f,usecols=(0,1),unpack=True)
   fvh.append(fv)
#   print fvh[j]
   j=j+1

print fvh
print len(fvh),len(fvh[0])
print '[][]=',fvh[1][10]

fvh_ave=[]
fvh_std=[]
j=0
for i in range(len(fvh[0])):
    fv1=[] 
    for k in range(len(num)):
      fv1.append(fvh[k][i])
#    print 'fv1=',fv1
    fvh_ave.append(mean(fv1))
    fvh_std.append(std(fv1))

print z
#print fvh_ave
#print fvh_std
plt.errorbar(z,fvh_ave,yerr=fvh_std,label='Courant 0.5')


fvh=[]
#for i in range(len(num)):
#   fvh.append([])

j=0
for i in num:
   f = open('fvh_reduce_Courant_'+str(i)+'.dat','r')
   z,fv = loadtxt(f,usecols=(0,1),unpack=True)
   fvh.append(fv)
#   print fvh[j]
   j=j+1

print fvh
print len(fvh),len(fvh[0])
print '[][]=',fvh[1][10]

fvh_ave=[]
fvh_std=[]
j=0
for i in range(len(fvh[0])):
    fv1=[]
    for k in range(len(num)):
      fv1.append(fvh[k][i])
#    print 'fv1=',fv1
    fvh_ave.append(mean(fv1))
    fvh_std.append(std(fv1))

print z
#print fvh_ave
#print fvh_std
plt.errorbar(z,fvh_ave,yerr=fvh_std,color='red',label='Courant 0.25')










plt.grid()
plt.title('averaged over t=18.4-25.3Myr')
plt.ylabel('f_V,hot')
plt.xlabel('z/kpc')
plt.legend(loc=2)
plt.savefig('fvh_z_ave.png')
