pmg - Piptv M3U Generator
=======

An M3U generator for IPTV services [kodi/plex/etc.] using the same scraping logic as [piptv](https://github.com/schwifty42069/piptv)!

**Installation**

Pgm is available on pypi. To install the script, do the following in a terminal/cmd prompt

**Windows**

```
pip install piptv_pmg
```

**Ubuntu/Debian**

```
python3 -m pip install piptv_pmg
```

**Usage**

To use the script to generate an M3U, simply run the script and pass the directory 
(including file name) you would like the M3U to be written to with the -o flag. For example

**Windows**

```
python -m piptv_pgm.pgm -o C:\Users\Example_Person\Example_dir\example.m3u
```

**Ubuntu/Debian**

```
python3 -m piptv_pgm.pgm -o /home/some_user/some_dir/example.m3u
```

*Documentation for cross platform automation of the script, as well as some processes for use with 
specific IPTV services such a plex and kodi will be added shortly, we are still working on making
them as clear and detailed as possible!*