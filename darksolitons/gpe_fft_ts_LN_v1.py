# In[1]:

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
from gpe_fft_utilities import * # local folder utilities
import numpy.linalg as lin
from pylab import*
import time

close('all')
pi=np.pi
start=time.time()


# Data block5
# ________________________________________________________________________________________________

# In[2]:

Zmax = 15.0              # Grid half length
Npoint =2056              # Number of grid points
Nparticle = 500.0          # Number of particles
a_s = 0.00                # scattering length 
whoz = 1.0               # harmonic oscilator angular frequency
Omega = pi/(2*Zmax)      # reference frame velocity
Ntime_fin = 15000          # total number of time steps
Ntime_out = 1          # number of time steps for intermediate outputs
Dtr = 1.0e-4             # real time step
Dti = 1.0e-4             # imaginary time step

#while True:
#    try:
#        exc=float(raw_input("introduce posicion inicial del soliton de 0 a 6"))
#        while (np.abs(exc)>(6)): # tolerance for the initial position of the soliton
#            print "ERROR: el soliton debe estar dentro del rango de 0 a 6"
#            exc=float(raw_input("introduce posicion inicial del soliton"))
#        break
#    except ValueError:
#        print("Escribe un numero")

f=open('input_2.txt','r')
lines = f.readlines()
f.close()
for line in lines:
    p = line.split()
    exc=(float(p[0]))

# We choose the initial position of soliton:

#while True:
#    try:
#        x0=float(raw_input("introduce posicion inicial del soliton de 0 a 6"))
#        while (np.abs(x0)>(6)): # tolerance for the initial position of the soliton
#            print "ERROR: el soliton debe estar dentro del rango de 0 a 6"
#            x0=float(raw_input("introduce posicion inicial del soliton"))
#        break
#    except ValueError:
#        print("Escribe un numero")
# Print evolution data:

print("Initial data:")
print(" Number of particles = %g"%(Nparticle))
print(" Harmonic oscillator angular frequency = %g"%(whoz))
print(" Domain half length = %g"%(Zmax))
print(" Number of grid points = %g"%(Npoint))
print(" Scattering length = %g"%(a_s))
print(" Total time of evolution = %g"%(Ntime_fin*Dtr))
print(" Real time step = %g"%(Dtr))
print(" Imaginary time = %g"%(Dti))
print(" Intermediate solutions = %g"%(Ntime_fin/Ntime_out-1))


# Derived quantities
# _________________________________________________________________________________________

# In[3]:

