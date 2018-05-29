# getNaturePodcast
python script to download nature podcasts

## python libraries
requests, BeautifulSoup, subprocess, os

## use:
```python
# to remove the previously downloaded files
python seekDownloadResampleAmp.py remove

# to keep the previously downloaded files
python seekDownloadResampleAmp.py

```

## functionality

The script downloads podcasts from the nature [podcast repository](https://www.nature.com/nature/articles?type=nature-podcast)


The script downloads five<sup name="a1">[1](#f1)</sup> podcasts at the time. The script checks whether the current file has already been downloaded and skips it if the file is already present in my mp3player. The script loops through the list of podcasts until it finds 5 podcasts which have not been downloaded already. The 'futures' are not downloaded because I do not like them, but the script downloads 'backchat' and 'extra'.

<b id="f1">1</b> To download more podcasts change the value of the variable podcasts2download	to the desired amount (line 39). [↩](#a1)
