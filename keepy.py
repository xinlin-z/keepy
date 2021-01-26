#!/usr/bin/env python3
import os
import argparse
import re
import shutil
import textwrap
from stat import *
from datetime import date
import subprocess


# contants
_VER = 'keepy V0.05\n'\
       "Automatically delete files or folders, only keep(y) what you need!"


def shell(cmd, cwd=None):
    """Run a shell cmd, return stdout+stderr, or raise, no need 2>&1."""
    proc = subprocess.run(cmd, shell=True, cwd=cwd,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise ChildProcessError(proc.stdout.decode())
    return proc.stdout.decode()


def du_size(pathname, unit='b'):
    """Return size of pathname in unit format by using du command.

    pathname can be a file or folder (os.path.getsize cannot be used here),
    unit can be 'b|B' (default), 'k|K', 'm|M' or 'g|G'.
    return int if unit is b, else return float.
    """
    bnum = int(shell('du -bs %s | cut -f 1'%pathname))
    if unit in ('b','B'): return bnum  # int
    elif unit in ('k','K'): return bnum/1024
    elif unit in ('m','M'): return bnum/1024**2
    elif unit in ('g','G'): return bnum/1024**3
    else: raise ValueError('unit parameter error')


def keepy(path, yes, refile, refolder, mType, distance, today):
    delist = []
    typeStr = 'files' if refile else 'folders'
    for f in os.listdir(path):
        if refile:
            # skip folders and pattern failure
            pathname = os.path.join(path, f)
            if S_ISDIR(os.stat(pathname).st_mode):
                continue
            if not re.search(refile, f):
                continue
        else:  # refolder
            # skip files and pattern failure
            pathname = os.path.join(path, f)
            if not S_ISDIR(os.stat(pathname).st_mode):
                continue
            if not re.search(refolder, f):
                continue
        # get mtime and compare with now
        f_mtime = date.fromtimestamp(os.path.getmtime(pathname))
        if mType == 'day':
            if (today - f_mtime).days > distance:
                delist.append(pathname)
        elif mType == 'month':
            if ((today.year-f_mtime.year)*12 +
                    (today.month - f_mtime.month)) > distance:
                delist.append(pathname)
        elif mType == 'year':
            if (today.year - f_mtime.year) > distance:
                delist.append(pathname)
        else:  # last N or sizelimit
            delist.append(pathname)
    else:
        # last N
        if mType == 'last':
            if distance != 0:
                if len(delist) <= distance:
                    delist = []
                else:
                    delist.sort(key=lambda x:os.path.getmtime(x))
                    delist = delist[:len(delist)-distance]
            # if N == 0, keep all stuff in delist.
        # sizelimit
        elif mType == 'sizelimit':
            delist.sort(key=lambda x:os.path.getmtime(x))
            while distance>0 and len(delist)>0:
                size = du_size(delist[-1])
                if distance >= size:
                    delist.pop()
                distance -= size
            # if sizelimit == 0, keep all stuff to delete.
        # delete process
        if len(delist) == 0:
            print('Nothing needs to be deleted. Keep them all.')
            return
        # sorted by name
        delist.sort()
        print('['+str(len(delist))+ '] %s in the delete list:' % typeStr)
        for item in delist:
            print(os.path.abspath(item))
        if yes:
            print('Are you sure to delete all %s (Yes/...)?Yes' % typeStr)
            for item in delist:
                if refile:
                    os.remove(item)
                else:
                    shutil.rmtree(item)
            print('Delete Complete Automatically!')
        else:
            confirm = input('Are you sure to delete all %s (Yes/...)?'%typeStr)
            if re.match('Yes$', confirm.strip()):
                for item in delist:
                    if refile:
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
                print('Delete Complete!')
            else:
                print('Delete Aborted!')


def pInt(string):
    try:
        num = int(string)
        if num < 0:
            raise argparse.ArgumentTypeError(
                  'here must be a positive integer.')
    except argparse.ArgumentTypeError:
        raise
    except Exception as e:
        raise argparse.ArgumentTypeError(repr(e))
    else:
        return num


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=_VER + textwrap.dedent('''\n

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

        5), keep the last 6 files/folders
            $ python3 keepy.py -p path --refile pattern --last 6
            $ python3 keepy.py -p path --refolder pattern --last 6
            --last 0 means delete all matches.

        '''),
        epilog='keepy project page: '
               'https://github.com/xinlin-z/keepy\n'
               'author\'s python note blog: '
               'https://www.pynote.net'
    )
    parser.add_argument('-V', action='version', version=_VER)
    parser.add_argument('-p', '--path', required=True,
                        help='specify the working path')
    parser.add_argument('-y', '--yes', action='store_true',
                        help='say Yes automatically while delete process')

    fType = parser.add_mutually_exclusive_group(required=True)
    fType.add_argument('--refile', metavar='RE',
                       help='regular expression for files')
    fType.add_argument('--refolder', metavar='RE',
                       help='regular expression for folders')

    mType = parser.add_mutually_exclusive_group(required=True)
    mType.add_argument('--day', type=pInt,
                       help='only keep the stuff of last x days')
    mType.add_argument('--month', type=pInt,
                       help='only keep the stuff of last x months')
    mType.add_argument('--year', type=pInt,
                       help='only keep the stuff of last x years')
    mType.add_argument('--last', type=pInt, metavar='N',
                       help='only keep the last N stuff')
    mType.add_argument('--sizelimit', type=pInt, metavar='BYTES',
                       help='size limit in bytes')

    args = parser.parse_args()
    if (not os.path.exists(args.path) or
            not S_ISDIR(os.stat(args.path).st_mode)):
        raise ValueError('Path must be existed, and should not be a file.')
    if args.day is not None:
        _mType = 'day'
        distance = args.day
    if args.month is not None:
        _mType = 'month'
        distance = args.month
    if args.year is not None:
        _mType = 'year'
        distance = args.year
    if args.last is not None:
        _mType = 'last'
        distance = args.last
    if args.sizelimit is not None:
        _mType = 'sizelimit'
        distance = args.sizelimit

    keepy(args.path, args.yes, args.refile, args.refolder,
          _mType, distance, date.today())


if __name__ == '__main__':
    main()


