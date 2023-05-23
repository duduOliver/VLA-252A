# TODO Make unittest for all functionalities
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RC_hpf import RCHighPass
from RC_lpf import RCLowPass
from BPF import RCBandPass

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