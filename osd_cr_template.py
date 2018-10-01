#!/usr/bin/env python3

import sys

disks = ['/dev/xvdb', '/dev/xvdc', '/dev/xvdd']

host = sys.argv[1]

for disk in disks:
    print(
        "ceph-deploy osd create --data {disk} {host}".format(disk=disk, host=host))
