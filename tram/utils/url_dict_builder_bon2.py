from bs4 import BeautifulSoup
import json
from requests import get

TRAM_FILE = '/Users/isakdrougge/Desktop/Skola/Advanced-Python/labs-advPyth/data/tramnetwork.json'


with open(TRAM_FILE, 'r') as openfile:
    loadedFile = json.load(openfile)

stops_to_look_for = loadedFile['stops']

stop_list_site = get('https://www.vasttrafik.se/reseplanering/hallplatslista/').text

soup = BeautifulSoup(stop_list_site, 'html.parser')
print(soup)
stop_and_id = {}

# url_list = [link.get('href')]
for link in soup.find_all('a'):

    link_paragraph = link.text.split()
    link_id = [int(number) for number in link.get('href').split('/') if number.isnumeric()]

    stop_name = []
    for word in link_paragraph:
        if word == 'Göteborg,' or word == 'Mölndal,':
            break
        elif 'Göteborg,' in link_paragraph or 'Mölndal,' in link_paragraph:
            stop_name.append(word.replace(",",""))
    
    if stop_name != []:
        print(stop_name)

    if stop_name != [] and " ".join(stop_name) in stops_to_look_for:
        try:
            stop_and_id[" ".join(stop_name)] = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid=' + str(link_id[0])
        except:
            pass
    



# try:
#     with open('/Users/isakdrougge/Desktop/Skola/Advanced-Python/labs-advPyth/Lab3/tram/utils/tramstop_google_url.json', "x") as f:
#         f.write(json.dumps(stop_and_id, indent=2))
# except FileExistsError:
#     x = input("File already exists, do you want to delete and create a new one? (y or n)")
#     if x == "y":
#         import os
#         os.remove('/Users/isakdrougge/Desktop/Skola/Advanced-Python/labs-advPyth/Lab3/tram/utils/tramstop_google_url.json')
#     with open('/Users/isakdrougge/Desktop/Skola/Advanced-Python/labs-advPyth/Lab3/tram/utils/tramstop_google_url.json', "x") as f:
#         f.write(json.dumps(stop_and_id, indent=2))