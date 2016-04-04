import jsonlines
f = jsonlines.open('reviews_csm2.jsonl', 'w')

for i in jsonlines.open('reviews_csm.jsonl'):
    i['rating'] = int(i['rating']) * 2
    jsonlines.Writer.dump(f, i)
