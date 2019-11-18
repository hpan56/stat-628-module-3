# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# add weight to each review sample data
# merge review data for the same business
import json


features = ["staff", "price", "distance", "clean", "equipment", "service", "membership",  "class", "time",
"parking", "room", "crowd",  "trainer",  "pool", "card", "floor", "sign", "open",
"massage", "locker", "contact", "day", "counter", "contract", "atmosphere", "cardio",
"kid", "management", "drink", "woman", "hot", "issue", "space","treadmill", "month", "wait",
"AC","environment", "yoga", "music", "24/7", "week", "year", "refund", "ball", "stuff", "bar","bathroom"]  # 48

non = ["weekend_close", "weekday_close", "weekday_open", "weekend_open",
       "ByAppointmentOnly", "BikeParking", "BusinessAcceptsCreditCards","GoodForKids","BusinessParking","DogsAllowed"]

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
    for j in non:
        try:
            new_dic1[j] = new_dic[j]
        except:
            new_dic1[j] = None
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
            if i in features:
                try:
                    weight_record[bus_id][i] = weight_record[bus_id][i] + new_dic[i]
                except:
                    pass
            if i in non:
                weight_record[bus_id][i] = weight_record[bus_id][i]
f.close()

stars = {}
f = open('process_nontext.json')
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    stars[new_dic['business_id']] = new_dic['stars']
f.close()


f1 = open('weighted_merge.json', 'w')
for i in weight_record:
    weight_record[i]['business_id'] = i
    weight_record[i]['stars'] = stars[i]
    weight_record[i].pop('review_id')
    json.dump(weight_record[i], f1)
    f1.write("\n")
f1.close()

