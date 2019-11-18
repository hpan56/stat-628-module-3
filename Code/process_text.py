# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# extract describing words for each aspect
# generate sentiment score for describing words
import spacy
import json
nlp = spacy.load('en_core_web_sm')

aspects = ["class", "time", "place", "staff", "month", "room", "day", "people", "equipment", "membership",
           "clean", "year", "machine", "location", "trainer", "member", "$", "area", "sign", "pay", "week", "lot",
           "hour", "facility", "service", "training", "instructor", "kid",
           "cardio", "locker", "pool", "wait", "walk", "price",
          "open", "check", "charge", "fee", "spa", "minute", "money", "manager", "desk", "club", "massage",
          "coach", "contract", "session", "shower", "yoga", "person", "owner", "home", "family", "issue",
          "towel", "floor", "train", "water", "woman", "space", "child", "card", "24", "problem", "phone", "schedule",
          "employee", "treadmill", "parking", "morning", "sauna", "hot", "music", "girl", "crowd", "night", "man",
          "account", "court", "program", "rate", "management", "steam", "town", "atmosphere", "daughter", "lady",
          "door", "box", "bar", "cost", "tv", "email", "environment", "community", "bathroom", "stuff", "bike", "son",
          "wall", "team", "amenity", "drive", "dirty", "lift", "basketball", "rack", "hair", "weekend", "smell", "bench",
          "climb", "crowded", "track", "refund", "access", "course", "student", "school", "boxing", "teacher", "tour",
          "office", "payment", "food", "bag", "ball", "fan", "elliptical", "appointment", "injury", "locate", "evening",
          "Zumba", "bill", "beginner", "chair", "online", "lock", "section", "mat", "vibe", "spacious", "website",
          "tanning", "key", "air", "condition", "Saturday", "park", "drink", "hurt", "swimming", "hook", "childcare",
          "instruction", "baby", "cleanliness", "downtown", "Groupon", "juice", "People", "dumbbell", "lesson", "lounge",
          "Spa", "discount", "Monday", "maintenance", "dry", "tan", "worker", "afternoon", "counter", "climbing",
           "jacuzzi",
          "monitor", "Sunday", "screen", "boy", "movie", "groupon", "folk", "layout", "pricing", "diet", "Friday",
           "24/7",
          "daycare", "mirror", "zone", "smoothie", "Hour", "pilate", "store", "kickboxe", "meal", "female", "window",
          "spray", "Coach", "restroom", "cafe", "mess", "dollar"]

# create sentiment dictionary
f = open('sen_dic.txt')
sen = f.read()
f.close()
sen = sen.split('\n')
sen = sen[:-1]
sen_dic = {}
for i in sen:
    r = i.split(' ')
    if r[5][14:] == 'positive':
        sen_dic[r[2][6:]] = [3, r[3][5:]]
    if r[5][14:] == 'negative':
        sen_dic[r[2][6:]] = [-3, r[3][5:]]
    else:
        sen_dic[r[2][6:]] = [0.5, r[3][5:]]


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


# input a list of words, output words which are connected to the input
def find_next(word_list, record):
    result = []
    for i in word_list:
        if i in record:
            result = result + record[i]
    return list(set(result))


def find_up(one_word, record):  # input a word, output its root
    for i in record:
        if one_word in record[i]:
            return i
    return None


def sent_sentiment(s):  # input a sentence, output a dictionary of all aspects it mentioned with sentiment scores.
    dependency = generate_record(s)
    sentiment = {}
    for token in s:
        if str(token.text) in aspects:  # discriminate whether there are aspects
            word = [str(token.text)]
            n = 0
            while not str(token.text) in sentiment and n < 4:  # search down three nodes of leaves
                find = find_next(word, dependency)
                for i in find:
                    if i in sen_dic:
                        if sen_dic[i][1] == 'adj':  # if describing words are adjective, add sentiment scores
                            sentiment[str(token.text)] = sen_dic[i][0]
                            break
                        if sen_dic[i][1] == 'verb':  # if describing words are verb and adverb
                            sentiment[str(token.text)] = sen_dic[i][0]
                            try:
                                adv = dependency[i]
                                for w in adv:
                                    if w in sen_dic and sen_dic[w][1] == 'anypos':
                                        sentiment[str(token.text)] = sentiment[str(token.text)]*sen_dic[w][0]
                                        break
                            except:
                                pass
                            break
                word = find
                n = n + 1
            find = str(token.text)
            while not sentiment and n < 8:  # search upward three nodes of leaves
                find_root = find_up(find, dependency)
                if find_root:
                    for i in dependency[find_root]:
                        if i in sen_dic:
                            if sen_dic[i][1] == 'adj':
                                sentiment[str(token.text)] = sen_dic[i][0]
                                break
                            if sen_dic[i][1] == 'verb':
                                sentiment[str(token.text)] = sen_dic[i][0]
                                try:
                                    adv = dependency[i]
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
f1 = open('raw_rbu_text.json', 'w')  # generate sentiment scores for each according to describing words
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    test = nlp(new_dic['text'])
    dic_as = {}
    for s in test.sents:
        value = sent_sentiment(s)
        for i in value:
            if i not in dic_as:
                dic_as[i] = value[i]
            elif abs(value[i]) > dic_as[i]:
                dic_as[i] = value[i]
            else:
                pass
    # print(dic_as)
    new_dic['text'] = dic_as
    json.dump(new_dic, f1)
    f1.write("\n")
f.close()
f1.close()


f = open('raw_rbu_text.json')
f1 = open('process_nontext.json')
f2 = open('model_data.json', 'w')
while True:  # merge with non-text aspects
    line = f.readline()
    line1 = f1.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    new_dic1 = dict(json.loads(line1))
    pd = new_dic['text']
    new_dic1['text'] = pd
    json.dump(new_dic1, f2)
    f2.write("\n")
f.close()
f1.close()
f2.close()

