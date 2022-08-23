# -*- coding: utf-8 -*-

# Copyright 2019 Language Technology, Universität Hamburg (author: Benjamin Milde)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

import multiprocessing as mp
import math

import spacy
import normalisierung

disable_pipeline = False
filter_exlude_zeichen = True
filter_satzzeichen = True
resplit_whitespace = True

# spacy config
nlp = spacy.load('de_core_news_sm')

if disable_pipeline:
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)

min_token_len = 1

satzzeichen = ',.?!:;<>()/\{}#"\'´`‚’‘_→[]~«»&+^|'

exlude_zeichen = '*/=→[]."'

subtitleList = []

def readFile(filename):
    print(f'read File: {filename}')
    content = []
    with open(filename, encoding='utf-8') as file:
        for line in file:
            if line.isspace():
                continue
            else:
                line = line.split('\n')
                for sentence in line:
                    if sentence:
                        content.append(sentence)
    return content

def writeFile(filename_out, text):
    print(f'write filename {filename_out}')
    text = ''.join(str(elem) for elem in text)
    with open(filename_out, 'w') as txt_out:
        txt_out.write(text)

def cleanup(texts):
    print('start cleanup process')
    results = []
    sen_num = 0
    lines_dropped = 0
    for text in texts:
        if text[-1] == '\n':
            text = text[:-1]

        text = text.replace('\t',' ')
        text = text.replace('\xa0',' ')

        if resplit_whitespace:
            text = ' '.join(text.split())

        text = text.replace('   ', ' ').replace('  ', ' ')

        #if disable_pipeline:
        #    text_sentences = nlp(text, disable=["tagger", "parser", "ner", "lemmatizer", "tokenizer"])        
        #else:
        #    text_sentences = nlp(text)
        #
            #for sentence in text_sentences.sents:
        normalized_sentence = normalisierung.text_normalization(text, tries=12)
            
            #if disable_pipeline:
            #    text_tokens = nlp(normalized_sentence, disable=["parser", "sentencizer", "lemmatizer"])
            #else:
            #    text_tokens = nlp(normalized_sentence)

        text_tokens = nlp(normalized_sentence, disable=["parser", "sentencizer", "lemmatizer"])

        # NE PROPN        proper noun
        # NNE PROPN       proper noun
        # NN  NOUN        noun, singular or mass
        
        lower_case_first = False

        #   print(text_tokens[0].tag_)

        if len(text_tokens) == 0:
            lines_dropped += 1
            continue

        try:
            if text_tokens[0].tag_ not in ["NE", "NNE", "NN"]:
                lower_case_first = True
        except:
            print("Warning could not retrieve tag!")

        if filter_satzzeichen:
            tokens = [token.text for token in text_tokens if token.text not in satzzeichen] #if (token.text != '\n' and token.text != ' ')]
            tokens = [token[:-1] if token and (token[-1] == '-') else token for token in tokens]
            tokens = [token[1:] if token and (token[0] == '-') else token for token in tokens]
        else:
            tokens = [token.text for token in text_tokens]

        if len(tokens) < min_token_len:
            lines_dropped += 1
            continue

        rejoined_text = ' '.join(tokens).strip()

        if filter_exlude_zeichen and any(character in exlude_zeichen for character in rejoined_text):
            lines_dropped += 1
            continue

        while '  ' in rejoined_text:
            rejoined_text = rejoined_text.replace('  ',' ')
        
        if rejoined_text == '':
            lines_dropped += 1
            continue

        if lower_case_first:
            rejoined_text = rejoined_text[0].lower() + rejoined_text[1:]

        if sen_num % 1000 == 0:
            print("At sentence:", sen_num)
            print(tokens)

        if rejoined_text and not rejoined_text.isspace():
            if not any(zeichen in rejoined_text for zeichen in satzzeichen):
                results.append(rejoined_text.replace(' \n','\n').replace('\n ','\n') + '\n')

        sen_num += 1
    print("Finished processing " + str(sen_num) + " sentences.")
    print("Dropped " + str(lines_dropped) + " sentences.")
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-p', '--processes', required=False, default=40, type=int)
    args = parser.parse_args()
    input_file = args.file
    output_file = args.output
    processes = args.processes

    # read file
    content = readFile(input_file)

    print(f'split the data in {processes} equal sized chunks')
    chunksize = math.ceil(len(content) / processes)
    chunks = [content[i: i+chunksize]
                for i in range(0,len(content), chunksize)]

    print('start processing')
    pool = mp.Pool(processes)
    subtitles = pool.imap(cleanup, chunks)

    # create a list of the results and write it to the file
    finishList = []
    for subtitle in subtitles:
        finishList.extend(subtitle)
    pool.close()
    writeFile(output_file, finishList)
    print('finish')
