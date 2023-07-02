RCBpf1OrderTS {
	*ar {|in, cutoff|
		var out, sig;
		sig = RCLpfTS.ar(in, cutoff);
		sig = RCHpfTS.ar(sig, cutoff);
		out = sig;


		^out}
}
