Langevin252A {
	*ar {|in, db1 = 0.0, db2 = 0.0, db3 = 0.0, db4 = 0.0, db5 = 0.0, db6 = 0.0, db7 = 0.0|
		var out, band1, band2, band3, band4, band5, band6, band7, sig, rq = 1.0, thresholddBm, referenceImpedance, thresholdLinear;

		thresholddBm = 24; // 24 as described in the specs
		referenceImpedance = 600; // Convert dBm to linear gain with 600 Ohms reference impedance
		thresholdLinear = 10 ** ((thresholddBm - 0) * 0.05) * sqrt(referenceImpedance / 1);
		sig = if(in > thresholdLinear, in * (1 + (in - thresholdLinear)), in); // Apply distortion when the input signal exceeds the threshold


		db1 = db1.round(1.0) + rand2(0.5);
		db2 = db2.round(1.0) + rand2(0.5);
		db3 = db3.round(1.0) + rand2(0.5);
		db4 = db4.round(1.0) + rand2(0.5);
		db5 = db5.round(1.0) + rand2(0.5);
		db6 = db6.round(1.0) + rand2(0.5);
		db7 = db7.round(1.0) + rand2(0.5);

		db1 = db1.clip(-8.0, 8.0);
		db2 = db2.clip(-8.0, 8.0);
		db3 = db3.clip(-8.0, 8.0);
		db4 = db4.clip(-8.0, 8.0);
		db5 = db5.clip(-8.0, 8.0);
		db6 = db6.clip(-8.0, 8.0);
		db7 = db7.clip(-8.0, 8.0);


		band1 = RCBpf2OrderTS.ar(sig, 50.0) * db1.dbamp;
		band2 = RCBpf2OrderTS.ar(sig, 130.0) * db2.dbamp;
		band3 = RCBpf2OrderTS.ar(sig, 320.0) * db3.dbamp;
		band4 = RCBpf2OrderTS.ar(sig, 800.0) * db4.dbamp;
		band5 = RCBpf2OrderTS.ar(sig, 2000.0) * db5.dbamp;
		band6 = RCBpf2OrderTS.ar(sig, 5000.0) * db6.dbamp;
		band7 = RCBpf2OrderTS.ar(sig, 12500.0) * db7.dbamp;



		sig = band1 + band2 + band3 + band4 + band5 + band6+ band7;
		out = sig;
		^out}
}

