import json
import pandas as pd

## This function is designed for a quick overview over dataset
def json_to_df_lines(path, lines=100, skip=0):
    #####################################################################################################################################
    ## Description: read json file in exactly three original json file format, with specific lines, may skip some lines if necessary
    ## Input:       (a) path,  a string indicates where the raw json file is
    ##              (b) lines, an integer indicates how many lines to read, 100 by default
    ##              (c) skip,  an integer indicates how many lines to skip, 0 by default
    ## Output:      a dataframe with all the columns but selected lines by tunning parameter lines and parameter skip
    #####################################################################################################################################
    with open(path, encoding="utf-8") as f:
        dic = {}
        for i in range(1,lines+skip+1):
            line = f.readline()
            if i <= skip:
                continue
            dic_new = dict(json.loads(line))
            if i == skip+1:
                dic = dic_new
                for key in dic:
                    dic[key] = [dic[key]]
            else:
                for key in dic:
                    dic[key].append(dic_new[key])
        f.close()
        dic = pd.DataFrame(dic)
        return dic

## This function is designed for read    
def json_to_df_exhaust(path,skip=0):
    #####################################################################################################################################
    ## Description: read json file in exactly three original json file format may skip some lines if necessary
    ## Input:       (a) path,  a string indicates where the raw json file is
    ##              (b) skip,  an integer indicates how many lines to skip, 0 by default
    ## Output:      a dataframe with all the columns but selected lines by tunning parameter lines and parameter skip
    #####################################################################################################################################
    with open(path, encoding="utf-8") as f:
        dic = {}
        lines = f.readlines()
        f.close()
        i = 0
        for line in lines:
            i += 1
            if i <= skip:
                continue
            dic_new = dict(json.loads(line))
            if i == 1+skip:
                dic = dic_new
                for key in dic:
                    dic[key] = [dic[key]]
            else:
                for key in dic:
                    try:
                        dic[key].append(dic_new[key])
                    except:
                        dic[key].append(None)
        dic = pd.DataFrame(dic)
        return dic