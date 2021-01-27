# Contents

* [keepy](#keepy)
* [How to Use](#How-to-Use)
* [Quick Examples](#Quick-Examples)
    * [keep the last 90 days log file](#keep-the-last-90-days-log-file)
    * [keep the last 10 months db file](#keep-the-last-10-months-db-file)
    * [keep this year's file](#keep-this-years-file)
    * [keep folders](#keep-folders)
    * [say Yes automatically](#say-Yes-automatically)
    * [keep the last N stuff](#keep-the-last-N-stuff)
    * [set size limit](#set-size-limit)
* [Version](#Version)

# keepy

If your server has many files/folders which are generated regularly, such as
daily, weekly or monthly etc, and you only want to keep some of them which are
in a specified time window towards now, or to set a space size limit. Then
keepy is the tool you need to check, which can delete files/folders
automatically and keep what you need!

You should specify a path, a name pattern and a time window or size limit.
Keepy searches all the files/folders in the path by the name pattern, only
those which are in the time window, or within the size limit (in descent order
of mtime) would be kept!

Pay attention, keepy use **file/folder mtime** to make decision!

**中文参考 https://www.pynote.net/archives/1797**

# How to Use

You can find a lot usage examples and explanation in help info.

    $ python3 keepy.py -h

# Quick Examples

## keep the last 90 days log file

    $ python3 keepy.py -p path --refile ^www.access.log_ --day 90

-- day 0 means only keep today's.

## keep the last 10 months db file

    $ python3 keepy.py -p path --refile pynote.db.gzip$ --month 10

--month 0 means only keep current month's.

## keep this year's file

    $ python3 keepy.py -p path --refile file_name_pattern --year 0

--year 0 means only keep files of this year.

## keep folders

    $ python3 keepy.py -p path --refolder folder_name_pattern --day N
    
--refolder means folder's regular expression. All the other parameters are
the same with --refile.

## say Yes automatically

    $ python3 keepy.py -p path --refile pattern --day 0

## keep the last N stuff

    $ python3 keepy.py -p path --refolder pattern --last N

If N == 0, delete all matches.

## set size limit

    $ python3 keepy.py -p path --refile pattern --sizelimit BYTES

It's very useful to keep a sort of content under a limited max size. If BYTES
== 0, delete all matches.

# Version

* **2021-01-27 V0.05**
    - add --sizelimit option
    - add tox.ini for flake8

* **2020-10-25 V0.04**
    - add --last N parameter which could delete all matches

* **2020-07-09 V0.03**
    - add --refolder option to keep folders
    - change -f to --refile
    - optimize info of -h

* **2020-03-07 V0.02**
    - change -a to -p, which can take a relevant path argument

* **2020-02-09 V0.01**
    - fist release


