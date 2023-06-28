# TODO Make unittest for all functionalities
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pywdf
from utils.new_plot_freqz import new_plot_freqz
from RC_hpf import RCHighPass
from RC_lpf import RCLowPass
from LC_BPF import RCBandPass

if __name__ == "__main__":
    SAMPLERATE = int(48e3)
    cutoff = 1000
    hpf = RCHighPass(SAMPLERATE, cutoff)
    hpf.plot_freqz()
    
    cutoff = 100
    lpf = RCLowPass(SAMPLERATE, cutoff)
    lpf.plot_freqz()
    
    center_frequency = 10
    bpf = RCBandPass(SAMPLERATE, center_frequency)
    bpf.plot_freqz()
    
    # New test units added on 20230523 
    SAMPLERATE = int(48e3)
    R = pywdf.Resistor(1000)
    C = pywdf.Capacitor(1e-6, SAMPLERATE)
    n_samples = int(4 * SAMPLERATE)
    white_noise = np.random.standard_normal(size=n_samples)

    delta = np.zeros(int(1 * SAMPLERATE))
    delta[0] = 1

    frequency = 130
    center_frequency = int(frequency)
    fft_size = int(2 ** 15)
    yLim_min = -20
    yLim_max = 0
    bpf = RCBandPass(SAMPLERATE, center_frequency)

    out_bpf = bpf(delta)
    print("Center Frequency: ", center_frequency)
    print("Improved graph")
    new_plot_freqz(bpf, yLim_min, yLim_max) 