import numpy as np
from pywdf.core.circuit import Circuit
from RC_hpf import RCHighPass
from RC_lpf import RCLowPass

def octave_distance(f1:float, f2:float):
  return np.log2(f2/f1)

class RCBandPass(Circuit):
    def __init__ (self, sample_rate: int, central_freq: float) -> None:
        self.fs = sample_rate
        self.central_freq = central_freq
        cf = [50, 130, 320, 800, 2000, 5000, 12500]
        n_octave = octave_distance(cf[0], cf[1])
        n_octave_over2 = n_octave / 4
        self.lowpass_cutoff = cf[0] * 4 ** n_octave_over2
        self.highpass_cutoff = cf[0] / (4 ** n_octave_over2)
        self.lowpass_filter = RCLowPass(self.fs, self.lowpass_cutoff)
        self.highpass_filter = RCHighPass(self.fs, self.highpass_cutoff)
        super().__init__(self.lowpass_filter, self.highpass_filter, self.highpass_filter)

    def process_sample(self, sample: float):
        lowpass_output = self.lowpass_filter.process_sample(sample)
        bandpass_output = self.highpass_filter.process_sample(lowpass_output)
        return bandpass_output
    #this is for the 50 hertz?
    def set_central_freq(self, new_central_freq: float):
        if self.central_freq != new_central_freq:
            self.central_freq = new_central_freq
            cf = [50, 130, 320, 800, 2000, 5000, 12500]
            n_octave = octave_distance(cf[0], cf[1])
            n_octave_over2 = n_octave / 2
            self.lowpass_cutoff = cf[0] * 2 ** n_octave_over2
            self.highpass_cutoff = cf[0] / (2 ** n_octave_over2)
            self.lowpass_filter = RCLowPass(self.fs, self.lowpass_cutoff)
            self.highpass_filter = RCHighPass(self.fs, self.highpass_cutoff)
            self.update_connections(self.lowpass_filter, self.highpass_filter, self.highpass_filter)