import json_to_df as jd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
import numpy as np
import pandas as pd


## load data
data1.to_json("../Data/cleaned_data.json",orient="records", lines=True)

## fill missing value with 0 and generate data to fit model
data1.fillna(0, inplace=True)
stars1 = data1.stars.values
data1_ = data1.drop(columns = ["review_id","stars"])
features1 = data1_.drop(columns=["Monday_open", "Monday_close","Tuesday_open", "Tuesday_close","Wednesday_open", 
                                "Wednesday_close", "Thursday_open", "Thursday_close","Friday_open", "Friday_close",
                                "Saturday_open", "Sunday_open", "Saturday_close", "Sunday_close", "weekday_close",
                                 "weekday_open", "weekend_close", "weekend_open"]).values

## Initialize a random forest model
rf = RandomForestClassifier(n_estimators=100,criterion="gini", max_depth=100,min_samples_split=5,min_samples_leaf=2,
min_weight_fraction_leaf=0.0, max_features="sqrt", max_leaf_nodes=None, min_impurity_decrease=0,
min_impurity_split=None, bootstrap=True, oob_score=True, n_jobs=-1, random_state=None,
verbose=True, warm_start=False, class_weight=None)

## Fit model
rf1 = rf.fit(features1, stars1)

## Generate a dataframe with features and correspondingly feature importance for plotting
features_ls = data1_.drop(columns=["Monday_open", "Monday_close","Tuesday_open", "Tuesday_close","Wednesday_open", 
                                "Wednesday_close", "Thursday_open", "Thursday_close","Friday_open", "Friday_close",
                                "Saturday_open", "Sunday_open", "Saturday_close", "Sunday_close","weekday_close",
                                 "weekday_open", "weekend_close", "weekend_open"]).columns
features_val = rf1.feature_importances_
features_df = pd.DataFrame({"features":list(features_ls), "importance":list(features_val)})

## Sort the feature importance
features_df.sort_values(by=['importance'], ascending = False, inplace = True)

## Draw pictures
fig, ax = plt.subplots(figsize=(8,6), dpi= 80)
ax.hlines(y=range(20,0,-1), xmin=0, xmax=0.14, color='gray', alpha=0.7, linewidth=1, linestyles='dashdot')
ax.scatter(y=range(20,0,-1), x=features_df.importance[0:20], s=75, color='firebrick', alpha=0.7)

# Title, Label, Ticks and Ylim
ax.set_title('The most important 20 features', fontdict={'size':18})
ax.set_xlabel('Feature importance')
ax.set_yticks(range(20,0,-1))
ax.set_yticklabels(features_df.features[0:20], fontdict={'horizontalalignment': 'right'})
ax.set_xlim(0, 0.14)

## Save the picture
plt.savefig("../Image/feature_importance.png", dpi = 80)

#plt.show()


# Reload data in case of some data changes
data1 = jd.json_to_df_exhaust("../Data/cleaned_data.json")


def plot_feature(feature, coef=False):
    #################################################################################################################################
    ## Descrption: Draw histogram for non-time features
    ## Input:  (a) feature, a string indicates which feature is going to explore the distribution.
    ##         (b) coef, a bool. True indicates generating a correlation matrix for features' value and ratings, False by default.
    ##
    ## Output: (a) a histogram plot
    ##         (b) a correlation matrix will be printed if coef is True.
    ##         (c) the combination of counts, bins and patch will be return as a tuple.                                            
    #################################################################################################################################

    (counts, bins, patch) = plt.hist([data1[data1[feature] > 0].stars, data1[data1[feature] < 0].stars], rwidth = 0.6,
             bins=5, histtype="barstacked",edgecolor="black", alpha=0.7, label=["positive", "negative"])
    plt.legend()
    plt.show()
    if coef:
        print(np.corrcoef([1,2,3,4,5], counts[0]/counts[1]))
    return (counts, bins, patch)


def hist_time(feature, rating=None, span=None, coef=False):
    #################################################################################################################################
    ## Descrption: Draw histogram for time span and ratings
    ## Input:  (a) feature, a string indicates which feature is going to explore the distribution.
    ##         (b) rating, an integer number from 1 to 5, indicates drawing plots about time span distribution over a specific rating
    ##         (c) span, a list with only two elements, indicates the interval of time span. A histogram about the distribution of  
    ##             ratings of the gyms whose time span is in this interval will be generated.
    ##         (d) coef, a bool. True indicates generating a correlation matrix for features' value and ratings, False by default.
    ##
    ## Output: (a) a histogram plot
    ##         (b) a correlation matrix will be printed if coef is True.                                          
    #################################################################################################################################

    if rating:
        plt.hist(advice[advice["stars"]==rating][feature], rwidth = 0.6,
                 bins=24, histtype="bar",edgecolor="black", alpha=0.7)
    else:
        (counts, bins, patch) = plt.hist(advice[(advice[feature]<=span[1]) & (advice[feature]>=span[0])].stars, 
                                         rwidth = 0.6, bins=5, histtype="bar",edgecolor="black", alpha=0.7)
    plt.show()
    if coef:
        print(np.corrcoef([1,2,3,4,5], counts))