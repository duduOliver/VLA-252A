import numpy as np
from pywdf.core.circuit import Circuit
from pywdf.core.wdf import Resistor
from pywdf.core.wdf import Capacitor
from pywdf.core.wdf import SeriesAdaptor
from pywdf.core.wdf import PolarityInverter
from pywdf.core.wdf import IdealVoltageSource

class RCLowPass(Circuit):
    def __init__(self, sample_rate: int, cutoff: float) -> None:

        self.fs = sample_rate
        self.cutoff = cutoff
        self.C = 1e-6 
        self.R = 1.0 / (2 * np.pi * self.C * self.cutoff)

        self.R1 = Resistor(self.R)
        self.C1 = Capacitor(self.C, self.fs)

        self.S1 = SeriesAdaptor(self.R1, self.C1)
        self.I1 = PolarityInverter(self.S1)
        self.Vs = IdealVoltageSource(self.I1)

        super().__init__(self.Vs, self.Vs, self.C1)

    def set_cutoff(self, new_cutoff: float):
        if self.cutoff != new_cutoff:
            self.cutoff = new_cutoff
            self.R = 1.0 / (2 * np.pi * self.C * self.cutoff)
            self.R1.set_resistance(self.R)

