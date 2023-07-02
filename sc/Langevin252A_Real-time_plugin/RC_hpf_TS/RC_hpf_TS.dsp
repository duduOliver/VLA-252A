
import("stdfaust.lib");
RC_hpf(in) = wd.buildtree(connection_tree)
with{
    vs1(i) = wd.u_voltage(i, in);
    rz(i) = wd.resistor_Vout(i, 1000);
    r1(i) = wd.resistor(i, 1000);
    c1(i) = wd.capacitor(i, 1.0 / (2 * ma.PI * 1000 * cutoff)); 
    connection_tree = vs1 : wd.parallel : ((wd.series : (rz, c1)), r1);
    cutoff = hslider("cutoff", 1000, 1, 24000, 1);
};

process = RC_hpf;
