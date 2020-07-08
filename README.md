# keepy

If your server has many files/folders which are generated regularly, such as
daily, weekly or monthly etc, and you only want to keep some of them which are
in a specified time window towards now. Then keepy is the tool you need to
check, which can delete files/foders automatically and keep what you need!

You specify a path, a name pattern and a time window. Keepy searches all the
files/folders in the path by the name pattern, only those which are in the
time window would be keeped!

Pay attention, keepy use **file/folder mtime** to make decision!

**中文参考 https://www.pynote.net/archives/1797**

# How to Use

You can find a lot usage examples and explanation in help info.

    $ python3 keepy.py -h

# Quick Examples

## only keep the last 90 days log file

    $ python3 keepy.py -p path --refile ^www.access.log_ --day 90

-- day 0 means only keep today's.

## only keep the last 10 months db file

    $ python3 keepy.py -p path --refile pynote.db.gzip$ --month 10

--month 0 means only keep current month's.

## only keep this year's file

    $ python3 keepy.py -p path --refile file_name_pattern --year 0

--year 0 means only keep files of this year.

## do with folders

    $ python3 keepy.py -p path --refolder folder_name_pattern --day N

## say Yes automatically

    $ python3 keepy.py -p path -f pattern --day 0

--day 0 means only keep today's files.

# Version

* **2020-03-07 V0.02**
    - change -a to -p, which can take a relevant path argument

* **2020-02-09 V0.01**
    - fist release


