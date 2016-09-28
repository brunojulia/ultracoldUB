# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
from gpe_bs_parameters import *

#opening outputs from gpe_bright_solitons.py

#energies
energies=open('./bs_evolution/energies.dat','r')
time=np.empty([402])
e_tot=np.empty([402])
e_kin=np.empty([402])
e_pot=np.empty([402])
e_int=np.empty([402])
mu=np.empty([402])
energy_lines=energies.readlines()
for i in xrange(0,len(energy_lines)):
    if i==0:
        pass
    else:
        line_values=(energy_lines[i]).split('\t')
        time[i]=float(line_values[0])
        e_tot[i]=float(line_values[1])
        e_kin[i]=float(line_values[3])
        e_pot[i]=float(line_values[4])
        e_int[i]=float(line_values[5])
        mu[i]=float(line_values[2])
        
#mean value
meanvals=open('./bs_evolution/meanvalues.dat','r')
time_m=np.empty([42])
mean=np.empty([42])
mean_vals=meanvals.readlines()
for i in xrange(0,len(mean_vals)):
    if i==0:
        pass
    else:
        line_mean=(mean_vals[i]).split('\t')
        time_m[i]=float(line_mean[0])
        mean[i]=float(line_mean[1])
        
#evolution
z=np.empty([1023])
psi_square=np.empty([1023])
V_tot=np.empty([1023])
V_c=np.empty([1023])


#Creating plots from data

#energies
f1=plt.figure()
plt.title('Convergence',fontsize=15)
plt.xlabel('time ($t \, \\omega_{\\xi}$)',fontsize=15)
plt.ylabel('Energy per particle ($E/\\hbar \,\\omega_{\\xi}$)',fontsize=15)
plt.locator_params('y',nbins=3)
plt.plot(time, e_tot, 'r-',label="$E_{med}$") # plot only average energy
plt.plot(time, e_kin, 'b-',label="$E_{kin}$")
plt.plot(time, e_pot, 'g-',label="$E_{pot}$")
plt.plot(time, e_int, 'y-',label="$E_{int}$")
plt.plot(time, mu, 'm',label="$\\mu$")
plt.legend(fontsize=15)

#mean value
f2=plt.figure()
plt.title('Mean value of the wave function at $t$',fontsize=15)
plt.ylabel('Mean value', fontsize=15)
plt.xlabel('time ($t \, \\omega_{\\xi}$)',fontsize=15)
plt.xlim(0,20)
plt.ylim(-128,128)
plt.locator_params('y',nbins=3)
plt.plot(time_m,mean, marker='.', linestyle='None', markersize=5)

#evolution
f3=plt.figure()
plt.title('Evolution of the initial wavefunction (real time)',fontsize=15)
plt.xlabel('$z$',fontsize=15)
plt.xticks(np.arange(-Zmax, Zmax+1,Zmax/2))
plt.axis((-Zmax,Zmax,0,0.3))
plt.locator_params('y',nbins=3)
fn=open('potencials.dat','w')
for i in xrange(0,201,5):
    evol=open('./bs_evolution/WfBs-%08d.dat' %(i*100), 'r')
    lines_evol=evol.readlines()
    for l in xrange(0,len(lines_evol)):
        if (l==0) or (l==1):
            pass
        else:
            line_ev=lines_evol[l].split('\t')
            z[l-2]=line_ev[0]
            psi_square[l-2]=line_ev[1] 
            if i==0:            
                V_tot[l-2]=line_ev[5] #written only once
                V_c[l-2]=line_ev[6]
            else:
                pass
    if i==0:
        plt.plot(z,psi_square, 'r-',label='$|\psi_0|^2$')
    elif i==5:
        plt.plot(z,psi_square, 'b--',label='$|\psi|^2$')
    else:
        plt.plot(z,psi_square, 'b--')
plt.plot(z,V_tot, 'g--',label='potential')
plt.plot(z,V_c, 'g--') #for the confinement potential, to make the plot more visual
for i in xrange(0,len(V_c)):
    fn.write("%f \t %f \t %f \t %f \n" %(z[i],psi_square[i],V_tot[i],V_c[i]))
fn.close()    
plt.legend(fontsize=15)

#show plots
f2.show()
f1.show()
f3.show()
plt.pause(-1)