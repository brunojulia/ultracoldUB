# coding: utf-8
import numpy as np
from gpe_bs_utilities import *
pi=np.pi


# Data block
# ------------------------------------------------------------------------------
#importing data file with input parameters
infile=open('input.txt', 'r')
listin=infile.readlines()
values=listin[0].split(' \t')    #read the line with inputs, only contains one line
infile.close()

V_ext=int(values[0])
if V_ext==0:    #no external potential    
    x0=float(values[2])
    int_str=int(values[1])
    velocity=float(values[3])
    def_w=int(values[4])
#    print V_ext,int_str,x0,velocity,def_w  #to check if it works or not
elif V_ext==1:  #harmonic trap
    int_str=int(values[1])
    x0=float(values[2])
    oscil=int(values[3])
    def_w=int(values[4])
#    print V_ext,int_str,x0,oscil,def_w
elif V_ext==2:  #wall
    int_str=int(values[1])
    x0=float(values[2])
    velocity=float(values[3])
    def_w=int(values[4])
    barrier_w=int(values[5])
    barrier_h=float(values[6])
#    print V_ext,int_str,x0,velocity,def_w,barrier_w,barrier_h
    
if int_str == 1:
    a_s = -0.005e-3
elif int_str == 2:
    a_s = -0.01e-3
elif int_str == 3:
    a_s = -0.02e-3


whoz = 1.0                          # harmonic oscilator angular frequency with f=2*pi
freq = 2.0*np.pi/whoz               #frequency

if V_ext==1:
    Zmax=2.0**5
    time_final=float(oscil)*freq
    Dti=1.0e-1                      # imaginary time step (not used)
    Ntime_fin=int(3.0e4)            # supposed as in the original one for total time=20 and Dtr=10^-3
    Dtr=float(time_final/float(Ntime_fin))
    Npoint = 2**10                      # Number of grid points (min. 2**8)
    velocity=0.0
else:
    Zmax = 2.0**7    
    Dtr = 1.0e-3                        # real time step (min. 1.0e-2)
    Dti = 1.0e-1                        # imaginary time step
    time_final = 20.0                   # final time
    Ntime_fin = int(time_final/Dtr)     # total number of time steps
    Npoint = 2**10                      # Number of grid points (min. 2**8)

#Zmax = 2.0**7                       # Grid half length
Nparticle = 20e+3                   # Number of particles
Ntime_out = 50                      # number of time steps for intermediate outputs

# Derived quantities and parameters of the initial wavefunction (bright soliton)
# ------------------------------------------------------------------------------

NormWF = 1.0/(2*Zmax)               # Wave function (WF) norm
Dz = 2*Zmax/Npoint                  # length step size
Dk = pi/Zmax                        # momentum step size
Kmax = Dk*(Npoint//2)               # maximum momentum
Dt = Dtr-1j*Dti                     # complex time
Ninter = Ntime_fin//Ntime_out       # Number of outputs with the intermediate states
gn = 2*a_s*Nparticle                # interaction (nonlinear-term) strength
gint = gn*NormWF                    # int. strenght, with factor NormWF
xi = 1.0/(np.abs(gn)**2*0.5)**0.5   # healing length
v = float(velocity)                 # initial velocity of the soliton


# Potential walls and barrier
# ------------------------------------------------------------------------------

if def_w == 1:
    wall = 1
elif def_w == 0:
    wall = 0

wall_h = 100.0                      # height of the walls


def height_barrier(a):
    """Height of the barrier, defined as 'a' times the initial kinetic energy of the soliton
    with initial velocity 'v', defined as Ekin = 0.5 * v**2.
    Returns Ekin * a.
    """
    global v
    height = a * v**2 * 0.5
    return height

# potential barrier

if V_ext == 2:

    xb = 0.0*Zmax                       # position of the potential barrier

#    if barrier_w == 1:
#        wb = 0.5 * xi
#    elif barrier_w == 2:
#        wb = 1.0 * xi
#    elif barrier_w == 3:
#        wb = 2.0 * xi
    wb=barrier_w*xi  #with the new input, barrier_W has already the correct value (0.5, 1.0 or 2.0)

    xbr = xb + 0.5*wb                   # position of the right wall (barrier)
    xbl = xb - 0.5*wb                   # positon of the left wall (barrier)

    hb = height_barrier(barrier_h)

else:
    xb, hb, wb = 0, 0, 0