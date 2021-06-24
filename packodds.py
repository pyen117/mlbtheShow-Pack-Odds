from bs4 import BeautifulSoup
import requests
import csv
import uuid
requests.packages.urllib3.disable_warnings()

# Make sure you change the range function below to match the number of pages, I always do pages + 5 just in case


def get_cards(csv_file):
    headers = {
    'authority': 'mlb21.theshow.com',
    'sec-ch-ua': '^\\^',
    'accept': 'text/html, application/xhtml+xml',
    'turbolinks-referrer': 'https://mlb21.theshow.com/packs/open_pack_history^#',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://mlb21.theshow.com/packs/open_pack_history',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'tsn_hide_ribbon=1-1619213959; tsn_last_seen_roster_id=2; tsn_last_url=--CCFFYHBDZE06TDQk68hJ_-IxQblpnnntq3LUcuMDuwHG_gcSJghq6kTM9xZE0u70z9piO-A7ikVh1BRqA6bw^%^3D^%^3D; _tsn_session=e1ce8aa303becbab37d8f6159ad783b9; tsn_token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NTUwOTg2LCJ1c2VybmFtZSI6IllFTiBXSU5TX1hCTCIsInBpY3R1cmUiOiJodHRwczovL3RoZXNob3duYXRpb24tcHJvZHVjdGlvbi5zMy5hbWF6b25hd3MuY29tL2ZvcnVtX2ljb25zL2ljb25fYW5pbWFsc19kb2cucG5nIiwiZ3JvdXBzIjpbXX0.hQKyAbFMmKtnVBkloyLXFSd6j_4AryGPP0ubx3R8tno',}

    
    try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as csv_file:
                packfile = csv.DictWriter(csv_file, fieldnames=['pack type','pack id', 'date', 'url', 'item', 'type', 'rarity'])
                packfile.writeheader()
                for x in range(1, 35):
                    params = (('page', str(x) + '^'), ('', ''), )
                    print(params)
                    r = requests.get("https://mlb21.theshow.com/packs/open_pack_history", headers=headers, params=params,
                                                                                                         verify=False)
                    print(r.url)
                    pagetext = r.text
                    soup = BeautifulSoup(pagetext, 'html.parser')
                    details = {}

                    pack_meta = soup.find_all("div", class_="section-pack-history-secondary")
                    #print(pack_meta)
                    #pack_items = soup.find_all("tr")

                    for x in pack_meta:
                        pack_type = x.find('h3').text
                        date_opened = x.find('p').text[7:16]
                        pack_items = x.find_all('tr')
                        pack_id = uuid.uuid4()


                        for p in pack_items:
                            item_name = p.find('td')

                            a_tags = p.find('a', {'href': True})
                            if a_tags is not None:
                                if a_tags.has_attr('href'):
                                    ending = a_tags['href']
                                    url = 'https://theshownation.com' + ending
                                    details['url'] = url

                            if p.contents[3].text == 'Name':
                                pass
                            else:
                                name = p.contents[3].text.lstrip('\n\n').rstrip('\n\n')
                                details['item'] = name



                            if p.contents[5].text == 'Type':
                                pass
                            else:
                                i_type = p.contents[5].text


                            for img in p.find_all('img', class_='icons-rarity'):
                                image = img['src']
                                details['rarity'] = image
                                image = image.split('shield-')[1]
                                image = image.rsplit('.png')[0]
                                packfile.writerow({'pack type': pack_type, 'pack id': pack_id.hex, 'date': date_opened, 'url': url,
                                                     'item': name, 'type': i_type, 'rarity': image})

    except Exception as e:
                    print(e)


if __name__ == '__main__':
    get_cards('packHistory.csv')
