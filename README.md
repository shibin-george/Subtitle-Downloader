Subtitle-Downloader
===================

Python script for downloading subtitles from www.subscene.com
===================

This script requires:
1) BeautifulSoup ( >= 4.0), a python library for parsing html content.

Script tested in Linux environment on Python(2.7.3).

1) Run the file as: python subtitleDownloader.py
2) Enter the name of the movie/video for which the subtitles are to be fetched, for ex: The Conjuring
3) Enter the index from the suggestions provided
4) Enter a language of choice.
5) Enter the name of the file for ex: The.Conjuring.2013.720p.BluRay.x264.YIFY
   Remember not to include the file extension.

The suggestions will be displayed in the order of closeness to the filename you entered.
The script proceeds to downloads the first suggestion.
However, in case the downloaded file doesn't sync( or is terrible), 
explore the other suggestions, preferably in the order displayed.
The links for all subtitles suggested have been provided,
and can be easily downloaded manually or saved for reference.

For finding the closest named subtitle, 
the script uses dynamic programming technique to compute the 'Levenshtein distance' ( or 'Edit distance') between the filenames.
For reference: en.wikipedia.org/wiki/Levenshtein_distance

Author:
Shibin George
B.Tech CSE, 2011-15,
National Institute Of Technology, Warangal.
