import wave
from Pluck import *
###Code to generate the plucks for the Shruti keyboard at github.com/Troy-Osborne/Shruti/
Newpluck=pluck(expt=1.2)
outsound=[]
list_to_wave(Newpluck.pluck(1,root=shruti(0)),"./Shruti Plucks Just Intonation/Sample.wav")###If exporting each sound
for n in range(-22,45):#2 octaves
    freq=shruti(n)
    octave,just=shrutiname(n)
    if octave<0:
        just=just[0],just[1]*2**abs(octave)
    if octave>0:
        just=just[0]*2**abs(octave),just[1]
        
    name="%s_%s.wav"%(just[0],just[1])
    print(name)
    print(freq)
    print("\n\n")
    #sound=Newpluck.pluck(1,root=freq) ##make new sound for each pluck
    outsound+=Newpluck.pluck(1,root=freq) ##Add every pluck to a list and export the lot (bad way to do it for memory, laziest way to finish atm)
    
    #list_to_wave(sound,"./Shruti Plucks Just Intonation/"+name)###If exporting each sound
    list_to_wave(outsound,"toslice.wav")
    
