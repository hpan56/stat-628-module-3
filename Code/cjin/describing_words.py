# !/usr/bin/env python3
# -*- coding: utf-8 -*-



import json

a = {}
f = open('raw_rbu_text_record.json')
while True:  # extract describing words for each aspects
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    for i in new_dic['text']:
        if i in a:
            a[i].append(new_dic['text'][i])
        else:
            a[i] = [new_dic['text'][i]]
f.close()
for i in a:
    a[i] = list(set(a[i]))
f2 = open('w.json', 'w')
json.dump(a, f2)
f2.close()
print(a['staff'])
