// Load the audio file and SynthDef to test
(
Task({

	~filePath = Platform.userExtensionDir ++ "/Langevin252A/somiomio.wav";
	~fileBuf = Buffer.read(s, ~filePath);
	~fileBuf.loadToFloatArray(action: {|x| f = x});
	~sampleDur = f.size/s.sampleRate;

	// MAIN SYNTH

	SynthDef(\LanTest, { |out, gate = 1, amp = 0.1, band1db = 0.0, band2db = 0.0, band3db = 0.0, band4db = 0.0, band5db = 0.0, band6db = 0.0, band7db =  0.0, buf, rate = 1, startSec = 0, loop = 1.0, choose = 0|
		var sig, envForRelease, envForAttack, freqArray;

		// INPUT SIGNAL
		freqArray = [50.0, 130.0, 320.0, 800.0, 2000.0, 5000.0, 12500.0]; // Central fr. of each BPF
		sig = Select.ar(choose, [WhiteNoise.ar(mul: 0.1), SinOsc.ar(freqArray).sum / freqArray.size * 0.1, PlayBuf.ar(numChannels: 1, bufnum: ~fileBuf, rate: BufRateScale.kr(~fileBuf), loop: loop, startPos: startSec, doneAction: 0, trigger: 1.0)]);

		// OUTPUT SIGNAL
		sig = Langevin252A.ar(sig, band1db, band2db, band3db, band4db, band5db, band6db, band7db);

		// ENVELOPE
		envForAttack = EnvGen.kr(Env.new([0.0, 1.0, 1.0], [0.01, 2**8]), gate, doneAction: Done.freeSelf);
		envForRelease = EnvGen.kr(Env.cutoff(1), gate, doneAction: Done.freeSelf);


		Out.ar(out, sig * amp * envForAttack * envForRelease);
	}).add;


}).play;
)


// Playback
~test = Synth(\LanTest, [buf: ~fileBuf])

// +8 db every bands
~test.set(\band1db, 8.0, \band2db, 8.0, \band3db, 8.0, \band4db, 8.0, \band5db, 8.0, \band6db, 8.0, \band7db, 8.0)

// Doesn't change anything since it is bounded + 8.0 db
~test.set(\band1db, 30.0, \band2db, 30.0, \band3db, 30.0, \band4db, 30.0, \band5db, 30.0, \band6db, 30.0, \band7db, 30.0)


// -8 db every bands
~test.set(\band1db, -8.0, \band2db, -8.0, \band3db, -8.0, \band4db, -8.0, \band5db, -8.0, \band6db, -8.0, \band7db, -8.0)

// Doesn't change anything since it is bounded -8.0 db
~test.set(\band1db, -5000.0, \band2db, -50.0, \band3db, -50.0, \band4db, -50.0, \band5db, -50.0, \band6db, -50.0, \band7db, -50.0)


~test.release

//////////////////////////////////////////////////////


// The mouse movement in the horizontal axes will control the gain changes for all the bands
// Here you can observe that by linear movement of the mouse corresponds to a non-linear mapping. The gain controls behave in 1 db steps with 0.5db of error


(
SynthDef(\LanTestSines, { |out, gate = 1, amp = 0.01, band1db = 0.0, band2db = 0.0, band3db = 0.0, band4db = 0.0, band5db = 0.0, band6db = 0.0, band7db =  0.0|
	var sig, envForRelease, envForAttack, control, freqArray;


	// INPUT SIGNAL
	freqArray = [50.0, 130.0, 320.0, 800.0, 2000.0, 5000.0, 12500.0];
	sig = SinOsc.ar(freqArray).sum / freqArray.size * 0.1;
	// CONTROL SIGNAL
	control = MouseX.kr(-8.0, 8.0).poll;

	// OUTPUT SIGNAL
	sig = Langevin252A.ar(sig, control, control, control, control, control, control, control);

	envForAttack = EnvGen.kr(Env.new([0.0, 1.0, 1.0], [0.01, 2**8]), gate, doneAction: Done.freeSelf);
	envForRelease = EnvGen.kr(Env.cutoff(1), gate, doneAction: Done.freeSelf);

	Out.ar(out, sig * amp * envForAttack * envForRelease);
}).add;
);


~testSines = Synth(\LanTestSines, [\amp, 0.01])
~testSines.release


///////////////////////////////////////////////////

// GUI VERSION
// "choose" botton changes the sound source

(
VarGui(
    synthCtr: [
		\band1db, [-8, 8.0, \lin, 0.00001, 0.0],
        \band2db, [-8.0, 8.0, \lin, 0.000001, 0.0],
        \band3db, [-8.0, 8.0, \lin, 0.000001, 0.0],
		\band4db, [-8.0, 8.0, \lin, 0.00000001, 0.0],
		\band5db, [-8.0, 8.0, \lin, 0.000001, 0.0],
		\band6db, [-8.0, 8.0, \lin, 0.0000001, 0.0],
		\band7db, [-8.0, 8.0, \lin, 0.00000001, 0.0],
		\choose, [0.0, 2.0, \lin, 1.0, -1.0],
	],
    synth: \LanTest
).gui;
)

