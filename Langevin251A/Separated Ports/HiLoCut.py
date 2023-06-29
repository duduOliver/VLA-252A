import pywdf
from pywdf.core.circuit import Circuit
from pywdf.core.wdf import Resistor
from pywdf.core.wdf import Capacitor
from pywdf.core.wdf import SeriesAdaptor
from pywdf.core.wdf import Inductor
from pywdf.core.rtype import RTypeAdaptor
from pywdf.core.wdf import ParallelAdaptor
from pywdf.core.wdf import IdealVoltageSource
from utils import new_plot_freqz

file_path = "/Users/sofiavallejo/Desktop/Langevin251A/sounds/input/piano.wav"
output_filepath = "/Users/sofiavallejo/Desktop/Langevin251A/sounds/output/piano.wav"

class HiLoCut(Circuit):
    def __init__(self, sample_rate) -> None:
        self.fs = sample_rate
        # L1 = #Need a value. 32mhy, 20.8mhy, 10.1mhy, 6.1mhy
        L2 = 5.7e-3 #Need a value 28.1 mhy, 18.6 mhy, 9.1 mhy, 5.7mhy.
        # L3 = #Need a value 1.3mhy, 525mhy
        L4 = 2.88e-2
        L5 = 2.763e-1
        R1 = 390
        R2 = 390
        R3 = 240
        R4 = 560
        R5 = 560
        RJ = 2092
        RG = 1507
        RS = 149
        RH = 7070
        RF = 2450
        RK = 2070
        RP = 21610
        C1 = 0.087 #Needs a value 0.017, 0.025, 0.055, 0.087
        # C2 = #Needs a value 0.088, .056, 0.026, 0.017
        C3 = 0.087
        C6 = .830

        # self.L1 = Inductor(L1, self.fs)
        # self.L2 = Inductor(L2, self.fs)
        # self.L3 = Inductor(L3, self.fs)
        self.L4 = Inductor(L4, self.fs)
        self.L5 = Inductor(L5, self.fs)

        self.R1 = Resistor(R1)
        self.R2 = Resistor(R2)
        self.R3 = Resistor(R3)
        self.R4 = Resistor(R4)
        self.R5 = Resistor(R5)
        self.RJ = Resistor(RJ)
        self.RG = Resistor(RG)
        self.RS = Resistor(RS)
        self.RH = Resistor(RH)
        self.RF = Resistor(RF)
        self.RK = Resistor(RK)
        self.RP = Resistor(RP)

        self.C1 = Capacitor(C1, self.fs)
        # self.C2 = Capacitor(C2, self.fs)
        self.C3 = Capacitor(C3, self.fs)
        self.C6 = Capacitor(C6, self.fs)
        
        # self.LoBoost = LoBoost
        # self.LoCut = LoCut
        # self.HiBoost = HiBoost
        # self.HiCut = HiCut
        # self.LoFreq = LoFreq
        # self.HiFreq = HiFreq

        # self.set_LoBoost(self.LoBoost)
        # self.set_LoCut(self.LoCut)
        # self.set_HiBoost(self.HiBoost)
        # self.set_HiCut(self.HiCut)
        # self.set_LoFreq(self.LoFreq)
        # self.set_HiFreq(self.HiFreq)

        #HiLoCut Port B
        self.B = Resistor(R4)

        #HiLoCut Port C
        self.C = Resistor(R5)

        #HiLoBoost Port D
        self.D = Inductor(L2, self.fs)

        #HiLoBoost Port E
        self.E = SeriesAdaptor(self.C1, self.RJ)

        #HiLoCut Port F
        self.P1 = ParallelAdaptor(self.C6, self.RS)
        self.F = ParallelAdaptor(self.L4, self.P1)
        
        self.R_Type = RTypeAdaptor([self.B, self.C, self.D, self.E, self.F], self.impedance_calc, 0)
        
        #Port A
        self.Vin = IdealVoltageSource(self.R_Type)

        super().__init__(self.Vin, self.Vin, None)        

    def impedance_calc(self, R: RTypeAdaptor):
        Rb, Rc, Rd, Re, Rf = R.get_port_impedances()
        R.set_S_matrix([[0,-Rd/(Rb+Rc+Rd+Re),-Rd/(Rb+Rc+Rd+Re),-(Rb+Rc+Re)/(Rb+Rc+Rd+Re),Rd/(Rb+Rc+Rd+Re),-1],
        [-Rb*Rd/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),(Rc*Rd*Rd+Rd*Re*Re-(Rb*Rb-Rc*Rc)*Rd+(2*Rc*Rd+Rd*Rd)*Re-(Rb*Rb-Rc*Rc-2*Rc*Rd-Rd*Rd-2*(Rc+Rd)*Re-Re*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),-(Rb*Rd*Rd+2*Rb*Rd*Re+2*(Rb*Rb+Rb*Rc)*Rd+2*(Rb*Rb+Rb*Rc+Rb*Rd+Rb*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),(Rb*Rd*Re+(Rb*Rb+Rb*Rc)*Rd+2*(Rb*Rb+Rb*Rc+Rb*Rd+Rb*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),(Rb*Rd*Rd+2*Rb*Rd*Re+2*(Rb*Rb+Rb*Rc)*Rd+2*(Rb*Rb+Rb*Rc+Rb*Rd+Rb*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),-Rb*Rd/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf)],
        [-Rc*Rd/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),-(Rc*Rd*Rd+2*Rc*Rd*Re+2*(Rb*Rc+Rc*Rc)*Rd+2*(Rb*Rc+Rc*Rc+Rc*Rd+Rc*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),(Rb*Rd*Rd+Rd*Re*Re+(Rb*Rb-Rc*Rc)*Rd+(2*Rb*Rd+Rd*Rd)*Re+(Rb*Rb-Rc*Rc+2*Rb*Rd+Rd*Rd+2*(Rb+Rd)*Re+Re*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),(Rc*Rd*Re+(Rb*Rc+Rc*Rc)*Rd+2*(Rb*Rc+Rc*Rc+Rc*Rd+Rc*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),(Rc*Rd*Rd+2*Rc*Rd*Re+2*(Rb*Rc+Rc*Rc)*Rd+2*(Rb*Rc+Rc*Rc+Rc*Rd+Rc*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),-Rc*Rd/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf)],
        [-((Rb+Rc)*Rd+Rd*Re)/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),((Rb+Rc)*Rd*Rd+Rd*Rd*Re+2*((Rb+Rc)*Rd+Rd*Rd+Rd*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),((Rb+Rc)*Rd*Rd+Rd*Rd*Re+2*((Rb+Rc)*Rd+Rd*Rd+Rd*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),-((Rb+Rc)*Rd*Rd+Rd*Rd*Re-(Rb*Rb+2*Rb*Rc+Rc*Rc-Rd*Rd+2*(Rb+Rc)*Re+Re*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),-((Rb+Rc)*Rd*Rd+Rd*Rd*Re+2*((Rb+Rc)*Rd+Rd*Rd+Rd*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),-((Rb+Rc)*Rd+Rd*Re)/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf)],
        [Rd*Re/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),(2*Rd*Re*Re+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+2*((Rb+Rc+Rd)*Re+Re*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),(2*Rd*Re*Re+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+2*((Rb+Rc+Rd)*Re+Re*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),-((Rb+Rc)*Rd*Re+Rd*Re*Re+2*((Rb+Rc+Rd)*Re+Re*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),((Rb+Rc)*Rd*Rd-Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd-Re*Re)*Rf)/((Rb+Rc)*Rd*Rd+Rd*Re*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc)*Rd+(2*(Rb+Rc)*Rd+Rd*Rd)*Re+(Rb*Rb+2*Rb*Rc+Rc*Rc+2*(Rb+Rc)*Rd+Rd*Rd+2*(Rb+Rc+Rd)*Re+Re*Re)*Rf),Rd*Re/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf)],
        [-(Rb+Rc+Rd+Re)*Rf/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),-Rd*Rf/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),-Rd*Rf/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),-(Rb+Rc+Re)*Rf/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),Rd*Rf/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf),((Rb+Rc)*Rd+Rd*Re)/((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf)]]);

        Ra=((Rb+Rc)*Rd+Rd*Re+(Rb+Rc+Rd+Re)*Rf)/(Rb+Rc+Rd+Re)
        return Ra
    
    def process_sample(self, sample):
        self.Vin.set_voltage(sample)
        self.R_Type.accept_incident_wave(self.Vin.propagate_reflected_wave())
        self.Vin.accept_incident_wave(self.R_Type.propagate_reflected_wave())
        return  - self.F.wave_to_voltage() + self.E.wave_to_voltage()
    
l251 = HiLoCut(44_100)
new_plot_freqz(l251)