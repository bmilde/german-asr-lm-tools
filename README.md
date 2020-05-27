# german-asr-lm-tools

This repository contains a couple of Python scripts that you can use to build resources for language modeling for German. Primary target is training a LM for ASR, see e.g. https://github.com/uhh-lt/kaldi-tuda-de/

Install prerequisites: 

```
pip3 install requests spacy
```

# Creating a LM resource from the German Wikipedia

Find the newest dewiki dump from https://dumps.wikimedia.org/backup-index.html

For example: https://dumps.wikimedia.org/dewiki/20200520/

Download the pages-articles-multistream file:

wget https://dumps.wikimedia.org/dewiki/20200520/dewiki-20200520-pages-articles-multistream.xml.bz2

Clone the wikiextractor package:

git clone https://github.com/attardi/wikiextractor
mkdir norm/

Now use the wikiextractor to store the output as compressed bz files in the norm/ folder. Splitting into multiple files is recommended so that you can use multiple cores for the following step:

Then use convert_wiki_norm.sh to normalize these files in parallel. This will remove punctuation and translates numerals into text form ("42" -> zwei und vierzig), expands abbreviations and does other normalizations specific to wiki texts. This step needs the spacy library with the German spacy model downloaded and installed.

```
./convert_wiki_norm.sh
```

# Crawling taggesschau news

```
output_file = 'tagesschau_news_may19_may20.txt'
compteted_dates_file = 'tagesschau_news_may19_may20_completed.log'
```

Now run the crawler:

```
python3 get_texts_taggesschau.py
```

The output file will contain the news texts and the log file will log success/fail for individual days of the archive. It is normal that some links can't be retrieved and this can be safetly ignored as long as the majority of files can be downlooaded. The tagesschau news archive stores old news up to 365 days.

Now filter some utterances that are not needed in LM modelling with a reverse grep:

```
grep -v "^Stand: " tagesschau_news_may19_may20.txt | grep -v "^Quelle:" > tagesschau_news_may19_may20_filt.txt
```

TODO: normalize these sentences

# Crawling Mediathek subtitles

First run ./download_public_German_TV_subtitles.sh

This will probe Mediathek servers for subtitles IDs. The default range will work well, but you might need to tweak the values if you want to download the newest subtitles.

This stores a bunch of subtitle XML files in mediathek_subs/

Now you need to extract the raw text from these subtitle files with: 

```
python3 extract_mediathek_text.py
```

You should check if everything went well by inspecting the output file: raw_text_subs3

Now you can a two staged normalization:

Filter some subtitle utterances that don't make sense for language modeling, this is specific to mediathek subtitle files:

```
python3 normalize_subs.py
```

This should create a file named "raw_subs_norm_text", with the filtered output. 

Now we do a few more normalizations that are specific to ASR, such as translate numerals into text form ("42" -> zwei und vierzig), remove all punctuation and recapitalizing the first word in a sentence ("Das Haus ist grün" -> "das Haus ist grün").

This step needs the spacy Python library installed with German models for part of speech tagging models downloaded. See https://github.com/explosion/spaCy for details.

```
python3 normalize_subs_sentences.py raw_subs_norm_text subs_norm1
```

Since the above takes a long time to finish, you can also use the unix tool "split" to split raw_subs_norm_text into N files and then use the ./convert_subs_norm.sh script to normalize in parallel across N cores.

This will take the "raw_subs_norm_text" as input file and output the filtered text into "subs_norm1"

# Create the vocabulary file

Now we use the statistics script to create the vocabulary file. Edit the variable "file"s and "output_voc" of statistics.py to suit your needs. This will generate a sorted vocabulary file with the top most used words at the top along with their frequency:

```
und 41327933
der 36773961
die 34655617
in 21432409
Hundert 15671589
das 15588621
ist 12763524
von 12378265
den 11900956
im 11047577
ein 10661592
mit 10286659
```

To generate a vocabulary file for Kaldi you can use the bash programs cut and head:

```
cut -d" " -f 1 ../lm_wiki_and_tv/new_complete_voc.txt | head -n 600000 > 
```

# Final filtering of mediathek subs

The mediathek subtitles contain a substianial number of English lyrics and songs and other problematic utterances for language modeling ("na na na na na na na na na") that we filter in a final step. First configure

```
filter_file = "subs_norm1"
out_file = "subs_norm1_filt"
vocabulary = "voc_600k.txt"
```

This makes use of the vocabulary file generated in the above step. Now run final_subs_filter.py:

```
python3 final_subs_filter.py
```

This will create the "subs_norm1_filt" output file.
