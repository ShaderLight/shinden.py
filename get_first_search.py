import requests
from bs4 import BeautifulSoup

def get_first_search(name, type_of_search = 'series'):
    name = str(name)
    url = 'https://shinden.pl/' + str(type_of_search) + '?search=' + name.replace(' ','+')
    
    r = requests.get(url)

    if r.status_code != 200:
        return "Error with status code: " + str(r.status_code)

    print("Status code: " + str(r.status_code))

    soup = BeautifulSoup(r.content, 'html.parser')

    search_result_box = soup.find('section', class_='title-table')
    animes = search_result_box.find_all('ul', class_='div-row')

    anime_list={}
    for anime in animes:
        tags=[]
        title = anime.find('h3')
        if title is None:
            continue
        tag_buttons = anime.find_all('a', {'data-tag-id':True})

        for tag in tag_buttons:
            tags.append(tag.text)
        
        anime_list[title.text] = {'tags': tags}

        rating_box = anime.find('li', {'class': 'ratings-col'})


        spec_rating = rating_box.find('div', {'class': 'rating rating-total'})
        for t in spec_rating.text.split():
            try:
                rating = float(t)
            except ValueError:
                pass
        
        anime_list[title.text]['ratings'] = {'total' : rating}

        spec_rating = rating_box.find('div', {'class': 'rating rating-story'})
        for t in spec_rating.text.split():
            try:
                rating = float(t)
            except ValueError:
                pass
        
        anime_list[title.text]['ratings']['story'] = rating

        spec_rating = rating_box.find('div', {'class': 'rating rating-graphics'})
        for t in spec_rating.text.split():
            try:
                rating = float(t)
            except ValueError:
                pass
        
        anime_list[title.text]['ratings']['graphics'] = rating

        spec_rating = rating_box.find('div', {'class': 'rating rating-music'})
        for t in spec_rating.text.split():
            try:
                rating = float(t)
            except ValueError:
                pass
        
        anime_list[title.text]['ratings']['music'] = rating

        spec_rating = rating_box.find('div', {'class': 'rating rating-titlecahracters'})
        for t in spec_rating.text.split():
            try:
                rating = float(t)
            except ValueError:
                pass
        
        anime_list[title.text]['ratings']['characters'] = rating

        anime_type = anime.find('li', {'class': 'title-kind-col'})
        anime_list[title.text]['type'] = anime_type.text
        
        episodes = anime.find('li', {'class': 'episodes-col'})
        anime_list[title.text]['episodes'] = int(episodes.text)

        status = anime.find('li', {'class': 'title-status-col'})
        anime_list[title.text]['status'] = status.text

        top_score = anime.find('li', {'class': 'rate-top'})
        try:
            anime_list[title.text]['top_score'] = float(top_score.text)
        except ValueError:
            anime_list[title.text]['top_score'] = top_score.text
    
    return anime_list