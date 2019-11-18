# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


f = open('process_nontext.json')
f2 = open('non.json', 'w')
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    new_dic.pop("user_id")
    new_dic.pop("business_id")
    new_dic.pop("stars")
    new_dic.pop("useful")
    new_dic.pop("date")
    new_dic.pop("name")
    new_dic.pop("city")
    new_dic.pop("state")
    new_dic.pop("bus_stars")
    new_dic.pop("bus_review_count")
    new_dic.pop("user_name")
    new_dic.pop("user_review_count")
    new_dic.pop("yelping_since")
    new_dic.pop("user_useful")
    new_dic.pop("friends")
    new_dic.pop("fans")
    new_dic.pop("average_stars")
    new_dic.pop("compliment")
    json.dump(new_dic, f2)
    f2.write("\n")
f.close()
f2.close()

