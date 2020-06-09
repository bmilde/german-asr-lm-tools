from collections import defaultdict

voc = defaultdict(int)
linenum = 0

output_voc = "voc_subs.txt"
files = ["subs_norm1_filt", "de_wiki", "europarl", "tagesschau_news"] #,"subs_norm1"]
#num_range = 45

#files = ["train_text.txt"]
output_voc = "new_complete_voc.txt"

#output_voc = "voc_output.txt"
#filename_mask = "IT_Ethik_deep_learning_text_normalized"
#num_range = 1

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
