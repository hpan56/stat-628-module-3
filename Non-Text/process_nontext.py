import json
import time
from tqdm import tqdm

def process_nontext(data_path,result_path):
    f1=open(result_path,'w')
    delete_list=['hours','funny','cool','text','address','postal_code','latitude','longitude','attributes','categories','user_funny','user_cool','elite','compliment_hot','compliment_more','compliment_profile','compliment_cute','compliment_list','compliment_note','compliment_plain','compliment_cool','compliment_funny','compliment_writer','compliment_photos']
    day=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    twolevel=['ByAppointmentOnly', 'GoodForKids', 'BusinessAcceptsCreditCards','BikeParking','AcceptsInsurance','WheelchairAccessible','DogsAllowed','BusinessAcceptsBitcoin','HasTV','OutdoorSeating']
    multilevel=['BusinessParking','GoodForMeal','Music','HairSpecializesIn']
    colevel=['WiFi','Smoking','intimate','casual','NoiseLevel']
    levels=twolevel+multilevel+colevel
    for line in tqdm(open(data_path,encoding='utf-8')):
        data=dict(json.loads(line))
        #useful
        data['useful']=data['useful']+data['funny']+data['cool']
        #attribute
        if data['attributes']:
            for level in levels:
                data[level]=0
            for level in twolevel:
                if level in data['attributes']:
                    if data['attributes'][level]!='None':
                        if data['attributes'][level]=='True':
            for level in multilevel:
                if level in data['attributes']:
                    if data['attributes'][level]!='None':
                        dic=eval(data['attributes'][level])
                        for keys in dic:
                            if dic[keys]==True:
                                data[level]=1
            if 'WiFi' in data['attributes']:
                if data['attributes']['WiFi']=="'free'" or data['attributes']['WiFi']=="u'free'" or data['attributes']['WiFi']=="'paid'" or data['attributes']['WiFi']=="u'paid'":
                    data['WiFi']=1
            if 'Smoking' in data['attributes']:
                if data['attributes']['Smoking']=="'no'" or data['attributes']['Smoking']=="u'no'":
                    data['Smoking']=1
            if 'Alcohol' in data['attributes']:
                if data['attributes']['Alcohol']=="'full_bar'" or data['attributes']['Alcohol']=="u'full_bar'":
                    data['Alcohol']=1
            if 'Ambience' in data['attributes']:
                if eval(data['attributes']['Ambience'])['intimate']==True:
                    data['intimate']=1
                elif eval(data['attributes']['Ambience'])['casual']==True:
                    data['casual']=1
            if 'NoiseLevel' in data['attributes']:
                if data['attributes']['NoiseLevel']=="u'very_loud'":
                    data['NoiseLevel']=1
        #hours
        for days in day:
            try:
                hours=data['hours'][days].replace(':','.').replace('.3','.5').split('-')
                data[days+'_open']=float(hours[0])
                data[days+'_close']=float(hours[1])
            except:
                a=1
        #user_useful
        data['user_useful']=data['user_useful']+data['user_funny']+data['user_cool']
        data['compliment']=data['compliment_hot']+data['compliment_more']+data['compliment_profile']+data['compliment_cute']+data['compliment_list']+data['compliment_note']+data['compliment_plain']+data['compliment_cool']+data['compliment_funny']+data['compliment_writer']+data['compliment_photos']
        for keys in delete_list:
            data.pop(keys) 
        # ~ print(data)
        f1.write(json.dumps(data)+'\n')


def test(data_path):
    for line in tqdm(open(data_path,encoding='utf-8')):
        data=dict(json.loads(line))
        print(data)
    # ~ l=[]
    # ~ for line in tqdm(open(data_path,encoding='utf-8')):
        # ~ data=dict(json.loads(line))
        # ~ level='Ambience'
        # ~ if data['attributes']:
            # ~ if level in data['attributes']:
                # ~ if data['attributes'][level] not in l:
                    # ~ l.append(eval(data['attributes'][level]))
    # ~ print(l)
    # ~ f1=open('data/tmp.json','w')
    # ~ with open(data_path,encoding='utf-8')as f:
        # ~ for i in range(0,1000):
            # ~ data=dict(json.loads(f.readline())) 
            # ~ if data['attributes']:
                # ~ if 'WiFi' in data['attributes']:
                    # ~ if data['attributes']['WiFi']=="u'no'":
                        # ~ print(data['attributes'])

# ~ ['ByAppointmentOnly', 'GoodForKids', 'BusinessAcceptsCreditCards', 'BusinessParking', 'BikeParking','AcceptsInsurance'
# ~ , 'WheelchairAccessible', 'DogsAllowed', 'BusinessAcceptsBitcoin', 
# ~ ,  'WiFi', 'GoodForMeal', 'HasTV', 'Smoking', 'Ambience', 'Alcohol', 
# ~ , 'OutdoorSeating', 'Music', 'NoiseLevel', 'HairSpecializesIn']
        
if __name__ == '__main__':
    t=time.time()
    # ~ process_nontext('data/raw_rbu.json','data/process_nontext.json')
    test('data/process_nontext.json')
    print(time.time()-t)
