import requests
from bs4 import BeautifulSoup
from os import path
import csv
# import pandas as pd


url = 'https://www.espncricinfo.com/india/content/player/caps.html?country=6;class=1'


if path.isfile('player_list.html'):
    with open('player_list.html') as source:
        soup = BeautifulSoup(source, 'html.parser')
        print('file has been loaded from local')
else:
    source = requests.get(url).content
    soup = BeautifulSoup(source,'html.parser')

    # saving file on local, so we don't have download the html from the server
    html_file = open('player_list.html','w')
    html_file.write(soup.prettify())
    html_file.close()

    print('file loaded from server and html file has been saved on the local')

csv_file = open('player_list.csv','w')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(['sr_no', 'player_name',
                     'player_link', 'player_first_match', 'player_first_match_link'
                     ])

# df = pd.DataFrame(columns=['sr_no', 'player_name',
#                      'player_link', 'player_first_match', 'player_first_match_link'
#                      ])

for player_list in soup.find_all('li', class_='sep'):
    # player sr_no
    sr_no = player_list.find('li', class_='ciPlayerserialno').text
    sr_no = " ".join(sr_no.split())

    # player_name
    player_name = player_list.find('a', class_='ColumnistSmry').text
    player_name = " ".join(player_name.split())

    # player_link
    player_link_div = player_list.find('li', class_='ciPlayername')
    player_link = player_link_div.find('a', class_='ColumnistSmry')['href']
    player_link = " ".join(player_link.split())

    # first match against
    player_first_match = player_list.find('a', class_='ColumnistSmry').text
    player_first_match = " ".join(player_first_match.split())

    # first match link ColumnistSmry
    player_first_match_div = player_list.find('li', class_='ciPlayerplayed')
    player_first_match_link = player_first_match_div.find('a', class_='ColumnistSmry')['href']
    player_first_match_link = " ".join(player_first_match_link.split())

    csv_writer.writerow([sr_no, player_name,
                         player_link, player_first_match, player_first_match_link
                         ])
    # creating dataframe columns
    # df['sr_no'] = sr_no
    # df['player_name'] = player_name
    # df['player_link'] = player_link
    # df['player_first_match'] = player_first_match
    # df['player_first_match_link'] = player_first_match_link

csv_file.close()