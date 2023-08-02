import numpy as np
from matplotlib import pyplot as plt
import wave
from struct import pack
SampleRate=44100
def Karplus_Strong(wavetable, n_samples,rate=0.499):
    """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
    samples = [] 
    current_sample = 0
    previous_value = 0
    while len(samples) < n_samples:
        wavetable[current_sample] = rate * (wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)

def Make_Pluck(WaveFunc=None,Freq=110,Length=5,DecayRate=0.01):
    wts=SampleRate//Freq
    #Random Noise
    if WaveFunc==None:
        wt = (2 * np.random.randint(0, 2, wts) - 1).astype(float)
    else:
        theta=np.linspace(0, np.pi*2, wts)
        wt = np.array([WaveFunc(i) for i in theta])
    return Karplus_Strong(wt,Length*SampleRate,0.5-DecayRate/200)
    
def list_to_wave(l,name="KP.wav",width=4):
    wavobj = wave.open(name,'w')
    wavobj.setnchannels(1) # mono
    wavobj.setsampwidth(width)
    wavobj.setframerate(44100)
    magnitude=2**(8*width-1)-1
    code="h" if width==2 else "l" if width ==4 else "b"
    for i in l:
        wavobj.writeframes(pack(code,int(i*magnitude)))
    wavobj.close()
    return 1
from random import random
sin=np.sin
pi=np.pi
weirdwave=lambda x:sin(sin(sin(4*x)*pi/2+2*x)*pi+x)
weirdwave2=lambda x:min(1,max(-1,weirdwave(x)+random()-random()))#weirdwavewith noise
weirdwave3=lambda x:(weirdwave(x+pi)**5+sin(x)**3+weirdwave2(x))/3
sound=Make_Pluck(WaveFunc=weirdwave3,Freq=220,DecayRate=.1)
sound2=Make_Pluck(WaveFunc=weirdwave3,Freq=55,DecayRate=.1)
#plt.plot(sound)
list_to_wave(sound,"_KP1.wav")
list_to_wave(sound2,"_KP2.wav")
#plt.show()
