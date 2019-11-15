#!/usr/bin/env python
# coding: utf-8

# In[45]:


import numpy as np
import pandas as pd
import json_to_df as jd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier


# In[22]:


def inverse_dict(dic):
    new_dic = {}
    for i in dic:
        for j in dic[i]:
            new_dic[j] = i
    return new_dic


# In[87]:


aspects_dict = {"class":["class", "training", "session", "course", "section", "lesson"], 
                "time":["time"],
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
                "spa":["spa", "Spa"],
                "minute":["minute"],
                "massage":["massage"],
                "contract":["contract"],
                "shower":["shower"],
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
                "treadmill":["treadmill"],
                "morning":["morning"],
                "sauna":["sauna"],
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
                "bathroom":["bathroom"],
                "stuff":["stuff"],
                "bike":["bike"],
                "wall":["wall"],
                "team":["team"],
                "amenity":["amenity"],
                "dirty":["dirty"],
                "lift":["lift"],
                "ball":["basketball", "ball"],
                "rack":["rack"],
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
                "elliptical":["elliptical"],
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
                "mess":["mess"]
                }


# In[88]:


aspect_mapping = inverse_dict(aspects_dict)


# In[126]:


model_data = jd.json_to_df_exhaust("../raw_data/model_data.json")
model_data = model_data[["review_id", "text"]]
model_data_ = model_data[["review_id", "stars"]]
model_data


# In[91]:


oh_df = pd.concat([model_data, pd.DataFrame(columns=aspect_mapping.keys())])
for i in range(len(oh_df)):
    for j in oh_df.loc[i, "text"]:
        oh_df.loc[i,aspect_mapping[j]] = oh_df.loc[i, "text"][j]
oh_df.drop(columns = "text", inplace = True)


# In[97]:


oh_df.to_json("../raw_data/oh_df.json",orient="records", lines=True)


# In[112]:


non_text = jd.json_to_df_exhaust("../raw_data/model_nontext.json")


# In[137]:


data = oh_df.merge(non_text, on="review_id").merge(model_data_, on="review_id")
stars = data.stars.values
data.drop(columns = ["review_id","stars"], inplace = True)
data.fillna(0, inplace=True)
features = data.values


# In[155]:


rf = RandomForestClassifier(n_estimators=1000,criterion="gini", max_depth=10,min_samples_split=5,min_samples_leaf=1,
min_weight_fraction_leaf=0.0, max_features=15, max_leaf_nodes=None, min_impurity_decrease=0.0,
min_impurity_split=None, bootstrap=True, oob_score=True, n_jobs=-1, random_state=None,
verbose=True, warm_start=False, class_weight=None)


# In[156]:


rf = rf.fit(features, stars)


# In[157]:


print(sorted(rf.feature_importances_, reverse = True))


# In[158]:


rf.oob_score_


# In[ ]:




