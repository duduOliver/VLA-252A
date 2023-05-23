import numpy as np
from pywdf.core.circuit import Circuit
from pywdf.core.wdf import Resistor
from pywdf.core.wdf import Capacitor
from pywdf.core.wdf import SeriesAdaptor
from pywdf.core.wdf import ParallelAdaptor
from pywdf.core.wdf import ResistiveVoltageSource

class RCHighPass(Circuit):
    def __init__(self, sample_rate: int, cutoff: float) -> None:

        self.fs = sample_rate
        self.cutoff = 0

        self.C = 0.14e-6
        self.Z = 10000

        self.Rz = Resistor(self.Z)
        self.C1 = Capacitor(self.C, self.fs)
        self.R1 = Resistor(1000)
        self.S2 = SeriesAdaptor(self.Rz, self.C1)
        self.P1 = ParallelAdaptor(self.S2, self.R1)

        self.Vs = ResistiveVoltageSource(75)
        self.S1 = SeriesAdaptor(self.P1, self.Vs)

        super().__init__(self.Vs, self.Vs, self.Rz)
        self.set_cutoff(cutoff)

    def process_sample(self, sample: float) -> float:
        self.Vs.set_voltage(sample)
        self.Vs.accept_incident_wave(self.S1.propagate_reflected_wave())
        self.S1.accept_incident_wave(self.Vs.propagate_reflected_wave())
        return self.Rz.wave_to_voltage()

    def set_cutoff(self, new_cutoff: float):
        if self.cutoff != new_cutoff:
            self.cutoff = new_cutoff
            self.C = 1.0 / (2 * np.pi * self.Z * self.cutoff)
            self.C1.set_capacitance(self.C)