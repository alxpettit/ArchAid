#!/usr/bin/env python3

# Copyleft alxandria pettiti blahblahbfuc gplv33 dont care

from pathlib import Path
from sys import argv
import sh

sh.mkdir('-p', 'data')

args = argv[1:]

if not args:
    print('Usage: insert_data.py [config file in which to insert the data]')
    exit(1)


target_file = Path(args[0])


# mmm yes take my ram daddy fill me up
file_contents = target_file.open('r').read()

changes_made = False

for data_file_path in Path('data/').glob('*'):
    var_name = data_file_path.stem
    var_data = data_file_path.open().read()
    if var_name in file_contents:
        file_contents = file_contents.replace(f'[[{var_name}]]', var_data)
        changes_made = True


# lol good luck
if changes_made:
    target_file.rename(target_file.with_suffix('.bak'))
    open(target_file, 'w').write(file_contents)