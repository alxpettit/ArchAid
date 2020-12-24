#!/usr/bin/env python3

# Copyright (C) Alexandria Pettit 2020 GNU GPLv3 blah blah blah fuck off
# Look, I was annoyed by the complexity of this process so I automated it in the most lazy way I could.

import sh
from hashlib import sha256
from sys import argv

sh.mkdir('-p', 'data')

args = argv[1:]

if not args:
    print('Usage: btrfs_swap_file_calculator.py [path to swap file on BTRFS partition]')
    exit(1)

# Some kernel nerd's source code.
url = 'https://raw.githubusercontent.com/osandov/osandov-linux/master/scripts/btrfs_map_physical.c'

c_code_path = '/tmp/btrfs_map_physical.c'


def get_btrfs_byte_offset():
    sh.gcc(c_code_path, '-o', '/tmp/btrfs_map_physical')
    btrfs_map_physical = sh.Command('/tmp/btrfs_map_physical')
    output = btrfs_map_physical(argv[1])
    line_2 = output.split('\n')[1]
    print(f'Extracted line 2 of output: "{line_2}"')
    byte_offset = int(line_2.split()[-1])
    print(f'Extracted byte offset: {byte_offset}')
    return byte_offset

def get_bytes_per_page():
    bytes_per_page = int(sh.getconf('PAGESIZE'))
    print(f'Got bytes per page: {bytes_per_page}')
    return bytes_per_page

def dl_c_code():
    sh.wget(url, '-c', '-O', c_code_path)
    sum = sha256(open(c_code_path, 'rb').read()).hexdigest()
    if sum != '9f55c0c4f020e194c0fa2716f40ac3bc8e8a92c085cd634684e014b36f3b02b7':
        print('Sum doesn\'t match! Cowardly refusing to compile.')
        exit(1)


def main():
    dl_c_code()
    byte_offset = get_btrfs_byte_offset()
    bytes_per_page = get_bytes_per_page()
    if byte_offset % bytes_per_page != 0:
        print('WARNING! Values are not properly divisible. Something may have gone wrong, just FYI.')
    page_offset = int(byte_offset/bytes_per_page)
    print(f'Calculated BTRFS page offset: {page_offset}')
    open('data/BTRFS_SWAP_FILE_OFFSET', 'w').write(str(page_offset))


main()
