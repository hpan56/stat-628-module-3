import json
import pandas as pd


def json_to_df_lines(path, lines=100, skip=0):
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

def json_to_df_exhaust(path,skip=0):
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
                    dic[key].append(dic_new[key])
        dic = pd.DataFrame(dic)
        return dic