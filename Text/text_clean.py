import json

f = open('raw_rbu_text.json')
f1 = open('raw_text.json','w')
while True:
    line = f.readline()
    if not line:
        break
    new_dic = dict(json.loads(line))
    pd = new_dic['text']
    for i in pd:
        if abs(pd[i]) <= 0.5:
            pd[i] = 0
        elif pd[i] > 0.5:
            pd[i] = 1
        else:
            pd[i] = -1
    new_dic['text'] = pd
    json.dump(new_dic, f1)
    f1.write("\n")
f.close()
f1.close()

