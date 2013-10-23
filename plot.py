import sys
import os
import time

import numpy as np
import scipy.io as sio
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

def plot(plot_type, save_flag):
#    infile = "acr_sp_0.0C_2x1_40.mat"
#    infile = "acr_sp_0.0C.mat"
    infile = "acr_sp_0.001C.mat"
#    infile = "acr_sp.mat"
    data = sio.loadmat(infile)
#    print data.keys()
#    print data['mpet.c_lyte_sep']
#    print data['mpet.c_lyte_trode']
#    print data['mpet.phi_applied']
#    print data['mpet.phi_lyte_sep']
#    print data['mpet.phi_lyte_trode']
#    print data['mpet.solid_vol0_part0']
#    print data['mpet.solid_vol9_part0']
#    print data['mpet.j_plus']
#    print data['mpet.currset']
#    print np.sum(data['mpet.j_plus'][0])
#    print np.sum(data['mpet.j_plus'][1])
#    print data['mpet.particle_numVols']
#    zzz
    # Pick out some useful parameters
    Vstd = float(data['mpet.Vstd'][0][0])        # Standard potential, V
    k = float(data['mpet.k'][0][0])       # Boltzmann constant
    T = float(data['mpet.Tabs'][0][0])             # Temp, K
    e = float(data['mpet.e'][0][0])       # Charge of proton, C
    # Extract the reported simulation times
    times = data['mpet.phi_applied_times'][0]
    numtimes = len(times)
    Ntrode = int(data['mpet.NumTrode'][0][0])
    Nsep = int(data['mpet.NumSep'][0][0])
    numpart = int(data['mpet.NumPart'][0][0])

    # Plot voltage profile
    if plot_type == "v":
        fig = plt.figure()
#        ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
        ax = fig.add_subplot(111)
#        print data['mpet.phi_applied_times'][0]
#        print data['mpet.phi_applied'][0]
        voltage = Vstd - (k*T/e)*data['mpet.phi_applied'][0]
        ax.plot(times, voltage)
        plt.show()

    # Plot concentration profiles
    elif plot_type == "c":
        if save_flag:
            outputdir = "{name}_image_output".format(name=infile[0:-4])
            os.mkdir(outputdir)
        else:
            # "interactive mode on"
            plt.ion()
#        numtimes = len(data['mpet.phi_applied_times'][0])
        fig = plt.figure()
#        ax = fig.add_axes([0.08, 0.08, 0.85, 0.85])
        ax = fig.add_subplot(111)
        ax.set_ylim((0, 1))
        ax.set_xlabel('Particle Length [nm]')
        ax.set_ylabel('Concentration [fraction]')
        sol = 'mpet.solid_vol9_part0'
        datay = data[sol][0]
#        print datay
#        Lx = data['mpet.Lx'][0]
        Lx = 1.
        numy = len(datay)
        datax = np.linspace(0, Lx, numy)
        # returns tuble of line objects, thus comma
        line1, = ax.plot(datay)
#        for i in range(5):
        for i in range(numtimes):
#            print "img {num}/{tot}".format(num=i, tot=numtimes)
            datay = data[sol][i]
            line1.set_ydata(datay)
            if save_flag:
                filename = os.path.join(outputdir,
                        'c{num:06d}.png'.format(num=i))
                fig.savefig(filename)
            else:
                fig.canvas.draw()
                time.sleep(1e-3)
#            fig.clear()

    elif plot_type == "e":
        if save_flag:
            outputdir = "{name}_image_output".format(name=infile[0:-4])
            os.mkdir(outputdir)
        else:
            # "interactive mode on"
            plt.ion()
#        numtimes = len(data['mpet.phi_applied_times'][0])
#        numtimes = len(times)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim((0, 1))
        ax.set_xlabel('Battery Position [um]')
        ax.set_ylabel('Concentration of electrolyte [fraction]')
        sep = 'mpet.c_lyte_sep'
        trode = 'mpet.c_lyte_trode'
        datay_sep = data[sep][0]
        datay_trode = data[trode][0]
        print datay_sep
        print datay_trode
        Lsep = data['mpet.Lsep'][0] * 1e6
        Ltrode = data['mpet.Ltrode'][0] * 1e6
        datay = np.hstack((datay_sep, datay_trode))
        print datay.shape
        numy = len(datay)
        datax = np.linspace(0, (Lsep + Ltrode), numy)
        # returns tuble of line objects, thus comma
        line1, = ax.plot(datax, datay)
        for i in range(numtimes):
            datay_sep = data[sep][i]
            datay_trode = data[trode][i]
            print datay_sep
            print datay_trode
            datay = np.hstack((datay_sep, datay_trode))
#            print datay.shape
            line1.set_ydata(datay)
            if save_flag:
                filename = os.path.join(outputdir,
                        'c{num:06d}.png'.format(num=i))
                fig.savefig(filename)
            else:
                fig.canvas.draw()
                time.sleep(1e-3)

    elif plot_type == "csld":
        if save_flag:
            outputdir = "{name}_image_output".format(name=infile[0:-4])
            os.mkdir(outputdir)
        else:
            # "interactive mode on"
            plt.ion()
#        Ntrode = 1
        fig, ax = plt.subplots(numpart, Ntrode, squeeze=False,
                sharey=True)
        sol = np.empty((numpart, Ntrode), dtype=object)
        lens = np.zeros((numpart, Ntrode))
        lines = np.empty((numpart, Ntrode), dtype=object)
        for i in range(numpart):
            for j in range(Ntrode):
                sol[i, j] = "mpet.solid_vol{j}_part{i}".format(i=i, j=j)
#                print data["mpet.psd_lengths"]
                lens[i, j] = data["mpet.psd_lengths"][0][j, i]
#                ax[i, j].set_frame_on(False)
                ax[i, j].xaxis.set_ticks_position('none')
#                ax[i, j].yaxis.set_ticks_position('none')
                ax[i, j].xaxis.set_ticklabels('')
#                ax[i, j].yaxis.set_ticklabels('')
                datay = data[sol[i, j]][0]
                numy = len(datay)
                datax = np.linspace(0, lens[i, j], numy)
                ax[i, j].set_ylim((0, 1))
                ax[i, j].set_xlim((0, lens[i, j]))
                line, = ax[i, j].plot(datax, datay)
                lines[i, j] = line
        for tval in range(numtimes):
            for i in range(numpart):
                for j in range(Ntrode):
                    datay = data[sol[i, j]][tval]
                    lines[i, j].set_ydata(datay)
            if save_flag:
                filename = os.path.join(outputdir,
                        'c{num:06d}.png'.format(num=i))
                fig.savefig(filename)
            else:
                fig.canvas.draw()
                time.sleep(1e-3)

    else:
        raise Exception("Unexpected plot type argument."
                + "Try 'v' or 'c' or 'csld'")
    return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot_type = sys.argv[1]
    else:
        plot_type = "v"
    save_flag = False
    plot(plot_type, save_flag)
