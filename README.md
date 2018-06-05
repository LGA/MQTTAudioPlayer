# Pure Data Player
Samples are organised in rows (A-E) and columns (1-5) -> 25 slots for samples
The Pure data player takes care of polyphony and sample pannning (left-right, back-front)

Before sending commands via command line `pdsend`, pure data has to be started and the file puredata/pdAudioPlayer.pd has to be opened.

## Loading patches
Single audio file can be loaded with:
`echo "l A 1 ../media/A1.wav" | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp`

Several audio files can be loaded with:
`echo "l A 1 ../media/A1.wav, l A 2 ../media/A2.wav, l A 3 ../media/A3.wav, l A 4 ../media/A4.wav, l A 5 ../media/A5.wav" | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp`

## Playing samples
Samples can be triggered via 
`echo "p A 1" | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp`