#!/usr/bin/env python
# -*- coding: utf-8 -*-

def dhdjhash(name):
    name = name.encode('utf-8')

    r = 0
    for c in name:
        r += c
    return str(r)

if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    passwd = dhdjhash(name)
    print(passwd)
