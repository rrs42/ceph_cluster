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
    parser.add_argument('-s', '--space', action='store_true')
    parser.add_argument('-n', '--newline', action='store_true')
    parser.add_argument('-o', '--one-match', action='store_true')

    args, groups = parser.parse_known_args()

    inv = get_ansible_inventory()

    for g in groups:
        hosts = sorted(inv[g]["hosts"])

        if args.one_match:
            result = hosts[0]
        elif args.space:
            result = " ".join(hosts)
        elif args.newline:
            result = "\n".join(hosts)
        else:
            result = ",".join(hosts)

        print(result)
