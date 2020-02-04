#!/usr/bin/env python3
import os
import sys
import argparse
import re
from stat import *
from datetime import date


def keepy(path, filereg, timeType, distance, today):
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
            pass
        if timeType == 'year':
            pass
    else:
        print(delist)


def pInt(string):
    try:
        num = int(string)
        if num <= 0:
            raise argparse.ArgumentTypeError(
                        'Here must be a positive integer.')
    except argparse.ArgumentTypeError:
        raise
    except Exception as e:
        raise argparse.ArgumentTypeError(repr(e))
    else:
        return num


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--abspath', required=True,  
            help='absolute path, support ~ expansion')
    #parser.add_argument('-m', '--mtime', required=True, action='store_true',
    #        help='use mtime to determine if delete')
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
    if args.day: _timeType = 'day'; distance = args.day
    if args.month: _timeType = 'month'; distance = args.month
    if args.year: _timeType = 'year'; distance = args.year
    keepy(args.abspath, args.filereg, _timeType, distance, date.today())


if __name__ == '__main__':
    main()


