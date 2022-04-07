from collections import defaultdict

filter_file = "subs_norm1"
out_file = "subs_norm1_filt"
vocabulary = "voc_600k.txt"

remove_repetitions = ["la la la la", "na na na na", "hei hei hei hei", "oh-oh-oh", "♪", "♯", "♬",
                      "oh oh oh oh", "quak quak quak quak", "gack gack gack gack",
                      "nein nein nein nein", "ja ja ja ja", "da da da da", 
                      "o o o o", "mann mann mann mann", "ui ui ui ui",
                      "bäh bäh bäh bäh", "komm komm komm komm", "ha ha ha ha", 
                      "ei ei ei ei", "nee nee nee nee", "weiter weiter weiter weiter",
                      "hey hey hey hey", "ba ba ba ba", "no no no no", "bitte bitte bitte bitte", 
                      "sehr sehr sehr sehr", "he he he he", "ho ho ho ho", "du du du du", 
                      "hopp hopp hopp hopp", "vt vt vt vt", "gut gut gut gut", "stopp stopp stopp stopp", 
                      "scheiße scheiße scheiße scheiße", "musik musik musik musik",
                      "miez miez miez miez", "jude jude jude jude", "krok krok krok krok",
                      "jo jo jo jo", "put put put put", "ta ta ta ta", "— — — —", "� � � �",
                      "bam bam bam bam", "go go go go", "so so so so", "was was was was",
                      "bum bum bum bum", "u u u u", "ich ich ich ich", "hm hm hm hm",
                      "oi oi oi oi", "uh uh uh uh", "au au au au", "hi hi hi hi", 
                      "di di di di", "bumm bumm bumm bumm", "☆ ☆ ☆ ☆", "★ ★ ★ ★",
                      "là là là là", "pam pam pam pam", "b b b b", "o-wim-o-weh o-wim-o-weh o-wim-o-weh o-wim-o-weh",
                      "eh eh eh eh", "nä nä nä nä", "nö nö nö nö", "a a a a", "c c c c", "th th th th",
                      "ah ah ah ah", "hr hr hr hr", "zu zu zu zu", "ma ma ma ma", "ne ne ne ne", 
                      "sch sch sch sch", "tak tak tak tak", "pa pa pa pa", "⁄ ⁄ ⁄ ⁄",
                      "hu hu hu hu", "dü dü dü dü", "ney ney ney ney", "tok tok tok tok",
                      '█ █ █ █', "i i i i", 'ay ay ay ay', 'h h h h', 'ai ai ai ai',
                      'ka ka ka ka', 'wi wi wi wi', "bä bä bä bä", "dei dei dei dei",
                      '〉 〉 〉 〉', "iah iah iah iah", "wow wow wow wow", "wa wa wa wa",
                      "f f f f", "öh öh öh öh", "aaaah aaaah aaaah aaaah", "fub fub fub fub",
                      "ga ga ga ga", "hoh hoh hoh hoh", "ko ko ko ko"]]
                                                                           
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
