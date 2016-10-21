# getNaturePodcast
python script to download nature podcasts

## sox
[Sox](http://sox.sourceforge.net/) is required since it is called within the script to process the audio in the podcast. Comment those lines if you do not want to process the audio file.

## python libraries
requests, BeautifulSoup, subprocess, os

## use:
```python
python seekDownloadResampleAmp.py
```

## functionality

The script downloads podcasts from the nature [podcast repository](http://www.nature.com/nature/podcast/archive.html)


The script downloads five<sup name="a1">[1](#f1)</sup> podcasts at the time. The script checks whether the current file has already been downloaded and skips the file download if the file is already present in my mp3player. The script loops through the list of podcasts until it finds 5 podcasts which have not been downloaded already. The 'futures' are not downloaded because I do not like them, but the script download 'backchat' and 'extra'.

Because the sound is very soft in my mp3 player I call sox to: 
1. increase the volume
2. down sample the sound file to 16K (from 44.1 K) this is to save space
3. rename the file with a 'c_' in front

The original file is then deleted.

<b id="f1">1</b> To download more podcasts change the value of the variable podcasts2download	to the desired amount (line 39). [↩](#a1)
