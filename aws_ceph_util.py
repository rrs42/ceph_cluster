#!/usr/bin/env python3

import json
import os
import subprocess
import argparse


def get_ansible_inventory():
    output = subprocess.check_output(['ansible-inventory', '--list', 'ceph'])

    s = output.decode("utf-8")
    return json.loads(str(s))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--space', action='store_true',
                       help="use space separator")
    group.add_argument('-c', '--comma', action='store_true',
                       help="use comma separator")
    group.add_argument('-o', '--one-match',
                       action='store_true', help="only print first match from each group")
    parser.add_argument('-d', '--long', action='store_true',
                        help="print long hostname (host.domain)")
    parser.add_argument('groups', nargs="+",
                        help="include these groups")

    args = parser.parse_args()

    inv = get_ansible_inventory()

    for g in args.groups:
        hosts = sorted(inv[g]["hosts"])

        if not args.long:
            hosts = [h.split('.')[0] for h in hosts]

        sep = '\n'
        if args.space:
            sep = " "
        elif args.comma:
            sep = ","

        if args.one_match:
            result = hosts[0]
        else:
            result = sep.join(hosts)

        print(result)
