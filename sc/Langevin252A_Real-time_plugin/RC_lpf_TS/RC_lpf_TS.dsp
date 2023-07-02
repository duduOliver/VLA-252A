

import("stdfaust.lib");
RC_lpf(in) = wd.buildtree(connection_tree)
with{
    vs1(i) = wd.u_voltage(i, in);
    c1(i) = wd.capacitor_Vout(i, 10^-6);
    r1(i) = wd.resistor(i, 1.0 / (2 * ma.PI * 10^-6 * cutoff));
    connection_tree = vs1 : wd.series : (r1, c1);
    cutoff = hslider("cutoff", 1000, 1, 24000, 1);
};

process = RC_lpf;