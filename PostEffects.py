from math import sin,pi
from matplotlib import pyplot as PLT
import wave
from struct import pack
from random import random
Samplerate=44100
Testwave=[sin(x*220*pi/Samplerate)**3*(1-x/22100) for x in range(22100)]

def delay(milliseconds,decrease,wet_dry,vol=.7):
    def inner(sound):
        bufferlength=int(Samplerate/1000*milliseconds)#sampleser
        buffer=sound[0:bufferlength]
        bufferpos=0
        out=[]
        for i in sound:
            currentsound=max(-1,min(1,(buffer[bufferpos]*wet_dry+i*(1-wet_dry))*vol))
            out.append(currentsound)
            buffer[bufferpos]+=i
            buffer[bufferpos]*=decrease
            bufferpos+=1
            if bufferpos==bufferlength:
                bufferpos=0
        termination_threshold=0.02
        
        while 1:
            currentsound=max(-1,min(1,buffer[bufferpos]*wet_dry*vol))
            out.append(currentsound*vol)
            buffer[bufferpos]*=decrease
            bufferpos+=1
            if bufferpos==bufferlength:
                bufferpos=0
                again=False
                for i in buffer:
                    if i >termination_threshold:
                        again=True
                        break
                if again:
                    continue
                else:
                    break
        return out
    return inner

def add_sound(sound1,sound2,start=0):
    out=sound1[0:start]
    n=0
    while 1:
        try:
            out.append(sound1[start+n]+sound2[n])
        except:
            if start+n>=len(sound1):
                out+=sound2[n:]
            else:
                out+=sound1[start+n:]
            break
                
        n+=1
    return out

def reverb_distribution(maxreflections,power,sourcedistance=.3,size=2.5):
    def inner(x):
        reflections=round(maxreflections*x**power)
        distancetraveled=.3+(maxreflections*x**power)*size
        volume=100/(100+distancetraveled)
        return reflections,distancetraveled,volume
    return inner
def soundbox(sound,distrib=reverb_distribution(40,1.6,.2,4),wet=1,dry=0,voices=1000):
    outwet=[0]*len(sound)
    for i in range(voices):
        reflections,distance,volume=distrib(random())
        outwet=add_sound(outwet,[i*volume for i in sound],start=int(distance*.01*44100))
    return add_sound(normalize(outwet,vol=wet),normalize(sound,vol=dry))
        
"""
sound=[sin(x*110*pi/44100)**3 for x in range(4000)]
a=soundbox(sound)
print(len(a))

#PLT.plot([reverb_distribution(x/100) for x in range(100)])
PLT.plot(sound)
PLT.plot(a)
PLT.show()
  """      

def normalize(l,vol=1):
    M=max(l)
    m=min(l)
    return [i/max(M,-m)*vol for i in l]


def list_to_wave(l,name="Deelay.wav",width=4):
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
"""marimba=delay(1,.7,.2)(delay(2,.5,.3)(Testwave))
PLT.plot(marimba)
PLT.show()
list_to_wave(marimba,name="marimba.wav")
"""
