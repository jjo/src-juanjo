#!/usr/bin/env python3
'''Just a logspam-er'''

import logging
import sys
import string
import argparse
from random import choice

MAX=int(10E9)
# with STR_LEN=45 we get 100bytes per line
STR_LEN=45

def parse_args():
    parser = argparse.ArgumentParser('logspam')
    parser.add_argument('max', type=int, nargs='?', default=MAX)
    parser.add_argument('--str-len', type=int, default=STR_LEN)
    parser.add_argument('--one-off', type=bool, default=False,
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    return args

args = parse_args()
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

while True:
    for i in range(args.max):
        logging.info('seq={:09d} '.format(i) +
                    ''.join([choice(string.ascii_letters) for i in
                            range(args.str_len)]))
    if args.one_off:
        break
