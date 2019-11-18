# !/usr/bin/env python3
# -*- coding: utf-8 -*-
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
negative_words = ["no", "n't", "never", "neither", "nor", "nobody", "none", "nothing", "none", "not",
                  "nowhere", "n’t", "hardly", "barely", "scarcely", "rarely", "seldom", "little", "few"]


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
        if str(token.text) in aspects:
            word = [str(token.text)]
            n = 0
            while not str(token.text) in sentiment and n < 3:
                find = find_next(word, dependency)
                for i in find:
                    if i in sen_dic:
                        if sen_dic[i][1] == 'adj':
                            sentiment[str(token.text)] = [sen_dic[i][0], i]
                            break
                        if sen_dic[i][1] == 'verb':
                            sentiment[str(token.text)] = [sen_dic[i][0], i]
                            try:
                                adv = dependency[i]
                                for w in adv:
                                    if w in sen_dic and sen_dic[w][1] == 'anypos':
                                        sentiment[str(token.text)][0] = sentiment[str(token.text)][0]*sen_dic[w][0]
                                        sentiment[str(token.text)][1] = sentiment[str(token.text)][1] + '&' + w
                                        break
                            except:
                                pass
                            break
                word = find
                n = n + 1
            find = str(token.text)
            while not sentiment and n < 7:
                find_root = find_up(find, dependency)
                if find_root:
                    for i in dependency[find_root]:
                        if i in sen_dic:
                            if sen_dic[i][1] == 'adj':
                                sentiment[str(token.text)] = [sen_dic[i][0], i]
                                break
                            if sen_dic[i][1] == 'verb':
                                sentiment[str(token.text)] = [sen_dic[i][0], i]
                                try:
                                    adv = dependency[i]
                                    for w in adv:
                                        if w in sen_dic and sen_dic[w][1] == 'anypos':
                                            sentiment[str(token.text)][0] = sentiment[str(token.text)][0]*sen_dic[w][0]
                                            sentiment[str(token.text)][1] = sentiment[str(token.text)][1] + '&' + w
                                            break
                                except:
                                    pass
                                break
                find = find_root
                n = n + 1
    return sentiment


f = open('raw_rbu.json')
f1 = open('raw_rbu_text_record.json', 'w')
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    test = nlp(new_dic['text'])
    dic_as = {}
    dic_as1 = {}
    for s in test.sents:
        value = sent_sentiment(s)
        if value:
            for token in s:
                if str(token) in negative_words:
                    for v in value:
                        value[v][0] = value[v][0] * -1
                        value[v][1] = value[v][1]
        for i in value:
            if i not in dic_as:
                dic_as[i] = value[i][0]
                dic_as1[i] = value[i][1]
            elif abs(value[i][0]) > dic_as[i]:
                dic_as[i] = value[i][0]
                dic_as1[i] = value[i][1]
            else:
                pass
    new_dic['text'] = dic_as1
    json.dump(new_dic, f1)
    f1.write("\n")
f.close()
f1.close()

