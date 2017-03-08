# -*- coding: utf-8 -*-

import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


tag = {}
type = {}
f = open('./yyb_app_tags.dat', 'r')
for line in open('./yyb_app_tags.dat'):
    line = f.readline()
    arr = line.split(", ")[:-1]
    print arr
    print "%s"%(arr[0].decode('UTF-8'))
    tag[arr[0].decode('UTF-8')].append(arr[2:])
    type[u"%s"%arr[0]].append(arr[1])

for k in type.keys:
    print k, set(type[k]), set(tag[k])

