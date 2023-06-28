# TODO Make unittest for all functionalities
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pywdf
from utils.new_plot_freqz import new_plot_freqz
from LCSecOrd_BPF import SecondOrderBandPass

if __name__ == "__main__":
    SAMPLERATE = int(48e3)
    R = pywdf.Resistor(1000)
    C = pywdf.Capacitor(1e-6, SAMPLERATE)
    n_samples = int(4 * SAMPLERATE)
    white_noise = np.random.standard_normal(size=n_samples)

    frequency = "130" #@param [50, 130, 320, 800, 2000, 5000, 12500]
    center_frequency = int(frequency)
    fft_size = int(2 ** 15)
    yLim_min = -20
    yLim_max = 0

    delta = np.zeros(int(1 * SAMPLERATE))
    delta[0] = 1
    bpf = SecondOrderBandPass(SAMPLERATE, center_frequency)

    print("Center Frequency: ", center_frequency)
    print("Improved graph")
    new_plot_freqz(bpf, yLim_min, yLim_max) 
