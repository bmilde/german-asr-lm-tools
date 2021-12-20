import os
import shutil
import re
import argparse
import multiprocessing
from bs4 import BeautifulSoup

subtitles = []

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', required=True, help='Directory of the subtitles (eg mediathek_subs/)')
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-p', '--processes', required=False, default=1, type=int, help='Number of processes')
args = parser.parse_args()
mediathek_subs = args.directory
filename_out = args.output
processes = args.processes

def extract_from_xmlfile(filename):
    with open(filename, encoding='utf-8') as infile:
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

    span_text = ''
    
    for elem in soup.findAll('tt:p'):
        line = ''
        for subelem in elem.findAll('tt:span'):
            line += ' ' + str(subelem.text).replace('\n','').replace('\r','').replace('\t',' ')
        line = re.sub(' +', ' ', line)
        line = line.strip() + '\n'
        if not line.lower().startswith('copyright'):
            if not line.lower().startswith('live-untertitelung'):
                if not line.lower().startswith('untertitel:'):
                    if not line.lower().startswith('untertitelung:'):
                        if not line == '.' and not line == '':
                            span_text += line
    return span_text

def write_to_file(filename_out):
    with open(filename_out, 'a') as out_file:
        for a in subtitles:
            out_file.write(a)

pool = multiprocessing.Pool(processes)

if os.path.isfile(filename_out):
    print('Exiting, file', filename_out, 'already exists!')
else:
    files = [os.path.join(mediathek_subs,f) for f in os.listdir(mediathek_subs) if os.path.isfile(os.path.join(mediathek_subs,f))]
    subtitles = pool.map(extract_from_xmlfile, files)
    write_to_file(filename_out)
    # for f in files:
    #     last_f = f.split('/')[-1]
    #     if last_f.isnumeric():
    #         extract_from_xmlfile(f)
    #         write_to_file(filename_out)
