Voices
======
281 points, 28 solves

Statement
---------

* [Listen](https://dctf.def.camp/dctf-18-quals-81249812/voices.wav). Can you hear the voices? They are there. Somehow. 

Solution
--------

Turn down your headphones volume before opening the link provided in the challenge statement (well, probably it's already too late). The link turns out to be a 3 minutes long .wav filled with white noise (and spoiler alert - it's not particularly interesting to listen to). 
The first thing I always do when dealing with a sound file in a steganography challenge is to open it in a spectrogram analysis program. For example, you can import file in Audacity and change the display mode from Waveform to Spectrogram:
!(voices1.png)

Hmmmmm, the spectrum of frequencies from 15K to 22K looks suspicious:
!(voices2.png)

After zooming in we can clearly see stripes aligned in four rows:
!(voices3.png)

Clearly these rows must represent our flag somehow. After inspection we can notice that there are exactly two filled rows at every moment. Moreover, exactly one of upper two rows is filled and exactly one of lower two rows is filled. Let's look closer at upper two rows and imagine that the top one being filled will denote 0 and the bottom one being filled will denote 1. Now assign bits to the lower two rows in a same manner:
!(voices4.png)

Wow, assembling first 8 bits into one byte (01000100) gives us a character 'D' in ascii. The next 8 bits (01000011) are a binary representation of 'C'. And next three bytes are 'T', 'F' and '{'. So clearly we are on the right track.
So let the happy funtime begin - 30 minutes of transcribing the "stripes notation" into ascii characters (and additional 30 minutes if you made a mistake somewhere in the middle of the file and your flag doesn't want to be accepted). Well, alternatively you can write a clever script to decode the flag automatically, but this doesn't look like it's easy, so why bother to do so? :)

Flag: DCTF{Oh noes I lost it somewhere on my computer, if you are really curious to see some random hexadecimal jumble then decode the file yourself :P} 
