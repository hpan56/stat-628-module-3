import numpy as np
import pandas as pd
import json_to_df as jd
import copy


## Initialize aspects dictionary for further analysis
as_dict = {"class":["class", "training", "session", "course", "section", "lesson"],
                "time": ["time"],
                "distance":["place", "location", "area", "walk", "home", "drive", "locate"],
                "counter":["counter", "desk"],
                "staff":["staff", "people", "manager", "person", "owner", "employee", "People", "worker", "folk"],
                "month":["month"],
                "room":["room"],
                "day":["day"],
                "equipment":["equipment", "machine", "facility"],
                "membership":["membership", "member", "club"],
                "clean":["clean", "cleanliness"],
                "year":["year"],
                "price":["$","pay", "price", "check", "charge", "fee", "money", "rate", "cost", "payment","bill","pricing","dollar"],
                "sign":["sign"],
                "week":["week"],
                "parking":["lot", "parking", "park"],
                "hour":["hour", "Hour"],
                "service":["service"],
                "trainer":["trainer", "instructor", "coach", "teacher", "Coach"],
                "kid":["kid", "child","daughter", "son", "baby"],
                "cardio":["cardio"],
                "locker":["locker", "lock", "key"],
                "pool":["pool", "swimming"],
                "wait":["wait"],
                "open":["open"],
                "minute":["minute"],
                "massage":["massage" ,"sauna",'spa','Spa'],
                "contract":["contract"],
                "yoga":["yoga"],
                "family":["family"],
                "issue":["issue", "problem"],
                "maintenance":["maintenance"],
                "towel":["towel"],
                "floor":["floor"],
                "train":["train"],
                "woman":["woman", "girl", "lady", "female"],
                "space":["space"],
                "card":["card", "account"],
                "24/7":["24","24/7"],
                "contact":["phone", "email", "online", "website"],
                "schedule":["schedule"],
                "treadmill":["treadmill", "rack","elliptical"],
                "morning":["morning"],
                "hot":["hot"],
                "music":["music"],
                "crowd":["crowd", "crowded"],
                "night":["night"],
                "man":["man","boy"],
                "court":["court"],
                "program":["program"],
                "management":["management"],
                "steam":["steam"],
                "town":["town", "downtown"],
                "atmosphere":["atmosphere", "vibe"],
                "door":["door"],
                "box":["box"],
                "bar":["bar"],
                "tv":["tv"],
                "environment":["environment"],
                "community":["community"],
                "bathroom":["bathroom", "shower"],
                "stuff":["stuff"],
                "bike":["bike"],
                "wall":["wall"],
                "team":["team"],
                "amenity":["amenity"],
                "dirty":["dirty"],
                "lift":["lift"],
                "ball":["basketball", "ball"],
                "hair":["hair"],
                "weekend":["weekend", "Saturday", "Sunday"],
                "smell":["smell"],
                "bench":["bench", "chair"],
                "climb":["climb", "climbing"],
                "track":["track"],
                "refund":["refund"],
                "access":["access"],
                "student":["student", "school"],
                "boxing":["boxing", "kickboxe"],
                "tour":["tour"],
                "office":["office"],
                "food":["food"],
                "bag":["bag"],
                "fan":["fan"],
                "appointment":["appointment"],
                "injury":["injury", "hurt"],
                "evening":["evening"],
                "Zumba":["Zumba"],
                "beginner":["beginner"],
                "mat":["mat"],
                "spacious":["spacious"],
                "tanning":["tanning", "tan"],
                "AC":["air", "condition"],
                "drink":["drink", "juice", "water", "smoothie"],
                "hook":["hook"],
                "childcare":["childcare", "daycare"],
                "instruction":["instruction"],
                "Groupon":["Groupon", "groupon"],
                "dumbbell":["dumbbell"],
                "lounge":["lounge"],
                "discount":["discount"],
                "Monday":["Monday"],
                "dry":["dry"],
                "afternoon":["afternoon"],
                "jacuzzi":["jacuzzi"],
                "monitor":["monitor"],
                "screen":["screen"],
                "movie":["movie"],
                "layout":["layout"],
                "diet":["diet"],
                "Friday":["Friday"],
                "mirror":["mirror"],
                "zone":["zone"],
                "pilate":["pilate"],
                "store":["store"],
                "meal":["meal"],
                "window":["window"],
                "spray":["spray"],
                "restroom":["restroom"],
                "cafe":["cafe"],
                "mess":["mess"]}

## Load data and select the columns
model_data = jd.json_to_df_exhaust("../Data/model_data.json")
model_data_ = model_data[["review_id", "stars"]]
model_data = model_data[["review_id", "text"]]


## An ancillary function to extract the sentiment
def map_aspcet(x,key):
    try:
        return x[key]
    except:
        return 0

## An ancillary function to transfer the text column into new features
def fill_df(df, mapping):
    for key in mapping:
        temp = np.array([0]*len(df.text), dtype="float32")
        count = 0
        for i in mapping[key]:
            temp += np.array(list(map(map_aspcet, list(df.text), [i]*len(df.text)))).astype("float32")
        df[key] = temp
    return df

## Drop former text columns
model_data_copy = copy.deepcopy(model_data)
data_m1 = fill_df(model_data_copy, as_dict)
data_m1.drop(columns="text",inplace=True)

## An ancillary function to change those close time equal to 0 into 24 (makes more sense then) 
def close_time(x):
    if x == 0:
        return 24
    else:
        return x

## Load non_text data and merge then together
non_text = jd.json_to_df_exhaust("../Data/model_nontext.json")
data1 = jd.json_to_df_exhaust("../Data/cleaned_data.json")
data1 = data_m1.merge(non_text, on="review_id").merge(model_data_, on="review_id")


## Convert open time and close time into 4 new features
data1["weekday_open"] = data1[["Monday_open", "Tuesday_open", "Wednesday_open", 
                                 "Thursday_open", "Friday_open"]].apply(np.mean,axis=1)
data1["weekday_close"] = data1[["Monday_close", "Tuesday_close", "Wednesday_close", 
                                 "Thursday_close", "Friday_close"]].apply(np.mean,axis=1)
data1["weekday_close"] = data1.weekday_close.apply(close_time)

data1["weekend_open"] = data1[["Saturday_open", "Sunday_open"]].apply(np.mean,axis=1)
data1["weekend_close"] = data1[["Saturday_close", "Sunday_close"]].apply(np.mean,axis=1)
data1["weekend_close"] = data1.weekend_close.apply(close_time)

data1["weekday_span"] = data1["weekday_close"] - data1["weekday_open"]
data1["weekend_span"] = data1["weekend_close"] - data1["weekend_open"]



## Generate clean data
data1.to_json("../Data/cleaned_data.json",orient="records", lines=True)
data1.to_csv("../Data/cleaned_data.csv")