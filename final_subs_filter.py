from collections import defaultdict

filter_file = "subs_norm1"
out_file = "subs_norm1_filt"
vocabulary = "voc_600k.txt"

remove_repetitions = ["la la la la", "na na na na", "hei hei hei hei", "oh-oh-oh", "♪", "♯",
                      "oh oh oh oh", "quak quak quak quak", "gack gack gack gack",
                      "nein nein nein nein", "ja ja ja ja", "da da da da", 
                      "O O O O", "mann mann mann mann", "ui ui ui ui",
                      "bäh bäh bäh bäh", "komm komm komm komm", "ha ha ha ha", 
                      "ei ei ei ei", "nee nee nee nee", "weiter weiter weiter weiter",
                      "hey hey hey hey", "ba ba ba ba", "no no no no", "bitte bitte bitte bitte", 
                      "sehr sehr sehr sehr", "he he he he", "ho ho ho ho", "du du du du", 
                      "hopp hopp hopp hopp", "vt vt vt vt", "gut gut gut gut", "stopp stopp stopp stopp", 
                      "scheiße scheiße scheiße scheiße", "musik musik musik musik",
                      "miez miez miez miez", "jude jude jude jude", "krok krok krok krok",
                      "jo jo jo jo", "put put put put", "ta ta ta ta", "— — — —", "� � � �",
                      "bam bam bam bam", "go go go go", "so so so so", "was was was was",
                      "bum bum bum bum", "U U U U", "ich ich ich ich", 
                      "oi oi oi oi", "uh uh uh uh", "au au au au", "hi hi hi hi", "hm hm hm hm",
                      "di di di di", "bumm bumm bumm bumm"]
                                                                           
dictionary_filter_score = True
voc = {}

if dictionary_filter_score:
    with open(vocabulary) as vocabulary_file_in:
        for line in vocabulary_file_in:
            if line[-1] == '\n':
                line = line[:-1]
            voc[line.split()[0]] = 1

with open(filter_file) as filter_file_in, open(out_file, 'w') as outfile:
    for line in filter_file_in:
        line_lower = line.lower()
        should_remove = False
        
        for remove_repetition in remove_repetitions:
            if remove_repetition in line_lower:
                should_remove = True
        
        if should_remove:
            print('Removing', line)
            continue       

        split = line.replace('-',' ').split()

        if dictionary_filter_score:
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
        if dictionary_filter_score:
            if len_split > 6 and score < 3:
                print('Removing', line)
                continue

        outfile.write(line)
