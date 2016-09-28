# coding: utf-8

# ## FFT solver for 1D Gross-Pitaevski equation

# We look for the complex function $\psi(x)$ satisfying the GP equation
#
# $ i\partial_t \psi = \frac{1}{2}(-i\partial_x - \Omega)^2\psi+ V(x)\psi + g|\psi|^2\psi $,
#
# with periodic boundary conditions.
#
# Integration: pseudospectral method with split (time evolution) operator;
# that is evolving in real (R) or momentum (K) space according to the operators
# in the Hamiltonian, i.e.
# first we evaluate
#
# $\hat{\psi}(x,\frac{t}{2})=\mathcal{F}^{-1}\left[\exp\left(-i \frac{\hbar^2 k^2}{2} \frac{t}{2}\right)\,\psi(k,0)\right] $
#
# and later
#
# $\psi(k,t) = \exp(-i \frac{\hbar^2 k^2}{2} \frac{t}{2})\,
# \mathcal{F}\left[\exp\left(-i (V(x)+\lvert \hat{\psi}(x,\frac{t}{2})\rvert ^2)\, t \right)\,\hat{\psi}(x,\frac{t}{2}) \,
# \right]$
#
# where $\cal{F}$ is the Fourier transform.
# _______________________________________________________________________________
# _______________________________________________________________________________

# Import libraries and general definitions
# ------------------------------------------------------------------------------

import numpy as np
import time
import os
import subprocess

from scipy.fftpack import fft, ifft
from gpe_bs_utilities import *
from gpe_bs_parameters import *
from gpe_bs_evolution import *
pi=np.pi


start = time.time()


# Grid definitions: physical and momentum space; kinetic energy in K space
# ------------------------------------------------------------------------------

z = np.arange(-Zmax+Dz,Zmax+Dz,Dz)  # R-space grid points in ascending order
zp = changeFFTposition(z,Npoint,1)  # R-space grid points with FFT order
kp = np.arange(-Kmax+Dk,Kmax+Dk,Dk) # K-space grid points in ascending order
kp = changeFFTposition(kp,Npoint,1) # K-space grid points with FFT order
Ekin_K = 0.5*(kp)**2                # Kinetic energy in K space


# Initial state (bright soliton) and potential
# ------------------------------------------------------------------------------

t0=0.0

c0 = normaliza(bright_soliton(zp,Npoint,x0,gn),0);
c = c0 # initialize
psi = changeFFTposition(ifft(c)*Npoint*NormWF**0.5,Npoint,1)
psi0 = psi

# initial potential
Vpot_R,Vpot_Rc = Vpot(V_ext, z)


#  Evolve in time the initial state
# ------------------------------------------------------------------------------

# checks evolution with imaginary time (comment next line to ignore it)
# c = evolution(t0, -1j*Dti, z, c0, Vpot_R, V, Ekin_K, 1, plots)

# initial kick to the soliton (velocity v)
psi = psi *np.exp(+1j*v*(z-x0))
cc = changeFFTposition(psi,Npoint,1)
c = fft( cc / (Npoint*NormWF**0.5)); c = normaliza(c,1); # check norm in the wf
c0 = c # initial wavefunction for the dynamic evolution (used in the animation)

# saves the initial wavefunction (psi**2) and potential on a file
fv = open('initial.dat', 'w')
format_v = "%.2f \t %.4f \t %.12g \n"
for i in range(0,Npoint-1):
    fv.write(format_v %(z[i],Vpot_R[i],np.abs(psi[i])**2))
fv.close()

# rearranges the potential with FFT order
V = Vpot_R # R3
Vpot_R = changeFFTposition(Vpot_R,Npoint,1) # K3

# evolution (real time)
t0=0.0
c = evolution(t0, Dtr, z, c0, Vpot_R, Vpot_Rc, V, Ekin_K, 0,1)

end = time.time()