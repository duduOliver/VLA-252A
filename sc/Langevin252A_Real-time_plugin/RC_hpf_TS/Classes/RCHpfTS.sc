
RCHpfTS : UGen {

    *ar{|in0,cutoff(1000)|
      ^this.multiNew('audio', in0,cutoff)
    }

    *kr{|in0,cutoff(1000)|
      ^this.multiNew('control', in0,cutoff)
    }

    name { ^"RCHpfTS" }

    info { ^"Generated with Faust" }
    

checkInputs {
    if (rate == 'audio', {
      1.do({|i|
        if (inputs.at(i).rate != 'audio', {
          ^(" input at index " + i + "(" + inputs.at(i) +
            ") is not audio rate");
        });
      });
    });
    ^this.checkValidInputs
  }


    
}
