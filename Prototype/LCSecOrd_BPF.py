from pywdf.core.circuit import Circuit
from LC_BPF import RCBandPass

class SecondOrderBandPass(Circuit):
    def __init__(self, sample_rate: int, central_freq: float) -> None: #Initializes the filter circuit.
      self.fs = sample_rate
      self.central_freq = central_freq
  
      self.bpf1 = RCBandPass(sample_rate, central_freq)
      self.bpf2 = RCBandPass(sample_rate, central_freq)
      
    def process_sample(self, sample: float) -> float: #Processes a single sample through the bandpass filter.
      output1 = self.bpf1.process_sample(sample)
      output = self.bpf2.process_sample(output1)
      return output

