from collections import defaultdict

filter_file = "subs_norm1"
out_file = "subs_norm1_filt"
vocabulary = "voc_600k.txt"

voc = {}
with open(vocabulary) as vocabulary_file_in:
    for line in vocabulary_file_in:
        if line[-1] == '\n':
            line = line[:-1]
        voc[line.split()[0]] = 1

with open(filter_file) as filter_file_in, open(out_file, 'w') as outfile:
    for line in filter_file_in:
        if "na na na na" in line:
            print('Removing', line)
            continue
        if "oh-oh-oh" in line:
            print('Removing', line)
            continue

        if "♪" in line:
            print('Removing', line)
            continue

        split = line.replace('-',' ').split()

        score = 0
        for word in split:
            if word in voc:
                score += 1

        len_split = len(split)

        if len_split==0:
            continue

#        if (len_split == 1 or len_split == 2) and score < 1:
#            print('Removing', line)
#            continue

        if len_split > 6 and score < 3:
            print('Removing', line)
            continue

        outfile.write(line)
