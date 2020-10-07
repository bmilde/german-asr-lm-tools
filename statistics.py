from collections import defaultdict
import argparse
voc = defaultdict(int)
linenum = 0

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', action='append', nargs='*')
parser.add_argument('-o', '--output', required=True)
args = parser.parse_args()
files = args.files[0]
output_voc = args.output

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
            for word in line.split():
                voc[word] += 1
            linenum += 1
            if linenum % 10000 == 0:
                print("file",filename,"linenum:",linenum,line)

sorted_voc = sorted(voc.items(), key=lambda kv: kv[1], reverse=True)

print("First hundered words:")

print(sorted_voc[:100])

with open(output_voc,"w") as out_file:
    for tup in sorted_voc:
        out_file.write(tup[0] + " " + str(tup[1]) + '\n')
