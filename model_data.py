# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

f = open('raw_text.json')
f1 = open('process_nontext.json')
f2 = open('model_data.json', 'w')
while True:
    line = f.readline()
    line1 = f1.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    new_dic1 = dict(json.loads(line1))
    pd = new_dic['text']
    new_dic1['text'] = pd
    json.dump(new_dic1, f2)
    f2.write("\n")
f.close()
f1.close()
f2.close()

f = open('model_data.json')
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    print(new_dic)
f.close()
