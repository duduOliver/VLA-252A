RCBpf2OrderTS {
	*ar {|in, cutoff|
		var out, sig;
		sig = RCBpf1OrderTS.ar(in, cutoff);
		sig = RCBpf1OrderTS.ar(sig, cutoff);
		out = sig;


		^out}
}