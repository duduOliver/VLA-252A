import pywdf
import numpy as np
from pywdf.core.circuit import Circuit
from pywdf.core.wdf import Resistor
from pywdf.core.wdf import Capacitor
from pywdf.core.wdf import SeriesAdaptor
from pywdf.core.wdf import Inductor
from pywdf.core.rtype import RTypeAdaptor
from pywdf.core.wdf import ParallelAdaptor
from pywdf.core.wdf import IdealVoltageSource
from utils import new_plot_freqz
from scipy.io import wavfile
import matplotlib.pyplot as plt

file_path = "/Users/sofiavallejo/Desktop/Langevin251A/sounds/input/piano.wav"
output_filepath = "/Users/sofiavallejo/Desktop/Langevin251A/sounds/output/piano.wav"

class HiLoBoost(Circuit):
    def __init__(self, sample_rate) -> None:
        self.fs = sample_rate
        
        self.I1 = 75
        self.Ca1 = 8.8e-8
        self.H = 7005.0
        self.F = 2450.0
        self.Re5 = 560.0
        self.Re6 = 560.0
        self.J = 2200.0
        self.Ca2 = 8.7e-8 
        self.G = 1507.0
        self.Ca3 = 5.758e-5
        self.S = 139.0

        #Port B
        self.L5 = Inductor(2.763e-1, self.fs)

        self.L1 = Inductor(3.2e-2, self.fs)
        self.C1 = Capacitor(self.Ca1, self.fs)
        self.R1 = Resistor(self.H)
        self.S1 = SeriesAdaptor(self.L1, self.C1)
        self.S2 = SeriesAdaptor(self.S1, self.R1)

        self.R2 = Resistor(self.F)
        self.L3 = Inductor(1.3, self.fs)
        self.P1 = ParallelAdaptor(self.R2, self.L3)
        
        self.P2 = ParallelAdaptor(self.S2, self.P1)

        self.B = SeriesAdaptor(self.L5, self.P2)

        #Port C
        self.C = Resistor(self.Re5)

        #Port D
        self.D = Resistor(self.Re6)

        #Port E
        self.C2 = Capacitor(self.Ca2, self.fs)
        self.L2 = Inductor(2.81e-2 , self.fs)
        self.R3 = Resistor(self.J)
        self.P3 = ParallelAdaptor(self.C2, self.L2)
        self.P4 = ParallelAdaptor(self.P3, self.R3)
        
        self.R7 = Resistor(self.S)

        self.S4 = SeriesAdaptor(self.P4, self.R7)

        self.R4 = Resistor(self.G)
        self.C3 = Capacitor(self.Ca3, self.fs)
        self.P5 = ParallelAdaptor(self.R4, self.C3)

        self.E = SeriesAdaptor(self.S4, self.P5)

        self.R_Type = RTypeAdaptor([self.B, self.C, self.D, self.E], self.impedance_calc, 0)

        #Join everything

        self.Vin = IdealVoltageSource(self.R_Type)

        super().__init__(self.Vin, self.Vin, None)

    def impedance_calc(self, R: RTypeAdaptor):
        Rb, Rc, Rd, Re = R.get_port_impedances()
        R.set_S_matrix([[0,-Rc/(Rb+Rc+Rd),-(Rb+Rd)/(Rb+Rc+Rd),Rc/(Rb+Rc+Rd),-1],
        [-Rb*Rc/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re),-(Rb*Rb*Rc-Rc*Rc*Rd-Rc*Rd*Rd+(Rb*Rb-Rc*Rc-2*Rc*Rd-Rd*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),(Rb*Rb*Rc+Rb*Rc*Rd+2*(Rb*Rb+Rb*Rc+Rb*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),(2*Rb*Rb*Rc+Rb*Rc*Rc+2*Rb*Rc*Rd+2*(Rb*Rb+Rb*Rc+Rb*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),-Rb*Rc/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re)],
        [-(Rb*Rc+Rc*Rd)/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re),(Rb*Rc*Rc+Rc*Rc*Rd+2*(Rb*Rc+Rc*Rc+Rc*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),-(Rb*Rc*Rc+Rc*Rc*Rd-(Rb*Rb-Rc*Rc+2*Rb*Rd+Rd*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),-(Rb*Rc*Rc+Rc*Rc*Rd+2*(Rb*Rc+Rc*Rc+Rc*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),-(Rb*Rc+Rc*Rd)/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re)],
        [Rc*Rd/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re),(2*Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+2*((Rb+Rc)*Rd+Rd*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),-(Rb*Rc*Rd+Rc*Rd*Rd+2*((Rb+Rc)*Rd+Rd*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),(Rb*Rb*Rc+Rb*Rc*Rc-Rc*Rd*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc-Rd*Rd)*Re)/(Rb*Rb*Rc+Rb*Rc*Rc+Rc*Rd*Rd+(2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd)*Re),Rc*Rd/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re)],
        [-(Rb+Rc+Rd)*Re/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re),-Rc*Re/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re),-(Rb+Rd)*Re/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re),Rc*Re/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re),(Rb*Rc+Rc*Rd)/(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re)]]);
        Ra=(Rb*Rc+Rc*Rd+(Rb+Rc+Rd)*Re)/(Rb+Rc+Rd)
        return Ra
    
    def process_sample(self, sample):
        self.Vin.set_voltage(sample)
        self.R_Type.accept_incident_wave(self.Vin.propagate_reflected_wave())
        self.Vin.accept_incident_wave(self.R_Type.propagate_reflected_wave())
        return  - self.E.wave_to_voltage() + self.D.wave_to_voltage()
    
l251 = HiLoBoost(44_100)
new_plot_freqz(l251)