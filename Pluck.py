from math import sin,pi
from matplotlib import pyplot as PLT
import wave
from struct import pack
from random import random
import PostEffects
def list_to_wave(l,name="temp.wav",width=4):
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

Samplerate=44100

def ar(a,r):
    def inner(x):
        if x>a+r or x<=0:
            return 0
        elif x<a:
            return x/a
        else:
            return 1-(x-a)/r
    return inner

def harmonic_ar(a=lambda n:.03,r= lambda n:1.97/(n)**.5): ##attack release
    return lambda n: ar(a(n),r(n))

def random_enharmonics(amount,minfreq=1,maxfreq=16):
    return [minfreq+random()*(maxfreq-minfreq) for i in range(amount)]
bellpattern=[]
enharm_profile_1=lambda length:[(enh,ar(.006,.3+1/enh),(1/32)/enh**.5) for enh in random_enharmonics(32,maxfreq=8)]+[(enh,ar(.2,.3+3/enh),(.6/20)/enh**.5) for enh in random_enharmonics(20)]
enharm_profile_2=lambda length:[(enh,ar(.2,.3+3/(1+(enh/3)**2)),(1/20)/enh**.5) for enh in random_enharmonics(32,minfreq=.94,maxfreq=8)]
enharm_profile_3=lambda length:[(enh,ar(.006,.3+1/enh),(1/32)/enh**.6) for enh in random_enharmonics(32,maxfreq=16)]+[(enh,ar(.1,.3+3/enh),(1/20)/enh**.8) for enh in random_enharmonics(20,maxfreq=16)]


class bell:
    def __init__(self,harmonic_envs=lambda length:[(n,ar(.01,(length/n**.3)-.01),1/(n**1.6)) for n in range(1,16)],
                 enharmonics=enharm_profile_3,
                 quasiharmonics=[],subharmonics=[]):
        self.harmonics=harmonic_envs
        self.enharmonics=enharmonics
        self.quasiharmonics=quasiharmonics
        self.subharmonics=subharmonics
    def wave(self,freq=220,force=1,length=1):
        harmonic_envs=self.harmonics(length)
        enharmonic_envs=self.enharmonics(length)
        out=[]
        highest=-1
        lowest=1
        for i in range(int(length*44100)):
            pos=i/44100
            #Base sound
            #val=0
            val=(sin(pos*pi*freq)**5*harmonic_envs[0][1](pos)+sin(pos*2*pi*freq)**3*harmonic_envs[0][1](pos)**2)
            #Harmonics
            for hrm in harmonic_envs:
                multiplier,env,vol=hrm
                overtone=sin(multiplier*pos*freq*pi)**5*env(pos)*vol
                val+=overtone

            #Enharmonics
            for enh in enharmonic_envs:
                multiplier,env,vol=enh
                overtone=sin(multiplier*pos*freq*pi)*env(pos)*vol
                val+=overtone

            #Quasiharmonics

            #Subharmonics
                
            if val<lowest:
                lowest=val
            if val>highest:
                highest=val
            out.append(val)
        mg=max(abs(lowest),highest)
        print(len(out))
        return [i/mg for i in out]
belltest=bell().wave()
PLT.plot(belltest)
list_to_wave(belltest,name="New_Bell.wav")
PLT.show()
class pluck:
    def __init__(self,basewave=lambda x,r=0:sin(x)**3*r + sin(x)*(1-r),volumeratio=.5,envfunc=harmonic_ar(),harmonics=16,voicesperharmonic=8,detuning=2,phaseshifts=lambda n:n,expt=2,post_proc=[]):
        self.basewave=basewave
        self.envfunc=envfunc
        self.envs=[envfunc for i in range(1,harmonics)]
        self.harmonics=harmonics
        self.phaseshifts=phaseshifts
        self.voicesperharmonic=voicesperharmonic
        self.volumeratio=volumeratio
        self.magnitude=(1+sum([voicesperharmonic/harmonic**1.2 for harmonic in range(1,harmonics)]))
        self.expt=expt
        self.postprocessing=post_proc
    def pluck(self,length,root=220,velocity=1):#velocity not used yet
        self.frequencies=[[root*harmonic for voice in range(self.voicesperharmonic)] for harmonic in range(1,self.harmonics)]
        self.angles=[[self.phaseshifts(harmonic) for voice in range(self.voicesperharmonic)] for harmonic in range(1,self.harmonics)]
        self.angle=0
        out=[]
        pos=0
        while pos< length*Samplerate:
            self.angle+=root/Samplerate*pi
            val=0
            for harmonic in range(1,self.harmonics):
                #move the angle of each voice of each harmonic accounting for each voice's detune
                for voice in range(self.voicesperharmonic):
                    self.angles[harmonic-1][voice]+=harmonic*root/Samplerate*pi
                    #val+=sin(harmonic*root*pos/Samplerate*pi)*self.envfunc(harmonic)(pos/Samplerate)/harmonic**self.expt
                    val+=(sin(self.angles[harmonic-1][voice])*self.envfunc(harmonic)(pos/Samplerate)/harmonic**self.expt)*(1-self.volumeratio)
                    rootwave=self.basewave(self.angle,pos/(length*Samplerate))*self.envfunc(1)(pos/Samplerate)
            out.append(val/self.magnitude*(1-self.volumeratio)+rootwave*self.volumeratio)
            pos+=1
            
        return out
    def pluck_and_mute(self,length,mutetime):
        pass
    

#test 1
"""
out=[]
test_ar=harmonic_ar()

for n in range(1,16):
    PLT.plot([test_ar(n)(i/Samplerate) for i in range(Samplerate*2)])
for n in range(1,16):
    PLT.plot([test_ar(n)(i/Samplerate) for i in range(Samplerate*2)])
PLT.show()
"""

#test2
"""
import wave

#testpluck=pluck()
#test2=testpluck.pluck(2)
#PLT.plot(test2)
#PLT.show()

testpluck2=pluck(envfunc=harmonic_ar(lambda n:.07,lambda n:.1+1.8/n**.8),expt=1.3)
test3=testpluck2.pluck(2)


#list_to_wave(test2,name="pluck1.wav")
#list_to_wave(test3,name="pluck2.wav")
test4=PostEffects.soundbox(test3,wet=.7,dry=.6)

#PLT.plot(test3)
PLT.plot(test4)
PLT.show()
list_to_wave(test4,name="reverbtest3.wav")"""

