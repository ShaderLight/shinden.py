import requests
from bs4 import BeautifulSoup

base_url = 'https://shinden.pl/'

class Result(object):
    def __init__(self, title, tags, ratings, type_, episodes, status, top_score, url, cover_url):
        self.title = title
        self.tags = tags
        self.ratings = ratings
        self.type = type_
        self.episodes = episodes
        self.status = status
        self.top_score = top_score
        self.url = url
        self.cover_url = cover_url

def get_first_page_search(name, type_of_search = 'series'):
    results = []
    name = str(name)
    url = base_url + str(type_of_search) + '?search=' + name.replace(' ','+')
    
    r = requests.get(url)

    if r.status_code != 200:
        return "Error with status code: " + str(r.status_code)

    print("Status code: " + str(r.status_code))

    soup = BeautifulSoup(r.content, 'html.parser')

    search_result_box = soup.find('section', class_='title-table')
    animes = search_result_box.find_all('ul', class_='div-row')

    for anime in animes:
        tags=[]
        title = anime.find('h3')
        if title is None:
            continue
        anime_url = title.find('a')['href']

        tag_buttons = anime.find_all('a', {'data-tag-id':True})

        for tag in tag_buttons:
            tags.append(tag.text)

        rating_box = anime.find('li', {'class': 'ratings-col'})
        rating_dict = {}

        spec_rating = rating_box.find('div', {'class': 'rating rating-total'})
        try:
            for t in spec_rating.text.split():
                try:
                    rating = float(t)
                except ValueError:
                    pass
        except AttributeError:
            rating = "None"
        
        rating_dict['ratings'] = {'total' : rating}

        spec_rating = rating_box.find('div', {'class': 'rating rating-story'})
        try:
            for t in spec_rating.text.split():
                try:
                    rating = float(t)
                except ValueError:
                 pass
        except AttributeError:
            rating = "None"
        
        rating_dict['ratings']['story'] = rating

        spec_rating = rating_box.find('div', {'class': 'rating rating-graphics'})
        try:
            for t in spec_rating.text.split():
                try:
                    rating = float(t)
                except ValueError:
                   pass
        except AttributeError:
            rating = "None"
        
        rating_dict['ratings']['graphics'] = rating

        spec_rating = rating_box.find('div', {'class': 'rating rating-music'})
        try:
            for t in spec_rating.text.split():
                try:
                    rating = float(t)
                except ValueError:
                    pass
        except AttributeError:
            rating = "None"
        
        rating_dict['ratings']['music'] = rating

        spec_rating = rating_box.find('div', {'class': 'rating rating-titlecahracters'})
        try:
            for t in spec_rating.text.split():
                try:
                    rating = float(t)
                except ValueError:
                    pass
        except AttributeError:
            rating = "None"
        
        rating_dict['ratings']['characters'] = rating

        anime_type = anime.find('li', {'class': 'title-kind-col'})
        
        episodes = anime.find('li', {'class': 'episodes-col'})

        status = anime.find('li', {'class': 'title-status-col'})

        top_score = anime.find('li', {'class': 'rate-top'})

        image_url = anime.find('li', {'class': 'cover-col'}).find('a')['href']
        
        try:
            true_top_score = float(top_score.text)
        except:
            true_top_score = top_score.text
        
        anime_object = Result(title.text, tags, rating_dict['ratings'], anime_type.text, episodes.text, status.text, true_top_score, base_url + anime_url, base_url + image_url)
        
        results.append(anime_object)
    return results

def get_tags():
    url = base_url + '/series?'

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

