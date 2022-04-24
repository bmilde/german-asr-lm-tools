from collections import defaultdict
import argparse
voc = defaultdict(int)
common_repeating_ngrams = defaultdict(int)
linenum = 0

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', action='append', nargs='*')
parser.add_argument('-o', '--output', required=True)
args = parser.parse_args()
files = args.files[0]
output_voc = args.output

def ngrams(input_list, n):
# from https://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams
    if n<=1:
        return [[elem] for elem in input_list]
    return zip(*[input_list[i:] for i in range(n)])

# num_range = 45
# files = ["train_text.txt"]
# filename_mask = "IT_Ethik_deep_learning_text_normalized"
# num_range = 1

for filename in files:

#    if "%" in filename_mask:
#        filename = filename_mask % x
#    else:
#        filename =  filename_mask
    print('Filename:', filename)
    with open(filename) as in_file:
        for line in in_file:
            if line[-1] == '/n':
                line = line[:-1]
            split = line.split()
            for word in line.split():
                voc[word] += 1
            for trigram in ngrams(split, 4):
                if trigram[0] == trigram[1] and trigram[1] == trigram[2] and trigram[2]==trigram[3]:
                    common_repeating_ngrams[' '.join(trigram)] += 1

            linenum += 1
            if linenum % 10000 == 0:
                print("file",filename,"linenum:",linenum,line)

sorted_voc = sorted(voc.items(), key=lambda kv: kv[1], reverse=True)

sorted_rep_trigrams = sorted(common_repeating_ngrams.items(), key=lambda kv: kv[1], reverse=True)

print("First hundered words:")
print(sorted_voc[:100])

print("Most common repeating trigrams:")
print(sorted_rep_trigrams[:300])

with open(output_voc,"w") as out_file:
    for tup in sorted_voc:
        out_file.write(tup[0] + " " + str(tup[1]) + '\n')
