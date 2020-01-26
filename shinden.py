import requests
from bs4 import BeautifulSoup
from time import sleep


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
    
    def __repr__(self):
        return '<Result "' + self.title + '" object>'


class Character(object):
    def __init__(self, name, gender, is_historical, url, image_url, appearance_list, description):
        self.name = name
        self.gender = gender
        self.is_historical = is_historical
        self.url = url
        self.image_url = image_url
        self.appearance_list = appearance_list
        self.description = description

    def __repr__(self):
        return '<Character "' + self.name + '" object>'

#gets all anime or manga results from first page of shinden search engine
def get_first_page_search(name, anime_or_manga = 'anime'):
    assert anime_or_manga in ['anime','manga']
    
    results = []
    name = str(name)
    if anime_or_manga == 'anime':
        url = base_url + 'series' + '?search=' + name.replace(' ','+')
    else:
        url = base_url + 'manga' + '?search=' + name.replace(' ','+')
    
    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)

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
        
        if anime_or_manga == 'anime':
            episodes = anime.find('li', {'class': 'episodes-col'})
        else:
            episodes = anime.find('li', {'class': 'chapters-col'})
        
        status = anime.find('li', {'class': 'title-status-col'})

        top_score = anime.find('li', {'class': 'rate-top'})

        image_url = anime.find('li', {'class': 'cover-col'}).find('a')['href']
        
        try:
            checked_top_score = float(top_score.text)
        except:
            checked_top_score = top_score.text
        title.text
        anime_type.text
        episodes.text
        status.text

        anime_object = Result(title.text, tags, rating_dict['ratings'], anime_type.text, episodes.text, status.text, checked_top_score, base_url + anime_url, base_url + image_url)
        
        results.append(anime_object)
    return results


def get_tags():
    url = base_url + '/series?'

    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)

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


# Searches shinden.pl for characters; search_type can be 'contains' or 'equals'
# depending on how we want to search using our keyword (name)
def search_characters(keyword, search_type = 'contains'):
    assert search_type == 'contains' or search_type == 'equals', 'Bad search type'
    character_list = []

    url = base_url + '/character?type=' + search_type + '&search=' + keyword.replace(' ','+')
    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')
    character_container = soup.find('section', {'class':'character-list'})
    characters = character_container.find_all('li',{'class':'data-view-list'})

    for character in characters:
        image_url = base_url + character.find('img')['src']
        name = character.find('h3',{'class':'title'}).text
        url = base_url + character.find('h3',{'class':'title'}).find('a')['href']
        info_str = character.find('p').text.replace(' ','')
        
        if 'female' in info_str:
            gender = 'female'
        elif 'male' in info_str:
            gender = 'male'
        else:
            gender = 'unspecified'
        if info_str[-3:] == 'tak':
            is_historical = True
        else:
            is_historical = False
        
        appearance_list = []
        appearance_container = character.find('ul',{'class':'data-view-list'})
        appearances = appearance_container.find_all('li')
        
        for appear in appearances:
            appearance_list.append(appear.text.replace(',',''))
        appearance_list = (list(dict.fromkeys(appearance_list)))

        sleep(0.2) # wait a bit before another request
        description = get_character_description(url)

        character_object = Character(name, gender, is_historical, url, image_url,appearance_list,description)
        character_list.append(character_object)
        print(character_object)
    return(character_list)


def get_character_description(url):
    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        description_box = soup.find_all('table',{'class':'data-view-table'},limit=2)
        description = description_box[1].find_all('td',limit=2)[1].text
    except IndexError:
        return None
    
    return(description)