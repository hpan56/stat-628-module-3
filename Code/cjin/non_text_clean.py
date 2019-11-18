# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

a = ["review_id","is_open","ByAppointmentOnly","GoodForKids","BusinessAcceptsCreditCards", "BikeParking",
 "AcceptsInsurance", "WheelchairAccessible", "DogsAllowed","BusinessAcceptsBitcoin","HasTV",
 "OutdoorSeating", "BusinessParking", "GoodForMeal","Music","HairSpecializesIn", "WiFi","Smoking",
 "intimate", "casual","NoiseLevel", "Monday_open", "Monday_close","Tuesday_open", "Tuesday_close",
 "Wednesday_open","Wednesday_close","Thursday_open","Thursday_close","Friday_open", "Friday_close",
 "Saturday_open", "Saturday_close", "Sunday_open","Sunday_close"]
f = open('process_nontext.json')
f1 = open('model_nontext.json', 'w')
while True:  # cleaning non-text data
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    b = {}
    for i in a:
        try:
            b[i] = new_dic[i]
        except:
            pass
    json.dump(b, f1)
    f1.write("\n")
f.close()
f1.close()




