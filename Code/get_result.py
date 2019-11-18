import json
import time
from tqdm import tqdm


def extract_recommand(data_path,suggest_path,result_path):
    #read suggestion file
    f1=open(suggest_path,encoding='utf-8')
    suggest=f1.readlines()
    #extract suggestions
    feature=['ByAppointmentOnly','BusinessParking','GoodForKids','BikeParking','distance','DogsAllowed','price', 'staff', 'crowd', 'drink', 'trainer', 'contract', 'membership', 'class', 'card', 'kid', 'clean', 'wait', 'sign', 'parking', 'equipment', 'service', 'room', 'woman', 'music', 'atmosphere', 'yoga', 'open', 'pool', 'bar', 'AC', 'locker', 'management', 'contact', 'ball', 'hot', 'space', 'cardio', 'massage', 'counter', 'refund', '24/7', 'treadmill', 'bathroom', 'floor']
    #construct suggestions for each feature
    fea_dict={}
    for line in suggest:
        if line.split('\t')[0] in feature:
            if line.split('\t')[0]=='distance':
                fea_dict[line.split('\t')[0]]=[line.split('\t')[1].strip('\n'),line.split('\t')[2].strip('\n')]
            else:
                fea_dict[line.split('\t')[0]]=line.split('\t')[1].strip('\n"')
    print(fea_dict)
    t=[]
    sug_dict={}
    f2=open(result_path,'w')
    for line in tqdm(open(data_path,encoding='utf-8')):
        #load data
        data=dict(json.loads(line))
        #delete and transfer some features
        data1={}
        data1['business_id']=data.pop('business_id')
        data1['name']=data.pop('name')
        data1['stars']=data.pop('stars')
        data1['city']=data.pop('city')
        data1['state']=data.pop('state')
        data1['postal_code']=data.pop('postal_code')
        data1['suggested_postal_code']=data.pop('suggested_postal_code')
        a={}
        #extract nontext features
        a['ByAppointmentOnly']=data.pop('ByAppointmentOnly')
        a['BusinessParking']=data.pop('BusinessParking')
        a['GoodForKids']=-1*data.pop('GoodForKids')
        a['BikeParking']=data.pop('BikeParking')
        a['DogsAllowed']=data.pop('DogsAllowed')
        #delete useless text feature
        day=['weekend_close','weekday_close','weekday_open','weekend_open','BusinessAcceptsCreditCards','time','week','day','year','month','issue','stuff','environment']
        for days in day:
            data.pop(days)
        #extract the first three text features with lowest sentiment score
        text=[]
        for i in range(0,3):
            key=min(data,key=lambda k:data[k])
            data.pop(key)
            text.append(key)
        for texts in text:
            if texts not in t:
                t.append(texts)
        data1['text']=text
        #extract the first three nontext features that the business does not have
        count=0
        nontext=[]
        for keys in a:
            if a[keys]==-1:
                nontext.append(keys)
                count+=1
                if count==3:
                    break
        data1['nontext']=nontext
        #construct suggestions
        recommand=''
        #suggestions for text features
        for texts in text:
            print(texts)
            #for distance, if there exist recommanded postal code, use it as the suggestion
            if texts=='distance':
                if data1['suggested_postal_code']!=None:
                    recommand=recommand+fea_dict[texts][0]+str(data1['suggested_postal_code'])+'.\t'
                else:
                    recommand=recommand+fea_dict[texts][1]+'\t'
            else:
                recommand=recommand+fea_dict[texts]+'\t'
        #suggestions for nontext features
        for nontexts in nontext:
            print(nontexts)
            if nontexts=='BusinessParking':
                if 'parking' not in text:
                    recommand=recommand+fea_dict[nontexts]+'\t'
            elif nontexts=='GoodForKids':
                if 'kid' not in text:
                    recommand=recommand+fea_dict[nontexts]+'\t'
            else:
                recommand=recommand+fea_dict[nontexts]+'\t'
        data1['suggest']=recommand
        print(data1)
        #put all suggestions in a dictionary
        sug_dict[data1['business_id']]=recommand.strip('\t')
    #write suggestions to file
    f2.write(json.dumps(sug_dict))
    print(t)
    print(len(t))

def get_result(data_path,sug_path,result_path):
    #load suggestions generated in extract_recommand
    with open(sug_path,encoding='utf-8') as f1:
        suggestions=dict(json.loads(f1.readline()))
    f2=open(result_path,'w')
    #write file head
    f2.write('name|city|state|address|suggestion\n')
    for lines in tqdm(open(data_path,encoding='utf-8')):
        #load data
        data=dict(json.loads(lines))
        if data['business_id'] in suggestions:
            try:
                #write gym info and suggestions to result file
                gym=data['name']+'|'+data['city']+'|'+data['state']+'|'+data['address']+'|'+suggestions[data['business_id']]+'\n'
                f2.write(gym)
            except:
                #if there is some code which are unrecognized under utf-8, deal with it case by case.
                if data['name'].encode('utf_8')==b'\xc3\x89nergie Cardio Complexe Desjardins':
                    gym='Energie Cardio Complexe Desjardins|Montreal|QC|175 Boul Rene-Levesque O'+suggestions[data['business_id']]+'\n'
                    print(gym)
                    f2.write(gym)
                if data['name'].encode('utf_8')==b'M\xc3\x9cV Integrated Physical Culture':
                    gym='MUV Integrated Physical Culture|Pittsburgh|PA|5469 Penn Ave'+suggestions[data['business_id']]+'\n'
                    print(gym)
                    f2.write(gym)
                if data['name'].encode('utf_8')==b'Centre sportif de Notre-Dame-de-Gr\xc3\xa2ce':
                    gym='Centre sportif de Notre-Dame-de-Grace|Montreal|QC|6445 Avenue de Monkland'+suggestions[data['business_id']]+'\n'
                    print(gym)
                    f2.write(gym)
        
if __name__ == '__main__':
    extract_recommand('./Data/advice.json','./Data/feature_importance.txt','./Data  /suggestions.json')
    get_result('./Data/business_gym.json','./Data/suggestions.json','./Data/gym_suggestion.csv')
