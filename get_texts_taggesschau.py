import requests
import time

from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup as soup

base_url =  "https://www.tagesschau.de/"

link = "https://www.tagesschau.de/archiv/meldungsarchiv100~_date-<date>.html"

output_file = 'tagesschau_news_may19_may20.txt'
compteted_dates_file = 'tagesschau_news_may19_may20_completed.log'

sleep_time = 1

replace_rules = [('<strong>',''), ('</strong>',''), ('<i>',''), ('</i>',''), ('<em>',''), ('</em>',''), ('<span class="stand">',""), ('<span>',''), ('</span>',''), ('<i>',''), ('</i>','')]

with open(output_file, 'w') as output_f, open(compteted_dates_file, 'w') as completed_f:
    got_text = False
    for i in range(1,365):
        print('Sleep '+str(sleep_time)+' seconds...')
        time.sleep(sleep_time)
        date = date.today() + timedelta(days=-i)
        datestr = str(date).replace('-','')

        request_link = link.replace('<date>', datestr)

        print('GET', request_link)

        try:
            page_html = requests.get(request_link)
        except:
            print('Error retrieving:', request_link)
            completed_f.write(str(date) + ' fail ' + request_link +'\n')
            continue


        page_soup = soup(page_html.text, "lxml")

        for li in page_soup.findAll('li'):
            if 'Uhr' in str(li):
                link_to_fetch = str(list(li.findAll('a', href=True))[0]['href'])

                if link_to_fetch[0] == '/':
                    link_to_fetch = base_url + link_to_fetch

                print('GET', link_to_fetch)

                try:
                    link_html = requests.get(link_to_fetch)
                except:
                    print('Error retrieving:', link_to_fetch)
                    completed_f.write(str(date) + ' fail ' + link_to_fetch +'\n')
                    continue

                link_soup = soup(link_html.text, "lxml")

                for p in link_soup.find_all('p', class_='text'):
                    pc = str(p.getText()).strip()

                    for rule in replace_rules:
                        pc = pc.replace(rule[0], rule[1])

                    if len(pc) > 0:
                        got_text = True
                        output_f.write(pc + '\n')
                        print('Added text of len:', len(pc))
        
        if got_text:
            completed_f.write(str(date) + ' success' +'\n')
        else:
            completed_f.write(str(date) + ' fail' +'\n')
