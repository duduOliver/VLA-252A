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
import matplotlib.pyplot as plt

file_path = "/Users/sofiavallejo/Desktop/Langevin251A/sounds/input/piano.wav"
output_filepath = "/Users/sofiavallejo/Desktop/Langevin251A/sounds/output/piano.wav"

class HiCutLoBoost(Circuit):
    def __init__(self, sample_rate) -> None:
        self.fs = sample_rate
        
        self.I1 = 75
        RF = 2450
        self.L3 = Inductor(1.3, self.fs)
        self.L5 = Inductor(2.763e-1, self.fs)

        R1 = 560 
        R2 = 560
        RS = 149
        C1 = 0.087

        #Port B
        self.RF = Resistor(RF)
        self.P1 = ParallelAdaptor(self.RF, self.L3)
        self.B = SeriesAdaptor(self.P1, self.L5)

        #Port C
        self.C = Resistor(R1)

        #Port D
        self.D = Resistor(R2)

        #Port E
        self.C1 = Capacitor(C1, self.fs)
        self.RS = Resistor(RS)
        self.E = ParallelAdaptor(self.C1, self.RS)

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
    
l251 = HiCutLoBoost(44_100)
new_plot_freqz(l251)