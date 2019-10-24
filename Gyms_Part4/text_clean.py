import spacy
import copy
import json
nlp = spacy.load('en_core_web_sm')


def generate_record(sent):
    record = {}  # to make the dependence relationship into a dictionary
    for token in sent:
        if token.head.text == token.text:
            record['root'] = [token.text]
            continue
        if token.head.text not in record:
            record[token.head.text]=[token.text]
        else:
            record[token.head.text].append(token.text)
    return record


# input a list containing the keys want to be checked，and return keys want to be checked in the next turn
def one_step(c_key, re):
    fb = copy.deepcopy(re)
    keys = list(fb.keys())
    result = []
    for i in c_key:
        for j in fb[i]:
            if j in keys:
                result.append(j)
            elif noise[j]:
                re[i].remove(j)
            else:
                pass
    return list(set(result))

# input a record dictionary of a sentence, it will return a clean dictionary containing three levels of relationship
# and the root value


def deal_sent(re):
    dynamic = re['root']
    i = 0
    key_re = []
    while i < 4 and len(dynamic) > 0:
        key_re.append([e for e in dynamic])
        dynamic = one_step(dynamic, re)
        i = i+1
    final = {'root': re['root']}
    for p in key_re:
        for q in p:
            final[q] = re[q]
    return final


f = open('gym_review.json')
f1 = open('gym_review_text.json', 'w')

for i in range(3000):
    line = f.readline()
    if not line:
        break
    dic_new = json.loads(line)
    texts = dic_new['text'].replace("\n", "").lower()
    texts = nlp(texts)
    deal = []
    for s in texts.sents:
        try:
            noise = {str(i): (i.is_stop or i.dep_ == 'punct') and i.dep_ != 'neg' and i.dep_ != 'nsubj' for i in s}
            # discriminate stop words in a sentence
            deal.append(deal_sent(generate_record(s)))
        except:
            print(s)
    dic_new['text'] = deal
    json.dump(dic_new, f1)
    f1.write("\n")

f.close()
f1.close()





