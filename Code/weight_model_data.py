# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

features = ['weekend_close', 'weekday_close', 'weekday_open', 'staff', 'weekend_open', 'price',
    'distance','service', 'equipment', 'clean', 'membership', 'ByAppointmentOnly', 'WheelchairAccessible',
   'class', 'BusinessParking', 'GoodForKids', 'BusinessAcceptsCreditCards', 'time', 'BikeParking',
    'room', 'is_open', 'parking', 'crowd', 'trainer', 'card', 'floor', 'sign', 'pool', 'contact',
   'open', 'locker', 'day', 'contract', 'management', 'counter', 'woman', 'kid', 'cardio', 'drink',
   'atmosphere', 'hot', 'issue', 'space','month', 'family', 'wait', 'environment', 'spa', 'refund', 'AC']
f = open('data1.json')
f1 = open('business_gym_weight.json')
f2 = open('data_weight.json', 'w')  # generate reviews multiply weights
while True:
    line = f.readline()
    weight1 = f1.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    weight = dict(json.loads(weight1))
    new_dic1 = {}
    if weight['review_id'] != new_dic['review_id']:
        print('error')
    new_dic1['review_id'] = new_dic['review_id']
    for i in features:
        try:
            new_dic1[i] = new_dic[i] * weight['weight']
        except:
            new_dic1[i] = None
    json.dump(new_dic1, f2)
    f2.write("\n")
f.close()
f1.close()
f2.close()

bus = {}
f = open('raw_rbu.json')
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    if new_dic['review_id'] not in bus:
        bus[new_dic['review_id']] = new_dic['business_id']
f.close()

weight_record = {}  # a dictionary to record every business, totally 2018 businesses
f = open('data_weight.json')
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    bus_id = bus[new_dic['review_id']]  # find the business_id
    if bus_id not in weight_record:
        weight_record[bus_id] = new_dic
    else:
        for i in weight_record[bus_id]:
            if i != 'review_id':
                try:
                    weight_record[bus_id][i] = weight_record[bus_id][i] + new_dic[i]
                except:
                    pass
f.close()

f1 = open('weighted_merge.json', 'w')
for i in weight_record:
    weight_record[i]['business_id'] = i
    json.dump(weight_record[i], f1)
    f1.write("\n")
f1.close()

