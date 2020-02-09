#!/usr/bin/env python3
import os
import sys
import argparse
import re
import textwrap
from stat import *
from datetime import date


# contants
VER = 'keepy V0.01\n'\
      'Only keep the last x days/months/years\' specific files '\
      'automatically.'


def keepy(path, yes, filereg, timeType, distance, today):
    delist = []
    for f in os.listdir(path):
        # skip dir and search failed
        if not re.search(filereg, f): continue
        pathname = os.path.join(path, f)
        if S_ISDIR(os.stat(pathname).st_mode): continue
        # get mtime and compare with now
        f_mtime = date.fromtimestamp(os.path.getmtime(pathname))
        if timeType == 'day':
            if (today - f_mtime).days > distance:
                delist.append(pathname)
        if timeType == 'month':
            if ((today.year-f_mtime.year)*12 
                  + (today.month - f_mtime.month)) > distance:
                delist.append(pathname)
        if timeType == 'year':
            if (today.year - f_mtime.year) > distance:
                delist.append(pathname)
    else:
        if len(delist) == 0:
            print('No file need to be delete. Keep them all.')
            return
        # delete process
        delist.sort()
        print('Files ('+str(len(delist))+') to delete:')
        for item in delist: print(item)
        if yes:
            print('Are you sure to delete (Yes/...)?Yes (automatically)')
            for item in delist: os.remove(item)
            print('Delete Complete!')
        else:
            confirm = input('Are you sure to delete (Yes/...)?')
            if re.match('Yes$', confirm.strip()):
                for item in delist: os.remove(item)
                print('Delete Complete!')
            else:
                print('Delete Aborted!')


def pInt(string):
    try:
        num = int(string)
        if num < 0:
            raise argparse.ArgumentTypeError(
                        'Here must be a positive integer.')
    except argparse.ArgumentTypeError:
        raise
    except Exception as e:
        raise argparse.ArgumentTypeError(repr(e))
    else:
        return num


def main():
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = VER + textwrap.dedent('''\n
        Keep those you need, remove the rest by computing the date of today
        and the mtime of files hitted by pattern.
        
        Usage Examples:

        1), keep the last 10 days
            $ python3 keepy.py -a /path -f pattern --day 10
            The files whose name is hitted by the pattern will be checked. 
            Only those whose mtime is within 10 days time from today's date
            will be kept, the others will be deleted after your confirmation.
            --day 0 means delete all except today's file.

        2), keep the last 10 months
            $ python3 keepy.py -a /path -f pattern --month 10
            --month 0 means delete all except file of current month

        3), keep the last 2 years
            $ python3 keepy.py -a /path -f pattern --year 2
            --year 0 means delete all except file of current yesr

        4), say Yes automatically
            $ python3 keepy.py -a /path -f pattern -y --month 3
            -y option can say Yes automatically while delete confirmation.
        '''),
        epilog = 'Keepy project page: '
                 'https://github.com/xinlin-z/keepy\n'
                 'Author\'s python note blog: '
                 'https://www.pynote.net'
    )
    parser.add_argument('-a', '--abspath', required=True,  
            help='absolute path, support ~ expansion')
    parser.add_argument('-y', '--yes', action='store_true',
            help='say Yes automatically while delete confirmation')
    parser.add_argument('-f', '--filereg', required=True, 
            help='file name re expression called by re.search '
                 'to group candidate files')
    timeType = parser.add_mutually_exclusive_group(required=True)
    timeType.add_argument('--day', type=pInt, 
            help='keep the last x days files')
    timeType.add_argument('--month', type=pInt, 
            help='keep the last x months files')
    timeType.add_argument('--year', type=pInt, 
            help='keep the last x years files')
    args = parser.parse_args()
    if (not os.path.isabs(args.abspath) 
          or not os.path.exists(args.abspath)
          or not S_ISDIR(os.stat(args.abspath).st_mode)):
        print('Path must be absolute and existed, and not be a file.')
        sys.exit(1)
    if args.day is not None: 
        _timeType = 'day'; distance = args.day
    if args.month is not None: 
        _timeType = 'month'; distance = args.month
    if args.year is not None: 
        _timeType = 'year'; distance = args.year
    keepy(args.abspath, args.yes, args.filereg,
          _timeType, distance, date.today())


if __name__ == '__main__':
    main()


