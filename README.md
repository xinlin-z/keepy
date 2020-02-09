# Keepy

If your server has many files which are generated regularly, such as daily 
or monthly etc, and you want only to keep some of them which are most close
to current time. Then keepy is the tool you need to check.

Keepy only keep those files you specified by an absolute path, a file name
pattern and a time window. The rest hitted by the file name pattern and in the
same path would be deleted for you automatically.

Pay attention, keepy use **file mtime** to make decision!

中文参考 https://www.pynote.net/archives/1797

# How to Use

You can find a lot usage examples and explanation in help info.

    $ python3 keepy.py -h

# Quick Examples 

## Only keep the last 90 days log file

    $ python3 keepy.py -a /path -f ^www.access.log_ --day 90

## Only keep the last 10 months db file

    $ python3 keepy.py -a /path -f pynote.db.gzip$ --month 10

## Only keep this year's file

    $ python3 keepy.py -a /path -f file_name_pattern --year 0

--year 0 means only keep current year's files.

--month 0 means only keep files of this month.

## say Yes automatically

    $ python3 keepy.py -a /path -f pattern --day 0

--day 0 means only keep today's files.

# Version

* **2020-02-09 V0.01**
    
    - fist release


