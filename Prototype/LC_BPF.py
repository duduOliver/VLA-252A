import numpy as np
from scipy.fftpack import fft
from pywdf.core.circuit import Circuit
from RC_hpf import RCHighPass
from RC_lpf import RCLowPass
from utils.octave_distance import octave_distance

def compute_spectrum(self, fft_size: int = None) -> np.ndarray:
    x = self.get_impulse_response()
    N2 = int(fft_size / 2 - 1)
    H = fft(x, fft_size)[:N2]
    return H

class RCBandPass(Circuit):
    def __init__(self, sample_rate: int, central_freq: float) -> None: #Initializes the RCBandPass circuit.
        """
        Args:
            sample_rate (int): The sample rate in Hz.
            central_freq (float): The central frequency in Hz.
        """
        self.fs = sample_rate
        self.central_freq = central_freq
        self.calculate_cutoffs()

    def calculate_cutoffs(self) -> None: #Calculates the lowpass and highpass cutoff frequencies based on the central frequency.
        n_octave = octave_distance(self.central_freq)
        n_octave_over2 = n_octave / 2
        self.lowpass_cutoff = self.central_freq * 2 ** n_octave_over2
        self.highpass_cutoff = self.central_freq / (2 ** n_octave_over2)
        self.lowpass_filter = RCLowPass(self.fs, self.lowpass_cutoff)
        self.highpass_filter = RCHighPass(self.fs, self.highpass_cutoff)
        super().__init__(self.lowpass_filter, self.highpass_filter, self.highpass_filter)

    def process_sample(self, sample: float) -> float: #Processes a single sample through the bandpass filter.
        """
        Args:
            sample (float): The input sample value.
        Returns:
            float: The output sample value after bandpass filtering.
        """
        lowpass_output = self.lowpass_filter.process_sample(sample)
        bandpass_output = self.highpass_filter.process_sample(lowpass_output)
        return bandpass_output
        
    def set_central_freq(self, new_central_freq: float) -> None: #Sets a new central frequency and updates the cutoff frequencies.
        """
        Args:
            new_central_freq (float): The new central frequency in Hz.
        """
        if self.central_freq != new_central_freq:
            self.central_freq = new_central_freq
            self.calculate_cutoffs()
            self.update_connections(self.lowpass_filter, self.highpass_filter, self.highpass_filter)