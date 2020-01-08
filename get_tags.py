import requests
from bs4 import BeautifulSoup

def get_tags():
    url = 'https://shinden.pl/series?'

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    tag_box = soup.find_all('div', {'class':'search-items tab-item'})

    genres = tag_box[0].find('ul', {'class':'genre-list'})
    target_groups = tag_box[1].find('ul', {'class':'genre-list'})
    entity = tag_box[2].find('ul', {'class':'genre-list'})
    place = tag_box[3].find('ul', {'class':'genre-list'})
    other_tags = tag_box[4].find('ul', {'class':'genre-list'})

    tag_list = {'genres': list(filter(None, genres.text.splitlines())), 'target_groups': list(filter(None, target_groups.text.splitlines())), 
        'entity': list(filter(None, entity.text.splitlines())), 'place': list(filter(None, place.text.splitlines())), 'other': list(filter(None, other_tags.text.splitlines()))}

    return (tag_list)