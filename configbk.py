#!/usr/bin/env python
# encoding: utf-8

import jsonpickle
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
class Item(object):
    def __init__(self, id, src, dst):
        self.id = id
        self.src = src
        self.dst = dst


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-b", "--backup", type=str, default="config.backup", help="Create/update backup")
    parser.add_argument("-u", "--update", type=str, default="config.backup" ,help="Update configs")
    parser.add_argument("-r", "--restore", type=str, default="config.backup" ,help="Restore configs")


args = parser.parse_args()
