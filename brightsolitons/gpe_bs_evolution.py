# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft
import os, glob
from gpe_bs_parameters import *
from gpe_bs_plots import *
from gpe_bs_utilities import *
import sys
import subprocess


# Evolution
# ------------------------------------------------------------------------------

def evolution(t0, Dt, z, c0, Vpot_R, Vpot_Rc, V, Ekin_K, write_ev, plots,oscil,time_final,kp):
    """Calculates the evolution of the wavefunction c.
       t0         initial time
       Dt         time step (either imaginary or real)
       z          R-space grid points
       c0         initial wavefunction (FFT order)
       Vpot_R     external potential (FFT order)
       Vpot_Rc    confinement potential (physical order)
       V          external potential (physical order)
       Ekin_K     kinetic energy (FFT order)
       write_ev   writes data into files if 0
       plots      plots data if 0
       oscil      gives the number of oscillation under harmonic potential
                  otherwise (no external potential or barrier) is 0.
       time_final total time of simulation
       kp         K-space grid points (FFT order)
    Global variables:
       Ntime_out  number of time steps for intermediate outputs
       Ntime_fin  total number of time steps
       gint       interaction strength * NormWF
       Npoint     number of points in the grid
       NormWF     norm of the wavefunction
       Zmax       halfwidth of the grid
       Nparticle  number of particles
       a_s        scattering length
       x0         initial position of the soliton
       v          initial velocity of the soliton
       whoz       harmonic oscillator frequency
       xb         position of the barrier
       wb         width of the barrier
       hb         height of the barrier
       wall_h     height of the walls
    Returns the final wavefunction.
    If write_ev == 0:
       the wavefunction (psi) and related magnitudes are written on a file for
           a certain time steps (a different file for each step).
       the file name includes the corresponding time x 1000.
       such files are created on a directory inside the current directory.
       the program checks if the directory where the files will be stored exists
           and if so deletes its contents (otherwise creates a new directory).
    """
    global Ntime_out, Ntime_fin, gint, Npoint, NormWF, Zmax, Nparticle, a_s, x0, v, whoz, xb, wb, hb, wall_h, wall,simtime
    # where the files of evolution will be saved
    if (write_ev==0):
        dir = "bs_evolution" # name of the directory
        ## dir = "bs-gn_%0d-v_%0d-hb_%0d-wb_%0d" % (np.abs(gn)*10, np.abs(v), np.abs(hb), np.abs(wb)) # name of directory (old)
        name = "WfBs" # general name of the files
        if (not os.path.exists(dir)): # creates the directory
            os.makedirs(dir)
        else: # removes its contents if it already exists        
            files_evolution = "%s/%s-*.dat" % (dir, name)
            files_energies = "%s/energies.dat" % (dir)
            for f in glob.glob(files_evolution):
                os.remove( f )
            for f in glob.glob(files_energies):
                os.remove( f )

    # open files for normalization, energies, and some values of c
    if isinstance(Dt, complex): #imaginary time evolution
        fn = open('normalization_imag.dat', 'w')
        fe = open('energies_imag.dat', 'w')
    else: #real time evolution
        fn = open('normalization_real.dat', 'w')
        print( "(Real time evolution)")
        if (write_ev==0):
            fe = open('./%s/energies.dat' % dir, 'w')
        else:
            fe = open('energies_real.dat', 'w')

    # wavefunction and counters
    Ninter = Ntime_fin//Ntime_out # number of outputs (intermediate states)
    c = c0
    j=0; t=t0; l=0
    counter=0

    # define vectors for the energies, time and % of the wf (matrix)
    tevol=np.empty([Ninter+1])
    if oscil==0:
        tmeanval=np.empty(Ntime_fin//50 + 1)
        meanval=np.empty(Ntime_fin//50 + 1)   #x mean value (from integral <x>)
        sigma=np.empty(Ntime_fin//50 + 1)
        vmean=np.empty(Ntime_fin//50 + 1)
    elif oscil!=0:
        tmeanval=np.empty(oscil*60 + 1)
        meanval=np.empty(oscil*60 + 1)   #x mean value (from integral <x>)
        sigma=np.empty(oscil*60 + 1)
        vmean=np.empty(oscil*60 + 1)
    energy_cicle=np.empty([Ninter+1,5])
    wave_function = np.empty([Ninter+1,3])
    number_name_file=[]
    
    # headers and formats for files
    fe.write("# %s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %("time","total energy","chemical potential","kinetic energy","potential energy","interaction energy", "left integral", "inside integral", "right integral"))
    format_psi = "%.2f" + ("\t %.12g")*6 + "\n"
    rmean=open('./bs_evolution/meanvalues.dat', 'w') #more files! this one for real mean value vs t
    rmean.write('#time   <x>    sigma    <v>' + '\n') 
    format_mean = "%.2f" + "\t %.12g" + "\t %.12g" + "\t %.12g" + "\n"
    if V_ext == 2: # potential barrier
        format_e = "%.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \n"
        header_variables = "x", "|psi|^2", "phase", "Re(psi)", "Im(psi)", "V(x)", Nparticle, a_s, 2*Zmax, Npoint, Ntime_fin, Dt, x0, v, xb, wb, hb, energy_cicle[j,1], energy_cicle[j,0]
        header_format = "# %s"+("\t%s")*5+"\n" + "# Number of particle = %s; scattering length = %s; Grid width = %s; Number of points = %s; Total number of time steps = %s; time step = %s " + "initial position of the soliton = %s; initial velocity of the soliton = %s; position of the barrier = %s; width of the barrier = %s; height of the barrier = %s;" + " results: chemical potential = %s; total energy = %s \n"
    else:
        format_e = "%.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \n"
        header_variables = "x", "|psi|^2", "phase", "Re(psi)", "Im(psi)", "V(x)", Nparticle, a_s, 2*Zmax, Npoint, Ntime_fin, Dt, x0, v, energy_cicle[j,1], energy_cicle[j,0]
        header_format = "# %s"+("\t%s")*5+"\n" + "# Number of particle = %s; scattering length = %s; Grid width = %s; Number of points = %s; Total number of time steps = %s; time step = %s " + "initial position of the soliton = %s; initial velocity of the soliton = %s;" + " results: chemical potential = %s; total energy = %s \n"

    # energy and time at t0
    tevol[0]=t0
    energy_cicle[0,:] = Energy(c, Vpot_R, Ekin_K)
    velm=velmean(c, kp) 
    print("Energies:          Emed    mu    Ekin    Epot    Eint")
    print("         initial = %g %g %g %g %g"%(Energy(c0, Vpot_R, Ekin_K)))

    # wavefunction
    cc = ifft(c)*Npoint*NormWF**0.5 # FFT from K3 to R3 and include the wf norm
    psi = changeFFTposition(cc,Npoint,0) # psi is the final wave function
    
    # writes initial energies and wavefunction on a file (if there is a potential barrier)
    if V_ext == 2:
        wave_function[0,:] = list_integrals(np.abs(psi)**2,z)
        fe.write(format_e %(tevol[0], energy_cicle[0,0], energy_cicle[0,1], energy_cicle[0,2], energy_cicle[0,3], energy_cicle[0,4], wave_function[0,0], wave_function[0,1], wave_function[0,2]))
    else:
        fe.write(format_e %(tevol[0], energy_cicle[0,0], energy_cicle[0,1], energy_cicle[0,2], energy_cicle[0,3], energy_cicle[0,4]))

    # writes initial state on the corresponding file
    if (write_ev==0):
        number_name_file.append(round(0)*1000)
        fpsi = open('./%s/%s-%08d.dat' %(dir,name,0), 'w')
        fpsi.write(header_format %(header_variables))
        integral=0
        integral2=0
        integral3=0
        for k in range(0,Npoint-1):
            fpsi.write(format_psi %(z[k], np.abs(psi[k]**2), np.angle(psi[k]), psi[k].real, psi[k].imag, V[k], Vpot_Rc[k]))
            integral=integral+(z[k]*(np.abs((psi[k])**2))*Dz)
            integral2=integral2+(((z[k])**2)*(np.abs((psi[k])**2))*Dz)
            integral3=integral3+(np.sqrt(2*Ekin_K[k])*(np.abs((psi[k])**2))*Dz)
        tmeanval[l]=tevol[j] #the final value written in each position corresponds to the one painted in the original plots
        meanval[l]=integral
        sigma[l]=np.sqrt((integral2)-(integral**2))
        vmean[l]=integral3
        rmean.write(format_mean %(tmeanval[l],meanval[l],sigma[l],velm))

    # time evolution cicle
    for i in range(1, Ntime_fin+1):
        t += np.abs(Dt)
        step=i
        psi=ifft(T_K(Dt, Ekin_K)*c)*Npoint
        c=T_K(Dt, Ekin_K)*fft(T_R_psi(t0,Dt,psi,Vpot_R))/Npoint
        c = normaliza(c,fn); # check norm in the wf
        V = changeFFTposition(Vpot_R,Npoint,0) # in physical order

        if(not(i%Ntime_out)):
            j+=1
            tevol[j] = t
            cc = ifft(c)*Npoint*NormWF**0.5 # FFT from K3 to R3 and include the wf norm
            psi = changeFFTposition(cc,Npoint,0) # psi is the final wave function
            energy_cicle[j,:] = Energy(c, Vpot_R, Ekin_K)
            velm=velmean(c, kp)              
            if V_ext == 2:
                wave_function[j,:] = list_integrals(np.abs(psi)**2,z)
                fe.write(format_e %(tevol[j], energy_cicle[j,0], energy_cicle[j,1], energy_cicle[j,2], energy_cicle[j,3], energy_cicle[j,4], wave_function[j,0], wave_function[j,1], wave_function[j,2]))
            else:
                fe.write(format_e %(tevol[j], energy_cicle[j,0], energy_cicle[j,1], energy_cicle[j,2], energy_cicle[j,3], energy_cicle[j,4]))

            # writes
            if V_ext==0:        
                if(not(i%Ntime_out)):
                # writes a file for each timestep
                    fpsi = open('./%s/%s-%08d.dat' %(dir,name,round(tevol[j],2)*1000), 'w')
                    fpsi.write(header_format %(header_variables))
                    format_psi = "%.2f" + ("\t %.12g")*6 + "\n"
                    l+=1
                    integral=0
                    integral2=0
                    for k in range(0,Npoint-1):
                        fpsi.write(format_psi %(z[k], np.abs(psi[k]**2), np.angle(psi[k]), psi[k].real, psi[k].imag, V[k], Vpot_Rc[k]))
                        integral=integral+(z[k]*(np.abs((psi[k])**2))*Dz)
                        integral2=integral2+(((z[k])**2)*(np.abs((psi[k])**2))*Dz)
                    meanval[l]=integral
                    tmeanval[l]=tevol[j] #the final value written in each position corresponds to the one painted in the original plots
                    sigma[l]=np.sqrt((integral2)-(integral**2))
                    rmean.write(format_mean %(tmeanval[l],meanval[l],sigma[l],velm))                  
                    fpsi.close()
            elif V_ext==2:        
                if(not(i%Ntime_out)):
                    
                    # adds elements to lists tmeanval and meanval for later outputs
                    if(not(i%Ntime_out)):
                        l+=1
                        integral=0
                        integral2=0
                        psileft=0.0
                        psiright=0.0
                        if (tevol[j]>=(round(time_final,2)/simtime - 0.5)) and (tevol[j]<=(round(time_final,2)/simtime+0.5)) and counter==0:
                            print ('Got one! %f' %(tevol[j]))
                            for k in range(0,Npoint-1):
                                if (z[k]>=0.5*wb):
                                    psiright=psiright+(np.abs(psi[k]))**2
                                elif (z[k]<=-0.5*wb):
                                    psileft=psileft+(np.abs(psi[k]))**2
                            counter=1
                            escriu=open('./bs_evolution/llum.dat','w')
                            escriu.write('%f \t %f' %(psileft,psiright))  #left and right |psi|^2
                            escriu.close()
                            
                            #creates gifs for light simulations                            
                            prevdir=os.getcwd()
                            try:
                                os.chdir(os.path.expanduser('./bs_evolution/'))
                                subprocess.call('python sim_1_light.py',shell=True)
                                subprocess.call('python sim_2_light.py',shell=True)
                            finally:
                                os.chdir(prevdir)
                                
                        for k in range(0,Npoint-1):
                            integral=integral+(z[k]*(np.abs((psi[k])**2))*Dz)
                            integral2=integral2+(((z[k])**2)*(np.abs((psi[k])**2))*Dz)
                        meanval[l]=integral
                        tmeanval[l]=tevol[j] #the final value written in each position corresponds to the one painted in the original plots
                        sigma[l]=np.sqrt((integral2)-(integral**2))
                        rmean.write(format_mean %(tmeanval[l],meanval[l],sigma[l],velm))                       

                # writes a file for each timestep
                if(not(i%Ntime_out)):
                    if(write_ev==0):
                        number_name_file.append(round(tevol[j],2)*1000)
                        fpsi = open('./%s/%s-%08d.dat' %(dir,name,round(tevol[j],2)*1000), 'w')
                        fpsi.write(header_format %(header_variables))
                        format_psi = "%.2f" + ("\t %.12g")*6 + "\n"
                        for k in range(0,Npoint-1):
                            fpsi.write(format_psi %(z[k], np.abs(psi[k]**2), np.angle(psi[k]), psi[k].real, psi[k].imag, V[k], Vpot_Rc[k]))
                        fpsi.close()
            elif V_ext==1:
                if(not(i%Ntime_out)):
                    # adds elements to lists tmeanval and meanval for later outputs
                    if(not(i%Ntime_out)):
                        l+=1
                        integral=0
                        integral2=0
                        for k in range(0,Npoint-1):
                            integral=integral+(z[k]*(np.abs((psi[k])**2))*Dz)
                            integral2=integral2+(((z[k])**2)*(np.abs((psi[k])**2))*Dz)
                        meanval[l]=integral
                        tmeanval[l]=tevol[j] #the final value written in each position corresponds to the one painted in the original plots
                        sigma[l]=np.sqrt((integral2)-(integral**2))
                        rmean.write(format_mean %(tmeanval[l],meanval[l],sigma[l],velm))

                # writes a file for each timestep
                if(not(i%(Ntime_out))):
                    if(write_ev==0):
                        number_name_file.append(round(tevol[j],2)*1000)
                        fpsi = open('./%s/%s-%08d.dat' %(dir,name,round(tevol[j],2)*1000), 'w')
                        fpsi.write(header_format %(header_variables))
                        format_psi = "%.2f" + ("\t %.12g")*6 + "\n"
                        for k in range(0,Npoint-1):
                            fpsi.write(format_psi %(z[k], np.abs(psi[k]**2), np.angle(psi[k]), psi[k].real, psi[k].imag, V[k], Vpot_Rc[k]))
                        fpsi.close()
                            
    print("         final   = %g %g %g %g %g"%(Energy(c, Vpot_R, Ekin_K)))
    print("Energy change at last step  = %g"%(energy_cicle[Ninter,0]-energy_cicle[Ninter-1,0]))
    print("  E(final) - E(initial) = %g"%(np.abs(energy_cicle[Ninter,0]-energy_cicle[0,0])))
    
    format_name = "%d" + "\n"
    if V_ext==1 or V_ext==2:
        anoms=np.array(number_name_file)
        noms=open('./bs_evolution/namefiles.dat','w')
        for i in range(0,len(number_name_file)):
            noms.write(format_name %(anoms[i]))
        noms.close()
    else:
        pass
    # closes files
    fn.close(); fe.close(); rmean.close()

    return c
