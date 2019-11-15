# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import spacy
import json
nlp = spacy.load('en_core_web_sm')

aspects = ['basketball', 'rack', 'hair', 'weekend', 'smell', 'bench', 'climb',
           'crowded', 'track', 'refund', 'access', 'course', 'student', 'school', 'boxing', 'teacher', 'tour',
           'office', 'payment', 'food', 'bag', 'ball', 'fan', 'elliptical', 'appointment', 'injury', 'locate',
           'evening', 'Zumba', 'bill', 'beginner', 'chair', 'online', 'lock', 'section', 'mat', 'vibe',
           'spacious', 'website', 'tanning', 'key', 'air', 'condition', 'Saturday', 'park', 'drink', 'hurt',
           'swimming', 'hook', 'childcare', 'instruction', 'baby', 'cleanliness', 'downtown', 'Groupon',
           'juice', 'People', 'dumbbell', 'lesson', 'lounge', 'Spa', 'discount', 'Monday', 'maintenance',
           'dry', 'tan', 'worker', 'afternoon', 'counter', 'climbing', 'jacuzzi', 'monitor', 'Sunday',
           'screen', 'boy', 'movie', 'groupon', 'folk', 'layout', 'pricing', 'diet', 'Friday', '24/7', 'daycare',
           'mirror', 'zone', 'smoothie', 'Hour', 'pilate', 'store', 'kickboxe', 'meal', 'female', 'window',
           'spray', 'Coach', 'restroom', 'cafe', 'mess','class', 'work', 'time', 'place', 'staff',
           'month','room', 'day', 'people', 'equipment', 'membership', 'clean', 'year', 'machine',
           'location', 'trainer', 'member', '$', 'fitness', 'area', 'sign', 'pay', 'week', 'lot', 'hour',
           'facility', 'service', 'training', 'instructor', 'kid', 'cardio', 'locker', 'pool', 'wait',
           'walk', 'price', 'open', 'check', 'charge', 'fee', 'spa', 'minute', 'money', 'manager',
           'desk', 'club', 'close', 'massage', 'coach', 'contract', 'session', 'shower', 'yoga', 'person',
           'owner', 'home', 'family', 'Vegas', 'issue', 'towel', 'floor', 'train', 'water', 'LA', 'woman',
           'space', 'child', 'card', '24', 'problem', 'phone', 'schedule', 'employee', 'treadmill', 'parking',
           'morning', 'sauna', 'hot', 'music', 'girl', 'crowd', 'night', 'man', 'account', 'court', 'program',
           'rate', 'management', 'steam', 'town', 'atmosphere', 'daughter', 'lady', 'client', 'door', 'box',
           'bar', 'cost', 'tv', 'email', 'environment', 'community', 'bathroom', 'stuff', 'bike', 'son',
           'wall', 'team', 'amenity', 'drive', 'dirty', 'lift']
negative_words = ["no", "n't", "never", "neither", "nor", "nobody", "none", "nothing", "none", "not",
                  "nowhere", "n’t", "hardly", "barely", "scarcely", "rarely", "seldom", "little", "few"]


# create sentiment dictionary
f = open('sen_dic.txt')
sen = f.read()
f.close()
sen = sen.split('\n')
sen = sen[:-1]
sen_dic = {}  # 创建情感词典
for i in sen:
    r = i.split(' ')
    if r[5][14:] == 'positive':
        sen_dic[r[2][6:]] = [3, r[3][5:]]
    if r[5][14:] == 'negative':
        sen_dic[r[2][6:]] = [-3, r[3][5:]]
    else:
        sen_dic[r[2][6:]] = [0.5, r[3][5:]]
for i in negative_words:
    if i in sen_dic:
        sen_dic.pop(i)


def generate_record(sent):  # to make the dependence relationship into a dictionary
    record = {}
    for token in sent:
        if not sent.root.is_ancestor(token):
            record['root'] = [token.text]
            continue
        if not token.head.is_punct:
            if token.head.text not in record:
                record[token.head.text] = [token.text]
            else:
                record[token.head.text].append(token.text)
    return record


# 构造函数向下遍历树的函数，输入一个词的list，找出下层词的list，BFS遍历
def find_next(word_list, record):
    result = []
    for i in word_list:
        if i in record:
            result = result + record[i]
    return list(set(result))


def find_up(one_word, record):  # 输入一个word, 输出它的根节点
    for i in record:
        if one_word in record[i]:
            return i
    return None


def sent_sentiment(s):  # 首先判断每个句子中是否存在aspects，如果存在存下aspects，再分层找情感词，先下两层，再同层，再上两层。
    dependency = generate_record(s)
    sentiment = {}
    for token in s:
        if str(token.text) in aspects:  # 判断aspect存在
            word = [str(token.text)]
            n = 0
            while not str(token.text) in sentiment and n < 3:  # 在尚未找到aspect对应的grade时,往下三层
                find = find_next(word, dependency)  # 往下找
                for i in find:
                    if i in sen_dic:
                        if sen_dic[i][1] == 'adj':  # 如果是形容词，直接判断
                            sentiment[str(token.text)] = sen_dic[i][0]
                            break
                        if sen_dic[i][1] == 'verb':  # 如果是动词，向下找一个副词
                            sentiment[str(token.text)] = sen_dic[i][0]
                            try:
                                adv = dependency[i]  # 该动词是一个根节点，有词在形容它
                                for w in adv:
                                    if w in sen_dic and sen_dic[w][1] == 'anypos':
                                        sentiment[str(token.text)] = sentiment[str(token.text)]*sen_dic[w][0]
                                        break
                            except:
                                pass
                            break
                word = find  # 继续往下找
                n = n + 1
            # 同层找和往上回溯
            find = str(token.text)
            while not sentiment and n < 7:  # 同层及往上找3层
                find_root = find_up(find, dependency)
                if find_root:
                    for i in dependency[find_root]:
                        if i in sen_dic:
                            if sen_dic[i][1] == 'adj':  # 如果是形容词，直接判断
                                sentiment[str(token.text)] = sen_dic[i][0]
                                break
                            if sen_dic[i][1] == 'verb':  # 如果是动词，向下找一个副词
                                sentiment[str(token.text)] = sen_dic[i][0]
                                try:
                                    adv = dependency[i]  # 该动词是一个根节点，有词在形容它
                                    for w in adv:
                                        if w in sen_dic and sen_dic[w][1] == 'anypos':
                                            sentiment[str(token.text)] = sentiment[str(token.text)]*sen_dic[w][0]
                                            break
                                except:
                                    pass
                                break
                find = find_root
                n = n + 1
    return sentiment


# aspects = ['ER', 'room', 'place', 'care', 'facility']


f = open('raw_rbu.json')
for i in range(500):
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    test = nlp(new_dic['text'])
    for s in test.sents:
        value = sent_sentiment(s)
        if value:
            for token in s:
                if str(token) in negative_words:  # 只要整个句子中有negative_word
                    for v in value:
                        value[v] = value[v] * -1
                        # pass
            print(value)

f.close()

