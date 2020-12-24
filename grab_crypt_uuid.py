#!/usr/bin/env python3

import sh
from sys import argv

sh.mkdir('-p', 'data')

args = argv[1:]

if not args:
    print('Usage: grab_crypt_uuid.py [block device for which to grab the UUID]')
    exit(1)

uuid_info_str = sh.blkid(args[0])
print(f'Info string from blkid: {uuid_info_str}')
uuid_section = uuid_info_str.split()[1]
# Remove 'UUID=""' crap
just_uuid = uuid_section[6:-1]
print(f'UUID grabbed: "{just_uuid}"')
open('data/CRYPT_UUID', 'w').write(just_uuid)