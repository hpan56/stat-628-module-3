import numpy as np
import pandas as pd
import json_to_df as jd
from sklearn.ensemble import RandomForestClassifier

## Load data
data1 = jd.json_to_df_exhaust("../Data/cleaned_data.json")

## Fill missing value thus model can be fit
data1.fillna(0, inplace=True)
## Generate explanatory variables and response variable for model fitting
stars1 = data1.stars.values
data1_ = data1.drop(columns = ["review_id","stars"])
features1 = data1_.drop(columns=["Monday_open", "Monday_close","Tuesday_open", "Tuesday_close","Wednesday_open", 
                                "Wednesday_close", "Thursday_open", "Thursday_close","Friday_open", "Friday_close",
                                "Saturday_open", "Sunday_open", "Saturday_close", "Sunday_close", "weekday_close",
                                 "weekday_open", "weekend_close", "weekend_open"]).values


## Initialize random forest model (a result of cross validation and efficiency consideration)
rf = RandomForestClassifier(n_estimators=100,criterion="gini", max_depth=100,min_samples_split=5,min_samples_leaf=2,
min_weight_fraction_leaf=0.0, max_features="sqrt", max_leaf_nodes=None, min_impurity_decrease=0,
min_impurity_split=None, bootstrap=True, oob_score=True, n_jobs=-1, random_state=None,
verbose=True, warm_start=False, class_weight=None)


## Model fitting and correspondingly out of bag score
rf1 = rf.fit(features1, stars1)
rf1.oob_score_


## Generate feature importance sequence and its corresponding features
feature_importance_dict1 = dict(zip(data1_.drop(columns=["Monday_open", "Monday_close","Tuesday_open", "Tuesday_close","Wednesday_open", 
                                "Wednesday_close", "Thursday_open", "Thursday_close","Friday_open", "Friday_close",
                                "Saturday_open", "Sunday_open", "Saturday_close", "Sunday_close", "weekday_close",
                                 "weekday_open", "weekend_close", "weekend_open"]).columns, rf1.feature_importances_))
feature_importance_1 = sorted(feature_importance_dict1.items(), key = lambda x: x[1], reverse = True)
for i in range(100):
    print(i, feature_importance_1[i])

## Another round of model fitting to test if the result is robust
new_features = []
for i in range(102):
    new_features.append(feature_importance_1[i][0])

## Remove two features that don't make sense
new_features.remove("WheelchairAccessible")
new_features.remove("is_open")

## Generate new explanatory variables
new_features_values = data1_[new_features].values

## Another round of model fitting and corresponding out of bag score
rf3 = rf.fit(new_features_values, stars1)
rf3.oob_score_

## Generate the feature importance sequence and corresponding features
feature_importance_dict3 = dict(zip(new_features, rf3.feature_importances_))
for i in range(100):
    print(i, new_features[i], feature_importance_dict3[new_features[i]])