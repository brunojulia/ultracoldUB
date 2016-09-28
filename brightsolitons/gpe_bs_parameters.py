# coding: utf-8
import numpy as np
from gpe_bs_utilities import *
pi=np.pi


# Data block
# ------------------------------------------------------------------------------
#importing data file with input parameters
infile=open('input.dat', 'r')
listin=infile.readlines()
values=listin[1].split('\t')    #read the line with inputs
infile.close()

int_str=int(values[0])          #option for gn -> Scattering length
velocity=float(values[1])         #initial velocity
def_w=str(values[2])            #confinement
V_ext=int(values[3])            #external potential
if V_ext==2:
    barrier_w=int(values[4])    #values for square barrier if it is chosen
    barrier_h=float(values[5])
else:
    pass

if int_str == 1:
    a_s = -0.005e-3
elif int_str == 2:
    a_s = -0.01e-3
elif int_str == 3:
    a_s = -0.02e-3

Zmax = 2.0**7                       # Grid half length
Npoint = 2**10                      # Number of grid points (min. 2**8)
Nparticle = 20e+3                   # Number of particles
whoz = 0.035                         # harmonic oscilator angular frequency
Ntime_out = 50                      # number of time steps for intermediate outputs
Dtr = 1.0e-3                        # real time step (min. 1.0e-2)
Dti = 1.0e-1                        # imaginary time step
time_final = 20.0                   # final time
Ntime_fin = int(time_final/Dtr)     # total number of time steps


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
x0 = -10.0                          # initial position of the soliton
v = float(velocity)                 # initial velocity of the soliton


# Potential walls and barrier
# ------------------------------------------------------------------------------

if def_w == "Y" or def_w == "y":
    wall = 1
elif def_w == "N" or def_w == "n":
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

    if barrier_w == 1:
        wb = 0.5 * xi
    elif barrier_w == 2:
        wb = 1.0 * xi
    elif barrier_w == 3:
        wb = 2.0 * xi

    xbr = xb + 0.5*wb                   # position of the right wall (barrier)
    xbl = xb - 0.5*wb                   # positon of the left wall (barrier)

    hb = height_barrier(barrier_h)

else:
    xb, hb, wb = 0, 0, 0