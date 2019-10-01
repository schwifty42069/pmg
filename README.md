pmg - Piptv M3U Generator
=======

An M3U generator for IPTV services [kodi/plex/etc.] using the same scraping logic as [piptv](https://github.com/schwifty42069/piptv)! *I provide this script and all support for it free of charge, but any donations are welcome and appreciated. They can be sent to this bitcoin address: **bc1qahz93vyljhjj0fsadu2m8zdhaqdaf60gnc7y2y** Thank you and enjoy!*

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

*This script requires geckodriver to be installed. I have included the latest 64 & 32bit geckodriver
binaries for windows in the resource directory in this repo. You can also find them [here.](https://github.com/mozilla/geckodriver/releases) 
Geckodriver must be moved to a location that's within
your path environment variable. To see how your path is currently configured in windows, open a cmd prompt
and type the following:*

```
echo @PATH@
``` 

*Ubuntu/Debian users can use their package manager to install geckodriver. 
For example, in Ubuntu you would type the following in a terminal:*

```
apt install firefox-geckodriver
```

**Usage**

To use the script to generate an M3U, simply run the script and pass the directory 
(including file name) you would like the M3U to be written to with the -o flag. For example

**Windows**

```
python -m piptv_pmg.pmg -o "C:\Users\Example_Person\Example_dir\example.m3u"
```

**Ubuntu/Debian**

```
python3 -m piptv_pmg.pmg -o /home/some_user/some_dir/example.m3u
```

*Documentation for cross platform automation of the script, as well as some processes for use with 
specific IPTV services such a plex and kodi will be added shortly, we are still working on making
them as clear and detailed as possible!*
