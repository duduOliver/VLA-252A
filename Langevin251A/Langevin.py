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

class Langevin251(Circuit):
    def __init__(self, sample_rate) -> None:
        self.fs = sample_rate

        L1 = 3.2e-2 #Need a value. 3.2e-2 , 2.08e-2 ,  1.01e-2,  6.1e-3.
        L2 = 2.81e-2 #Need a value 2.81e-2, 1.86e-2, 9.1e-3, 5.7e-3. CUT 60 H>, BOOST 900 ish
        L3 = 1.3 #Need a value 1.3, 5.25e-1 
        L4 = 2.88e-2 
        L5 = 2.763e-2
        R1 = 470
        R2 = 470
        R3 = 270
        R4 = 620
        R5 = 620
        RJ = 2700
        RG = 1800
        RS = 150
        RH = 10000
        RF = 39000
        RK = 33000
        RP = 33000
        ROut = 1000
        C1 = 0.015 #Needs a value 0.017, 0.025, 0.055, 0.087
        C2 = 0.0047 #Needs a value 0.088, .056, 0.026, 0.017
        C3 = 0.1
        C6 = 0.82

        self.L1 = Inductor(L1, self.fs)
        self.L2 = Inductor(L2, self.fs)
        self.L3 = Inductor(L3, self.fs)
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
        self.ROut = Resistor(ROut)

        self.C1 = Capacitor(C1, self.fs)
        self.C2 = Capacitor(C2, self.fs)
        self.C3 = Capacitor(C3, self.fs)
        self.C6 = Capacitor(C6, self.fs)

        #Port B
        self.P1 = ParallelAdaptor(self.L1, self.R1)
        self.B = ParallelAdaptor(self.P1, self.L5)

        #Port C
        self.S1 = SeriesAdaptor(self.L1, self.C1)
        self.S2 = SeriesAdaptor(self.S1, self.RH)
        self.P2 = ParallelAdaptor(self.S2, self.RF)
        self.P3 = ParallelAdaptor(self.P2, self.L3)
        self.S3 = SeriesAdaptor(self.C3, self.RF)
        self.C = ParallelAdaptor(self.P3, self.S3)

        #Port D
        self.P4 = ParallelAdaptor(self.C2, self.L2)
        self.P5 = ParallelAdaptor(self.P4, self.RJ)

        self.P6 = ParallelAdaptor(self.RS, self.L4)
        self.P7 = ParallelAdaptor(self.P6, self.C6)

        self.D = SeriesAdaptor(self.P5, self.P7)

        #Port E
        self.E = self.ROut
        
        #Port A
        self.R_Type = RTypeAdaptor([self.B, self.C, self.D, self.E], self.impedance_calc, 0)
        self.Vin = IdealVoltageSource(self.R_Type)
        super().__init__(self.Vin, self.Vin, None)        

    def impedance_calc(self, R: RTypeAdaptor):
        Rb, Rc, Rd, R3 = R.get_port_impedances()
        R.set_S_matrix([[0,-1,-Rd/(R3+Rc+Rd),-(R3+Rc)/(R3+Rc+Rd),-Rd/(R3+Rc+Rd)],
        [-(R3*Rb+Rb*Rc+Rb*Rd)/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),(R3+Rc)*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),-Rb*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),-(R3*Rb+Rb*Rc)/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),-Rb*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd)],
        [-Rc*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),-Rc*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),(R3*R3*Rb-Rb*Rc*Rc+(R3+Rb)*Rd*Rd+(R3*R3+2*R3*Rb-Rc*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd),(2*R3*Rb*Rc+2*Rb*Rc*Rc+((R3+2*Rb)*Rc+Rc*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd),-(2*R3*Rb*Rc+2*Rb*Rc*Rc+Rc*Rd*Rd+2*((R3+Rb)*Rc+Rc*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd)],
        [-(R3+Rc)*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),-(R3+Rc)*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),((R3+2*Rb+Rc)*Rd*Rd+2*(R3*Rb+Rb*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd),(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc-(R3+Rb+Rc)*Rd*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd),((R3+2*Rb+Rc)*Rd*Rd+2*(R3*Rb+Rb*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd)],
        [-R3*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),-R3*Rd/(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd),-(2*R3*R3*Rb+2*R3*Rb*Rc+R3*Rd*Rd+2*(R3*R3+R3*Rb+R3*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd),(2*R3*R3*Rb+2*R3*Rb*Rc+(R3*R3+2*R3*Rb+R3*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd),-(R3*R3*Rb-Rb*Rc*Rc-(Rb+Rc)*Rd*Rd+(R3*R3-2*Rb*Rc-Rc*Rc)*Rd)/(R3*R3*Rb+2*R3*Rb*Rc+Rb*Rc*Rc+(R3+Rb+Rc)*Rd*Rd+(R3*R3+2*R3*Rb+2*(R3+Rb)*Rc+Rc*Rc)*Rd)]]);

        Ra=(R3*Rb+Rb*Rc+(R3+Rb+Rc)*Rd)/(R3+Rc+Rd)
        return Ra
    
    def process_sample(self, sample):
        self.Vin.set_voltage(sample)
        self.R_Type.accept_incident_wave(self.Vin.propagate_reflected_wave())
        self.Vin.accept_incident_wave(self.R_Type.propagate_reflected_wave())
        return  - self.E.wave_to_voltage() + self.D.wave_to_voltage()
    
l251 = Langevin251(44_100)
new_plot_freqz(l251)