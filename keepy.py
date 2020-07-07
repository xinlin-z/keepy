#!/usr/bin/env python3
import os
import sys
import argparse
import re
import shutil
import textwrap
from stat import *
from datetime import date


# contants
VER = 'keepy V0.03\n'\
      "Automatically delete files or folders, only keep(y) what you need!"


def keepy(path, yes, refile, refolder, timeType, distance, today):
    delist = []
    _tstr = 'files' if refile else 'folders'
    for f in os.listdir(path):
        if refile:
            # skip folders and search failed
            pathname = os.path.join(path, f)
            if S_ISDIR(os.stat(pathname).st_mode):
                continue
            if not re.search(refile, f):
                continue
        if refolder:
            # skip files and search failed
            pathname = os.path.join(path, f)
            if not S_ISDIR(os.stat(pathname).st_mode):
                continue
            if not re.search(refolder, f):
                continue
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
            print('Nothing needs to be deleted. Keep them all.')
            return
        # delete process
        delist.sort()
        print('['+str(len(delist))+ '] %s in the delete list:' % _tstr)
        for item in delist:
            print(os.path.abspath(item))
        if yes:
            print('Are you sure to delete all %s (Yes/...)?Yes' % _tstr)
            for item in delist:
                if refile: os.remove(item)
                if refolder: shutil.rmtree(item)
            print('Delete Complete Automatically!')
        else:
            confirm = input('Are you sure to delete all %s (Yes/...)?'%_tstr)
            if re.match('Yes$', confirm.strip()):
                for item in delist:
                    if refile: os.remove(item)
                    if refolder: shutil.rmtree(item)
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

        Usage Examples:

        1), keep the last 10 days' files/folders
            $ python3 keepy.py -p path --refile pattern --day 10
            $ python3 keepy.py -p path --refolder pattern --day 10
            The files/folders whose name is hitted by the pattern will be
            checked. Only those whose mtime is within 10 days time from
            today's date will be kept, the others will be deleted after
            your confirmation.
            --day 0 means delete all except today's.

        2), keep the last 10 months' files/folders
            $ python3 keepy.py -p path -refile pattern --month 10
            $ python3 keepy.py -p path -refolder pattern --month 10
            --month 0 means delete all except those of current month

        3), keep the last 2 years' files/folders
            $ python3 keepy.py -p path --refile pattern --year 2
            $ python3 keepy.py -p path --refolder pattern --year 2
            --year 0 means delete all except those of current yesr

        4), say Yes automatically
            $ python3 keepy.py -p path -y --refile pattern --month 3
            $ python3 keepy.py -p path -yes --refolder pattern --month 3
            -y or --yes option can say Yes automatically for you, be careful.
        '''),
        epilog = 'keepy project page: '
                 'https://github.com/xinlin-z/keepy\n'
                 'author\'s python note blog: '
                 'https://www.pynote.net'
    )
    parser.add_argument('-p', '--path', required=True,
            help='specify the working path')
    parser.add_argument('-y', '--yes', action='store_true',
            help='say Yes automatically while delete process')

    fType = parser.add_mutually_exclusive_group(required=True)
    fType.add_argument('--refile', metavar='RE',
                    help='regular expression for files')
    fType.add_argument('--refolder', metavar='RE',
                    help='regular expression for folders')

    timeType = parser.add_mutually_exclusive_group(required=True)
    timeType.add_argument('--day', type=pInt,
            help='keep the stuff of last x days')
    timeType.add_argument('--month', type=pInt,
            help='keep the stuff of last x months')
    timeType.add_argument('--year', type=pInt,
            help='keep the stuff of last x years')

    args = parser.parse_args()
    if (not os.path.exists(args.path)
          or not S_ISDIR(os.stat(args.path).st_mode)):
        print('Path must be existed, and should not be a file.')
        sys.exit(1)
    if args.day is not None:
        _timeType = 'day'; distance = args.day
    if args.month is not None:
        _timeType = 'month'; distance = args.month
    if args.year is not None:
        _timeType = 'year'; distance = args.year

    keepy(args.path, args.yes, args.refile, args.refolder,
          _timeType, distance, date.today())


if __name__ == '__main__':
    main()


