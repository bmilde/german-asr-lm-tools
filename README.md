# german-asr-lm-tools

This repository contains a couple of Python scripts that you can use to build resources for language modeling for German. Primary target is training a LM for ASR, see e.g. https://github.com/uhh-lt/kaldi-tuda-de/

Install prerequisites: 

```
pip3 install requests spacy beautifulsoup4 lxml && python -m spacy download de
```

# Creating a LM resource from the German Wikipedia

Find the newest Wikipedia dumps at https://dumps.wikimedia.org/backup-index.html.
We use the dewiki dumps: https://dumps.wikimedia.org/dewiki/

For example: https://dumps.wikimedia.org/dewiki/20200520/

Download the pages-articles-multistream file:
```
wget https://dumps.wikimedia.org/dewiki/20200520/dewiki-20200520-pages-articles-multistream.xml.bz2
```
Download the wikiextractor package (Due to problems with the repository we can't clone it):
```
wget https://github.com/attardi/wikiextractor/archive/f8282ab41090f94b7dfd17ce58a985f537db6c21.zip
unzip -j f8282ab41090f94b7dfd17ce58a985f537db6c21.zip -d wikiextractor
mkdir wikiextractor_output/
mkdir norm/
```
Now use the wikiextractor to store the output as compressed bz files in the `norm/` folder. Splitting into multiple files is recommended so that you can use multiple cores for the following step, use the `--bytes` flag to set a filesize for the output. Also in the example we use 28 processes:

```
cd wikiextractor
python3 WikiExtractor.py -o ../wikiextractor_output/ --processes 28 --filter_disambig_pages --min_text_length 0 --compress --bytes 64M --ignored_tags abbr,b,big --no_templates -q ../dewiki-20200520-pages-articles-multistream.xml.bz2
```

Then use `convert_wiki_norm.sh` to normalize these files in parallel (check that the number of output file matches the number in the script). This step will remove punctuation and translates numerals into text form ("42" -> zwei und vierzig), expands abbreviations and do other normalizations specific to wiki texts. This step needs the spacy Python library with the German spacy model downloaded and installed.

```
cd ..
./convert_wiki_norm.sh
```

This will put the normalized files in the `norm/` folder. You can then simply concatenate all files to a single file with 

```
cat norm/*.txt > de_wiki
```

# Crawling taggesschau news

First, configure `output_file` and `compteted_dates_file` in `get_texts_taggesschau.py`

```
output_file = 'tagesschau_news_may19_may20.txt'
compteted_dates_file = 'tagesschau_news_may19_may20_completed.log'
```

Now run the crawler:

```
python3 get_texts_taggesschau.py
```

The output file will contain the news texts and the log file will log success/fail for individual days of the archive. It is normal that some links can't be retrieved and this can be safetly ignored as long as the majority of files can be downloaded. The tagesschau news archive stores old news up to 365 days.

Now filter some utterances that are not needed in LM modelling with a reverse `grep`:

```
grep -v "^Stand: " tagesschau_news_may19_may20.txt | grep -v "^Quelle:" > tagesschau_news_may19_may20_filt.txt
```

You can now use the wikipedia cleanup script on the Tagesschau news data as well (it only takes compressed bzip2 as input, so compress with `bzip2` first):

```
bzip2 tagesschau_news_may19_may20_filt.txt
python3 normalize_wiki_sentences.py tagesschau_news_may19_may20_filt.txt.bz2 tagesschau_news
```

You now have the cleaned `tagesschau_news` text for LM training, with news from the past 365 days.

# Crawling Mediathek subtitles

First run 
```
./download_public_German_TV_subtitles.sh
```

This will probe Mediathek servers for subtitles IDs. The default range will work well, but you might need to tweak the values if you want to download the newest subtitles.

This stores a bunch of subtitle XML files in `mediathek_subs/`

Now you need to extract the raw text from these subtitle files with: 

```
python3 extract_mediathek_text.py -d mediathek_subs/ -o raw_text_subs3 -p 28
```

You should check if everything went well by inspecting the output file: `raw_text_subs3`

Now you can a two staged normalization:

Filter some subtitle utterances that don't make sense for language modeling, this is specific to mediathek subtitle files:

```
python3 normalize_subs.py -f raw_text_subs3 -o raw_subs_norm_text
```

This should create a file named `raw_subs_norm_text` with the filtered output. 

Now we do a few more normalizations that are specific to ASR, such as translate numerals into text form ("42" -> zwei und vierzig), remove all punctuation and recapitalizing the first word in a sentence ("Das Haus ist grün" -> "das Haus ist grün").

This step needs the spacy Python library installed with German models for part of speech tagging models downloaded. See https://github.com/explosion/spaCy for details.

```
python3 normalize_subs_sentences.py raw_subs_norm_text subs_norm1
```
This will take the `raw_subs_norm_text` as input file and output the filtered text into `subs_norm1`

Since the above takes a long time to finish, you can also use the unix tool `split` to split `raw_subs_norm_text` into N files and then use the `./convert_subs_norm.sh` script to normalize in parallel across N cores.

```
mkdir split
split -n 28 raw_subs_norm_text split/line
mkdir norm/split
./convert_subs_norm.sh
```

This will put the normalized files in the `norm/split` folder. You can then simply concatenate all files to a single file with

```
cat norm/split/* > subs_norm1
```


# Normalized Europarl

```
wget https://www.statmt.org/europarl/v7/de-en.tgz
tar xvfz de-en.tgz
```

Split the files for parallel processing:

```
mkdir europarl_split
split -l 100000 europarl-v7.de-en.de europarl_split/e_
mkdir -p europarl_norm/europarl_split
```

Now run the normalization:

```
./convert_europarl_norm.sh
```

And copy the output into a single file:

```
cat europarl_norm/europarl_split/* >> europarl
```

# Create the vocabulary file

Now we use the statistics script to create the vocabulary file in two steps. Start the `statistics.py` Script with the parameters `-f` for the input files and `-o` for the output file. 
Edit the variable `files` and `output_voc` of `statistics.py` to suit your needs. Then run:

```
python3 statistics.py -f subs_norm1 de_wiki europarl tagesschau_news -o complete_voc.txt
```

This will generate a sorted vocabulary file with the top most used words at the top along with their frequency:

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

# Final filtering of mediathek subs

The mediathek subtitles contain a substianial number of English lyrics and songs and other problematic utterances for language modeling ("na na na na na na na na na") that we filter in a final step. First configure

```
filter_file = "subs_norm1"
out_file = "subs_norm1_filt"
vocabulary = "voc_600k.txt"
```

This makes use of the vocabulary file generated in the above step. Now run `final_subs_filter.py`:

```
python3 final_subs_filter.py
```

This will create the `subs_norm1_filt` output file.

After this step we run the `statistics.py` Script a second time

```
python3 statistics.py -f subs_norm1_filt de_wiki europarl tagesschau_news -o complete_voc.txt
```

# Generate Kaldi vocabulary

To generate a vocabulary file for Kaldi you can use the bash programs cut and head:

```
cut -d" " -f 1 complete_voc.txt | head -n 600000 > voc_600k.txt 
```

# Size of all cleaned sentences

Currently (May 2020) we have gathered about 102 million cleaned German sentences in total with the above method:

```
wc subs_norm1_filt de_wiki europarl tagesschau_news
  51410053  455188544 2881248575 subs_norm1_filt
  48876923  801712134 5772118925 de_wiki
   1873122   43538807  316189253 europarl
    368584    5425504   38867347 tagesschau_news
 102528682 1305864989 9008424100 total
```
