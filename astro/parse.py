#!/usr/bin/env python
"""
Example Usage:
    $ head -n 10 bsc5.dat | python3 parse.py
"""
import sys
import json
import signal


signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def parse_line(line):
    data = {
        'hr': int(line[0:4]),
        'name': line[4:14].strip(),
        'sao_number': int(line[31:37]) if line[31:37].strip() else None,
        'vmag': float(line[102:107]) if line[102:107].strip() else None,
    }
    return data


if __name__ == '__main__':
    data = [parse_line(line) for line in sys.stdin]
    data = sorted(data, key=lambda o: o['vmag'] or 2 ^ 32 - 1)
    for row in data:
        print(json.dumps(row))