NormWF = 1.0/(2*Zmax)           # Wave function (WF) norm
gint = 2*a_s*Nparticle*NormWF   # interaction (nonlinear-term) strength
Dz = 2*Zmax/Npoint              # length step size
Dk = pi/Zmax                    # momentum step size
Kmax = Dk*(Npoint//2)           # maximum momentum
Dt = Dtr-1j*Dti                 # complex time
Ninter = Ntime_fin/Ntime_out    # Number of outputs with the intermediate states
print(" Characteristic interaction energy = %g"%(gint))


# Grid definitions: physical and momentum space
# __________________________________________________________________________________________

# In[5]:

z = np.arange(-Zmax+Dz,Zmax+Dz,Dz)  # physical (R-space) grid points in ascending order 
zp = changeFFTposition(z,Npoint,1)  # (R-space) grid points with FFT order

kp = np.arange(-Kmax+Dk,Kmax+Dk,Dk) # physical (K-space) grid points in ascending order
kp = changeFFTposition(kp,Npoint,1) # (K-space) gridd points with FFT order


# Define kinetic energy and potential:
# ________________________________________________________________________________________

# In[6]:

Ekin_K = 0.5*(kp**2) # Kinetic energy in K space

# Potential energy in R space:
# Harmonic oscillator with angular frequency whoz:

Vpot_R = 0.5*whoz*zp**2  

    
# Main functions:
# ________________________________________________________________________________________
    
# In[7]:

def Energy(c): # Energy (per particle) calculation
    global gint, Vpot_R, Ekin_K, Npoint
    ek = sum(Ekin_K*abs(c)**2)              # Kinetic energy in K
    psi = ifft(c)*Npoint;                   # wf FFT to R
    ep = sum(Vpot_R*abs(psi)**2)/Npoint;    # Potential energy
    ei = 0.5*gint*sum(abs(psi)**4)/Npoint;  # Interaction energy
    em =  ek+ep+ei;                         # average energy
    chem_pot = em+ei;                       # chemical potential
    return em, chem_pot, ek, ep, ei

def T_K (t,Dt,psi): # Action of the time evolution operator over state c in K space
    global Ekin_K
    #psi is the wave function in K space
    # t is the time (which is not used for time independant Hamiltonians)
    # Dt is the complex time step   
    
    return np.exp(-1j*0.5*Dt*Ekin_K)*psi # return action on psi

def T_R_psi(t,Dt,psi): # Action of the time evolution operator over state c in R space
    global gint, Vpot_R
    # Includes the external potential and the interaction operators:
    #       T_R_psi = exp(-i Dt (Vpot_R+ gint|psi|^2) ) c    
    # psi is the wave function in R space
    # t is the time (which is not used for time independant Hamiltonians)
    # Dt is the complex time step 
    
    return np.exp( -1j*Dt*(Vpot_R + gint*(abs(psi)**2)) )*psi # return action on psi

def node(x,n,exc):# initial wave function
    global gint
    if (exc==0):
        fx = np.exp((-x**2.0)/2.0)
    if (exc==1):
        fx = 2.0*x*np.exp((-x**2.0)/2.0)
    if (exc==2):    
        fx = (4.0*x**(2.0)-2.0)*np.exp((-x**2.0)/2.0); # define the initial wf in R3
#    fx=np.tanh(x-x0)*np.tanh(x+x0)
#    fx=np.tanh((x+x0)*np.sqrt(gint))*np.tanh((x-x0)*np.sqrt(gint))
#    fx=x*0.0+10.0
#    fx=2.0*x*np.exp(-(x**2.0)/2.0)
    return fft(fx)/n;   # FFT to K3

def normaliza(c): # normalization to 1
    norm = lin.norm(c)
    if ((norm-1.0)>1.0e-4): # check norm
        print("normalization from: ",norm)
    return c/norm
    

# Choose initial wave function and evolve in imaginary time:
# __________________________________________________________________________________________

# In[8]:
file2=open('lin.txt','w')
file3=open('wf.txt','w')
c0=normaliza(node(zp,Npoint,exc)); # wf at t=0
for i in range (0,int(2*Zmax/Dz)):
    file3.write("%s\n%s\n" %(c0.real[i],c0.imag[i]))
file3.close()

#cc = ifft(c0)*Npoint*NormWF**0.5      # FFT from K3 to R3 and include the wf norm
#psi = changeFFTposition(cc,Npoint,0) # psi is the final wave function
#plot_density(z,psi,Zmax,0)
#file4=open('WfDs_Lin-%08d.txt'%(0),'w')
#for i in range (0,int(2*Zmax/Dz)):
#    file4.write("%s\t%s\n" %(z[i],(abs(psi)**2)[i]))
#file4.close()
  
for N in range (1,750): 
    # evolve in time: parameters
    t0=0.0
    tevol=np.empty([Ninter+1])          # time vector
    energy_cicle=np.empty([Ninter+1,5]) # put the energies in a matrix
    energy_cicle[0,:] = Energy(c0)      # Energies at t=0
    creal=np.empty([Npoint])
    cimag=np.empty([Npoint])
    c=np.empty([Npoint],dtype=np.complex_)
    #initiation of time evolution:
    
    file3=open('wf.txt','r')  
    for k in range(Npoint):
        creal[k]=file3.readline()
        cimag[k]=file3.readline()
        c[k]=creal[k]+1j*cimag[k]
    file3.close()
        
    tevol[0]=t0
    j=0
    t=0
    #imaginary time evolution cicle:
    for i in range(1, Ntime_fin+1): 
        t += Dt.real
        psi=ifft(T_K(t0,-1j*Dt.real,c))*Npoint
        c=T_K(t0,-1j*Dt.real,fft(T_R_psi(t0,-1j*Dt.real,psi))/Npoint)
        c = normaliza(c); # check norm in the wf
        if(not(i%Ntime_out)):
            j+=1
            tevol[j] = t
            energy_cicle[j,:] = Energy(c)
        if (np.abs(energy_cicle[j,1]-energy_cicle[j-1,1])<(1e-4)):
                    break
#    print (energy_cicle[j,1],energy_cicle[j,0])
    cc = ifft(c)*Npoint*NormWF**0.5      # FFT from K3 to R3 and include the wf norm
    psi = changeFFTposition(cc,Npoint,0) # psi is the final wave function
    
    file3=open('wf.txt','w')
    for i in range (0,int(2*Zmax/Dz)):
        file3.write("%s\n%s\n" %(c.real[i],c.imag[i]))
    file3.close()
#    plot_density(z,psi,Zmax,t)
    if (not(N%10)):
        file4=open('WfDs_Lin-%08d.txt'%(N/10),'w')
        for i in range (0,int(2*Zmax/Dz)):
            file4.write("%s\t%s\n" %(z[i],(abs(psi)**2)[i]))
#    plot_density(z,psi,Zmax,t)      
    file2.write ("%s\t%s\t%.14e\t%.14e\n"%(a_s,gint,energy_cicle[j,1],energy_cicle[j,0]))     
    a_s+=0.0002
    gint = 2*a_s*Nparticle*NormWF
    
file3.close()
file2.close()
file4.close()
#Ntime_fin=8800     # total number of time steps
#Ntime_out = 100              # number of time steps for intermediate outputs
#Dtr=1.0e-3                   # real time step
#Dti=1.0e-3                   # imaginary time step
#Dt = Dtr-1j*Dti              # complex time
#Ninter = Ntime_fin/Ntime_out # Number of outputs with the intermediate states
#f4=plt.figure()
#for i in range(1, Ntime_fin+1): # time evolution cicle
#    t += Dt.real
#    psi=ifft(T_K(t0,Dt.real,c))*Npoint
#
#    c=T_K(t0,Dt.real,fft(T_R_psi(t0,Dt.real,psi))/Npoint)
#    c = normaliza(c); # check norm in the wf         
#    
#
#    if(not(i%Ntime_out)):
#        j+=1
#        tevol[j] = t
## Write energies from function Energy        
#        energi=(Energy(c))
## Representation of intermediate solutions
#        cc = ifft(c)*Npoint*NormWF**0.5 # FFT from K3 to R3 and include the wf norm
#        psi = changeFFTposition(cc,Npoint,0) # psi is the final wave function
#        
#        plt.title('Evolution in time'%(tevol[Ninter]),fontsize=15)
#        plt.xlabel('$x/a_{ho}$',fontsize=15)
#        plt.xticks(np.arange(-Zmax, Zmax+1,Zmax/2))
#        plt.locator_params('y',nbins=3)
#        plt.plot(z, abs(psi)**2, 'b--',label='$|\psi|^2$') # plot density
##        plt.plot(z, psi.real, 'r.',label='real$(\psi)$')
##        plt.plot(z, psi.imag, 'b--',label='imag$(\psi)$')
##        plt.plot(z, np.angle(psi), 'b.',label='$Arg(\psi)$')
#        f4.show()
## Minus of density (soliton) 
#print a_s,Nparticle
#point= int(0.5/Dz)
#min1=np.empty([point+10])
#min2=np.empty([point+10])        
#
#for i in range (len(z)/2-point-10,len(z)/2):
#    min1[i-int(len(z)/2-point-10)]=str((abs(psi)**2)[i])
#for i in range (len(z)/2,len(z)/2+point+10):
#    min2[i-len(z)/2]=str((abs(psi)**2)[i])
#
#for i in range (len(min1)):
#    if (min(min1)==min1[i]):
#        pos_min1=z[i+int(len(z)/2-point-10)]
#    if (min(min2)==min2[i]):
#        pos_min2=z[i+len(z)/2]
#print pos_min1,pos_min2