import json
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
 
    
def process_weight(data_path,result_path):
    #list of features usef to compute weight
    tag=['useful','user_review_count','friends','fans','compliment']
    a=[]
    f1=open(result_path,'w')
    for line in tqdm(open(data_path,encoding='utf-8')):
        #load data
        data=dict(json.loads(line))
        #use log to compute weight score and add them all
        l=[]
        for tags in tag:
            l.append(math.log(data[tags]+1)+1)
        l.append(math.log(5009/data['date'])+1)
        weight=1
        for i in l:
            weight=weight+i
        a.append(weight)
        #write weight score to file
        data1={}
        data1['review_id']=data['review_id']
        data1['weight']=weight/47.69282550552211
        f1.write(json.dumps(data1)+'\n')
    print(max(a))
    # ~ sns.set()
    # ~ ax=sns.distplot(a,bins=None,kde=True,norm_hist=False)
    # ~ plt.show()
    

if __name__ == '__main__':
    process_weight('./Data/process_nontext.json','./Data/business_gym_weight.json')
