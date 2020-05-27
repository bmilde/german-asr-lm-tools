import re
from bz2 import BZ2File as bzopen

from collections import defaultdict

# Findet den Ausdruck den man haben will
def finde_ausdruck(ausdruck, text):
    match = re.search(ausdruck, text)
    if not match:
        return None, None
    begin = match.start() ## füll mich aus
    end = match.end()
    return begin, end

#filename_mask = "IT_Ethik_deep_learning_text_normalized"
filename_mask = "norm/%.2d.txt"

filename_mask = "output/AA/wiki_%.2d.bz2"
num_range = 44

regex = "([^ ]+ 1[0-9]{3} [^ ]+)"

pres = defaultdict(int)
posts = defaultdict(int)

for x in range(num_range):
    if "%" in filename_mask:
        filename = filename_mask % x
    else:
        filename =  filename_mask
    print('Filename:', filename)
    with bzopen(filename) as bzin:
        for line in bzin:
            try:
                line = line.decode('utf-8')

                if line[-1] == '/n':
                    line = line[:-1]
                begin, end = finde_ausdruck(regex, line)
                if end:
                    exp = line[begin:end]
                    split = exp.split()
                    pres[split[0]] += 1
                    posts[split[2]] += 1

            except:
                print("Error in line:", line)


pres_sorted = sorted(pres.items(), key= lambda k: k[1], reverse=True)
posts_sorted = sorted(posts.items(), key= lambda k: k[1], reverse=True)

print('pres:')
print('"),("'.join([elem[0] for elem in pres_sorted[:200]]))

print('posts:')
print('"),("'.join([elem[0] for elem in posts_sorted[:200]]))

