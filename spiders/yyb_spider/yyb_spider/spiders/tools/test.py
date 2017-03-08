# -*- coding: utf-8 -*-

import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


f = open('./items.json', 'r')
data = f.read()
decode_json = json.loads(data)
for i in decode_json:
    print("%s, %s,"%(i['appname'], i['type'])),
    for j in i['tags']:
        print("%s,"%j),
    print("\n"),


