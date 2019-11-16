#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import json_to_df as jd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import matplotlib


# In[2]:


data1 = jd.json_to_df_exhaust("../raw_data/data1.json")


# In[3]:


data1.fillna(0, inplace=True)
stars = data1.stars.values
data1_ = data1.drop(columns = ["review_id","stars"])
features2 = data1_.drop(columns=["Monday_open", "Monday_close","Tuesday_open", "Tuesday_close","Wednesday_open", 
                                "Wednesday_close", "Thursday_open", "Thursday_close","Friday_open", "Friday_close",
                                "Saturday_open", "Sunday_open", "Saturday_close", "Sunday_close"]).values


# In[4]:


rf = RandomForestClassifier(n_estimators=100,criterion="gini", max_depth=100,min_samples_split=5,min_samples_leaf=2,
min_weight_fraction_leaf=0.0, max_features="sqrt", max_leaf_nodes=None, min_impurity_decrease=0,
min_impurity_split=None, bootstrap=True, oob_score=True, n_jobs=-1, random_state=None,
verbose=True, warm_start=False, class_weight=None)


# In[5]:


rf1 = rf.fit(features2, stars)


# In[6]:


rf1.oob_score_


# In[7]:


feature_importance_dict = dict(zip(data1_.drop(columns=["Monday_open", "Monday_close","Tuesday_open", "Tuesday_close","Wednesday_open", 
                                "Wednesday_close", "Thursday_open", "Thursday_close","Friday_open", "Friday_close",
                                "Saturday_open", "Sunday_open", "Saturday_close", "Sunday_close"]).columns, rf1.feature_importances_))


# In[8]:


feature_importance_ = sorted(feature_importance_dict.items(), key = lambda x: x[1], reverse = True)


# In[9]:


for i in range(50):
    print(i,feature_importance_[i])


# In[10]:


# 画图前重新读取包含Missing data的数据, 避免分布中包含缺失值
data1 = jd.json_to_df_exhaust("../raw_data/data1.json")


# In[11]:


## 给non_text 画图用
def plot_non_text(feature):
    (counts, bins, patch) = plt.hist([data1[data1[feature] > 0].stars, data1[data1[feature] <= 0].stars], rwidth = 0.6,
             bins=5, histtype="barstacked",edgecolor="black", alpha=0.7, label=["positive", "negative"])
    plt.legend()
    plt.show()
    return (counts, bins, patch)


# In[12]:


plt0 = plot_non_text("ByAppointmentOnly")


# In[13]:


plt0[0]
#一行表示一个group(如positvie)在1-5分中的count


# In[14]:


## 0表示 “缺失” 时画图用
## 0表示 “缺失” 时画图用
## 0表示 “缺失” 时画图用

##给text features画图用
def plot_text(feature):
    (counts, bins, patch) = plt.hist([data1[data1[feature] > 0].stars, data1[data1[feature] < 0].stars], rwidth = 0.6,
             bins=5, histtype="barstacked",edgecolor="black", alpha=0.7, label=["positive", "negative"])
    plt.legend()
    plt.show()
    return (counts, bins, patch)


# In[15]:


plt1 = plot_text("staff")


# In[16]:


plt1[0]
#一行表示一个group(如positvie)在1-5分中的count


# In[17]:


#开门时间画图
def plot_opentime(feature,time_split):
    (counts, bins, patch) = plt.hist([data1[data1[feature] <= time_split[0]].stars, 
                                      data1[(data1[feature] <= time_split[1])&(data1[feature] > time_split[0])].stars,
                                     data1[(data1[feature] <= time_split[2])&(data1[feature] > time_split[1])].stars, 
                                      data1[data1[feature] > time_split[2]].stars], rwidth = 0.6,
             bins=5, histtype="barstacked",edgecolor="black", alpha=0.7, 
                                     label=["earlier than %i o'clock" %time_split[0], "earlier than %i o'clock" %time_split[1],
                                            "earlier than %i o'clock" %time_split[2], "later than %i o'clock" %time_split[2]])
    plt.legend()
    plt.show()
    return (counts, bins, patch)


# In[18]:


plt2 = plot_opentime("weekday_open",[4,8,10])


# In[19]:


plt2[0]
#一行表示一个group(如earlier then 6am)在1-5分中的count


# In[20]:


#开门时间画图
def plot_closetime(feature,time_split):
    (counts, bins, patch) = plt.hist([data1[data1[feature] <= time_split[0]].stars, 
                                      data1[(data1[feature] <= time_split[1])&(data1[feature] > time_split[0])].stars,
                                     data1[(data1[feature] <= time_split[2])&(data1[feature] > time_split[1])].stars, 
                                      data1[data1[feature] > time_split[2]].stars], rwidth = 0.6,
             bins=5, histtype="barstacked",edgecolor="black", alpha=0.7, 
                                     label=["earlier than %i o'clock" %time_split[0], "earlier than %i o'clock" %time_split[1],
                                            "earlier than %i o'clock" %time_split[2], "later than %i o'clock" %time_split[2]])
    plt.legend()
    plt.show()
    return (counts, bins, patch)


# In[21]:


plt3 = plot_closetime("weekday_close",[14,18,22])


# In[22]:


plt3[0]
#一行表示一个group(如earlier then 6pm)在1-5分中的count

