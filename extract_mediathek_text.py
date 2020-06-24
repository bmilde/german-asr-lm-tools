import os
import shutil
from bs4 import BeautifulSoup

def extract_from_xmlfile(filename, filename_out):
    with open(filename) as infile:
        text = infile.read()

    if text.startswith('<!DOCTYPE html>'):
        print(filename,'is a html file.')
        print('Ignore', filename, 'move to removed/')
        if not os.path.exists('removed/'):
                os.makedirs('removed/')
        shutil.move(filename, 'removed/' + os.path.basename(filename))
        return

    print('Parsing:', filename)

    soup = BeautifulSoup(text, features='lxml')

    with open(filename_out, 'a') as out_file:
        for elem in soup.findAll('tt:p'):
            span_text = ''
#            print(elem.findAll('tt:span'))
            for subelem in elem.findAll('tt:span'):
                span_text += ' ' + str(subelem.text).replace('\n','').replace('\r','').replace('\t',' ')
            span_text = span_text[1:]
            span_text = span_text.replace('  ',' ')
            if not span_text.lower().startswith('copyright'):
                if not span_text.lower().startswith('live-untertitelung'):
                    if not span_text.lower().startswith('untertitel:'):
                        if not span_text == '.' and not span_text == '':
                            out_file.write(span_text.strip() + '\n')

filename_out = 'raw_text_subs3'
mediathek_subs = 'mediathek_subs/'

if os.path.isfile(filename_out):
    print('Exiting, file', filename_out, 'already exists!')
else:
    files = [os.path.join(mediathek_subs,f) for f in os.listdir(mediathek_subs) if os.path.isfile(os.path.join(mediathek_subs,f))]
    for f in files:
        last_f = f.split('/')[-1]
        if last_f.isnumeric():
            extract_from_xmlfile(f, filename_out)
