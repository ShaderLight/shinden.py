import requests
from bs4 import BeautifulSoup

def get_first_search(name, type_of_search = 'series'):
    name = str(name)
    url = 'https://shinden.pl/' + str(type_of_search) + '?search=' + name.replace(' ','+')
    
    r = requests.get(url)

    if r.status_code != 200:
        return "Error with status code: " + str(r.status_code)

    print(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')

    search_result_box = soup.find('section', class_='title-table')
    animes = search_result_box.find_all('ul', class_='div-row')

    anime_list=[]
    for anime in animes:
        tags=[]
        title = anime.find('h3')
        if title is None:
            continue
        anime_list.append(title.text)
        tag_buttons = anime.find_all('a', {'data-tag-id':True})
        for tag in tag_buttons:
            tags.append(tag.text)
        print(title.text)
        print(tags)
        print('\n')