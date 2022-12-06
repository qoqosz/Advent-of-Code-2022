#!/usr/bin/env python
import argparse
import requests
import sys
from pathlib import Path


URL = "https://adventofcode.com/{year}/day/{day}/input"


def get_cookie():
    try:
        f = Path('session.key').read_text()
        key, val = f.strip().split('=')
        return {key: val}
    except FileNotFoundError:
        print('Missing session.key file')


def filename(day):
    return Path(f'p{int(day):02d}.txt')


def download(day, year=2022):
    cookie = get_cookie()
    url = URL.format(day=day, year=year)
    r = requests.get(url, cookies=cookie)
    filename(day).open('w').write(r.text)


def is_file(day):
    return filename(day).exists()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('day')    
    parser.add_argument('-y', '--year', type=int, default=2022)
    parser.add_argument('-f', '--force', action='store_true')
    args = parser.parse_args()

    if not args.force:
        if is_file(args.day):
            print(f'Input file for day {args.day} already exists.')
            sys.exit(0)

    download(args.day)
    print(f'Input file for day {args.day} downloaded.')
