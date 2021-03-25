from urllib2 import urlopen
import pyaudio
import pymedia.audio.acodec as acodec
import pymedia.muxer as muxer
dm= muxer.Demuxer( 'mp3' )


pyaud = pyaudio.PyAudio()

srate=44100

stream = pyaud.open(format = pyaud.get_format_from_width(2),
                    channels = 1,
                    rate = srate,
                    output = True)


url = "http://www.bensound.org/bensound-music/bensound-dubstep.mp3"

u = urlopen(url)

data = u.read(8192)

while data:

    #Start Decode using pymedia
    dec= None
    s= " "
    sinal=[]
    while len( s ):
        s= data
        if len( s ):
            frames= dm.parse( s )
            for fr in frames:
                if dec== None:
                    # Open decoder
                    dec= acodec.Decoder( dm.streams[ 0 ] )
                r= dec.decode( fr[ 1 ] )
                if r and r.data:
                    din = r.data;
            s=""
    #decode ended

    stream.write(din)
    data = u.read(8192)