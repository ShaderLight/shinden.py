from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
import requests

from shinden.data_objects import*

base_url = 'https://shinden.pl'


# gets all anime or manga results from first page of shinden search engine
# 'anime or manga' variable can be either 'manga' or 'anime' depending on what are we looking for 
def get_first_page_search(name, anime_or_manga = 'anime'):
    assert anime_or_manga in ['anime','manga']
    
    results = []
    name = str(name)
    # different request urls for different type of search
    if anime_or_manga == 'anime':
        url = base_url + '/series' + '?search=' + name.replace(' ','+')
    else:
        url = base_url + '/manga' + '?search=' + name.replace(' ','+')
    
    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code) # checking if the server responded without errors

    soup = BeautifulSoup(r.content, 'html.parser')

    # locating an element, where all the anime/manga results are shown
    search_result_box = soup.find('section', class_='title-table')
    animes = search_result_box.find_all('ul', class_='div-row')

    # iterating through results
    for anime in animes:
        tags=[]

        title = anime.find('h3')
        if title is None:
            continue

        anime_url = title.find('a')['href']

        tag_buttons = anime.find_all('a', {'data-tag-id':True})

        # collecting tags
        for tag in tag_buttons:
            tags.append(tag.text)

        rating_box = anime.find('li', {'class': 'ratings-col'})
        rating_dict = {}

        # ratings are divided into few categories
        # additionally, sometimes the ratings may not exist on the page, so we need to check if we can convert them to float
        spec_rating = rating_box.find('div', {'class': 'rating rating-total'})
        try:
            for t in spec_rating.text.split():
                try:
                    rating = float(t)
                except ValueError:
                    pass
        except AttributeError: # attempting to convert None type to float raises AttributeError
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

        # basic data about the result (although the variables often contain 'anime' word, it also works for manga)
        anime_type = anime.find('li', {'class': 'title-kind-col'})
        
        if anime_or_manga == 'anime':
            episodes = anime.find('li', {'class': 'episodes-col'})
        else:
            episodes = anime.find('li', {'class': 'chapters-col'})
        
        status = anime.find('li', {'class': 'title-status-col'})

        top_score = anime.find('li', {'class': 'rate-top'})

        image_url = anime.find('li', {'class': 'cover-col'}).find('a')['href']
        
        # we need to check top_score, because it sometimes can be a string (on the page), saying that there is no top score for that result
        try:
            checked_top_score = float(top_score.text)
        except:
            checked_top_score = top_score.text

        # creating Result object and passing all the data
        anime_object = Result(title.text[1:], tags, rating_dict['ratings'], anime_type.text, episodes.text, status.text, checked_top_score, base_url + anime_url, base_url + image_url)
        
        # appending new object to a list, that will be returned after the iteration
        results.append(anime_object)
    return results

# doesn't require any arguments, because it only scans available tags (located in the search filters)
def get_tags():
    url = base_url + '/series?'

    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')

    # locating tag containter on the page
    tag_box = soup.find_all('div', {'class':'search-items tab-item'})

    # splitting the tags into categories
    genres = tag_box[0].find('ul', {'class':'genre-list'})
    target_groups = tag_box[1].find('ul', {'class':'genre-list'})
    entity = tag_box[2].find('ul', {'class':'genre-list'})
    place = tag_box[3].find('ul', {'class':'genre-list'})
    other_tags = tag_box[4].find('ul', {'class':'genre-list'})

    # splitting the tags into elements on a list, each category has own list, additionally the tags are sorted alphabetically
    tag_dict = {'genres': list(filter(None, genres.text.splitlines())), 'target_groups': list(filter(None, target_groups.text.splitlines())), 
        'entity': list(filter(None, entity.text.splitlines())), 'place': list(filter(None, place.text.splitlines())), 'other': list(filter(None, other_tags.text.splitlines()))}

    return (tag_dict)


# Searches shinden.pl for characters; search_type can be 'contains' or 'equals'
# depending on how we want to search using our keyword (name)
# get_description allows to turn off making another request if we dont need description
def search_characters(keyword, search_type = 'contains', get_descriprion = True):
    assert search_type == 'contains' or search_type == 'equals', 'Bad search type'
    character_list = []

    url = base_url + '/character?type=' + search_type + '&search=' + keyword.replace(' ','+')
    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)

    # finding the character container box on the page and finding all the elements within it
    soup = BeautifulSoup(r.content, 'html.parser')
    character_container = soup.find('section', {'class':'character-list'})
    characters = character_container.find_all('li',{'class':'data-view-list'})

    # iteration through all the character elements
    for character in characters:
        # some basic data
        image_url = base_url + character.find('img')['src']
        name = character.find('h3',{'class':'title'}).text
        url = base_url + character.find('h3',{'class':'title'}).find('a')['href']
        info_str = character.find('p').text.replace(' ','')

        # checking gender
        if 'female' in info_str:
            gender = 'female'
        elif 'male' in info_str:
            gender = 'male'
        else:
            gender = 'unspecified'
        
        # checking if the character is historical
        if info_str[-3:] == 'tak':
            is_historical = True
        else:
            is_historical = False
        
        # getting the list of apperances of the character in the anime or manga
        appearance_list = []
        appearance_container = character.find('ul',{'class':'data-view-list'})
        appearances = appearance_container.find_all('li')
        
        for appear in appearances:
            appearance_list.append(appear.text.replace(',','')) # removing the unnecessary commas
        appearance_list = (list(dict.fromkeys(appearance_list))) # removing duplicates (if present)

        if get_descriprion:
            sleep(0.3) # wait a bit before another request, dont bully the server
            description = get_character_description(url)
        else:
            description = None

        # passing all the collected data to an object and appending it to the list
        character_object = Character(name, gender, is_historical, url, image_url, appearance_list, description)
        character_list.append(character_object)
    
    return(character_list)


# this function only collects the description of the character, used by search_character function
def get_character_description(url):
    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        description_box = soup.find_all('table',{'class':'data-view-table'},limit=2)
        description = description_box[1].find_all('td',limit=2)[1].text
    except IndexError: # if no description is present, it will raise an IndexError because there wont be enough elements
        return None
    
    return(description)


# searches for users, takes the keyword and search type
def search_users(keyword, search_type='contains'):
    assert search_type in ['contains', 'equals']
    url = base_url + '/users/?type=' + search_type + '&search=' + keyword.replace(' ','+')
    r = requests.get(url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)
    
    user_list = []
    soup = BeautifulSoup(r.content, 'html.parser')

    # getting the user container, where all searched users are
    user_container = soup.find('ul', {'class':'users-list'})
    users = user_container.find_all('li',{'class':'user-list-item'})

    # iterating through the users
    for user in users:
        nickname = user.find('h3',{'class':'title user-name'}).text
        url = base_url + user.find('a',{'class':'media-img'})['href']
        
        # if an user hadn't uploaded an avatar image, the default avatar shows up, and it is always hosted on 'gravatar.com' website
        # therefore it is unnecessary to add base url to it
        if 'gravatar.com' in user.find('img',{'class':'avatar-image av-size100x100'})['src']:
            avatar_url = user.find('img',{'class':'avatar-image av-size100x100'})['src']
        else:
            avatar_url = base_url + user.find('img',{'class':'avatar-image av-size100x100'})['src']
        
        # this isnt located on the search subpage, but still we are able to create urls to achievement, manga and anime lists based on the main profile url
        achievement_url = base_url + '/user' + url[23:] + '/achievements'
        animelist_url = base_url + '/animelist' + url[23:]
        mangalist_url = base_url + '/mangalist' + url[23:]

        # getting detailed data by requesting the user profile subpage
        sleep(0.3) # delaying subsequent requests
        info_dict = get_detailed_user_info(url)

        # passing all the data (a lot of data) to an User object and appending it to the list 
        user_object = User(nickname, url, avatar_url, achievement_url, animelist_url, 
        mangalist_url, info_dict['friend_list'], info_dict['registered_time_ago'], 
        info_dict['last_seen'], info_dict['achievement_count'], info_dict['points'], 
        info_dict['average_anime_ratings'], info_dict['anime_rated'], 
        info_dict['anime_minutes_watched'], info_dict['anime_titles_watched'], 
        info_dict['anime_episodes_watched'], info_dict['anime_episodes_rewatched'], 
        info_dict['recent_anime'], info_dict['average_manga_ratings'], 
        info_dict['manga_rated'], info_dict['manga_minutes_read'], 
        info_dict['manga_titles_read'], info_dict['manga_chapters_read'], 
        info_dict['manga_chapters_reread'], info_dict['recent_manga'])

        user_list.append(user_object)
    
    return(user_list)


# used by search_users function, needs extact user's profile url to make a request
def get_detailed_user_info(user_url):
    assert 'shinden.pl/user/' in user_url, 'Bad url'
    r = requests.get(user_url)
    assert r.status_code == 200, "Error with status code: " + str(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')
    info_dict = {} # dictionary with all collected data, returned at the end of this function
    
    # finding friend container and iterating through friends shown on the user's profile
    friend_list = []
    friend_container = soup.find('div',{'class':'friends'})
    for friend in friend_container.find_all('a',{'class':'avatar button-with-tip'}):
        friend_dict = {}
        friend_dict['nickname'] = friend['title']
        friend_dict['url'] = (base_url + friend['href'])
        friend_list.append(friend_dict)

    # finding general information about the user
    stats = soup.find('dl',{'class':'stats'})
    registered_time_ago = stats.find_all('span',{'class':'timeago'})[1]['title']
    registered_time_ago = datetime.strptime(registered_time_ago, '%Y-%m-%d %H:%M:%S')
    
    last_seen = stats.find_all('span',{'class':'timeago'})[0]['title']
    last_seen = datetime.strptime(last_seen, '%Y-%m-%d %H:%M:%S')
    
    achievement_count = int(soup.find('div',{'class':'achievements'}).find('span').text)
    
    points = int(stats.find_all('dd')[4].text)
    
    # finding anime stats, recent anime, time watched etc.
    anime_stats_section = soup.find('section',{'class':'push0 col6 box anime-stats'})

    average_anime_ratings = float(anime_stats_section.find('strong',{'class':'button-witch-tip'}).text)
    anime_rated = int(anime_stats_section.find('strong',{'class':'button-witch-tip'})['title'][16:])
    
    anime_minutes_watched = int(anime_stats_section.find('div',{'class':'total-time'}).find('strong')['title'][:-4])
    
    anime_titles_watched = int(soup.find('table',{'class':'data-view-table episodes'}).find_all('td')[1].text)
    anime_episodes_watched = int(soup.find('table',{'class':'data-view-table episodes'}).find_all('td')[3].text)
    anime_episodes_rewatched = int(soup.find('table',{'class':'data-view-table episodes'}).find_all('td')[5].text)
    
    recent_anime_box = soup.find('section',{'class':'push6 col6 box last-updates anime-updates'})

    recent_anime = []
    for result in recent_anime_box.find_all('div',{'class':'bd'}):
        anime_data = {}
        anime_name = result.find('a').text
        anime_url = base_url + result.find('a')['href']
        anime_status = result.find('span',{'class':'media-title-go'}).text.replace(' ','')

        anime_data['anime_name'] = anime_name
        anime_data['anime_url'] = anime_url
        anime_data['anime_status'] = anime_status

        recent_anime.append(anime_data)

    # basically the same as before but for manga
    manga_stats_section = soup.find('section',{'class':'push0 col6 box manga-stats'})

    average_manga_ratings = float(manga_stats_section.find('strong', {'class':'button-witch-tip'}).text)
    manga_rated = int(manga_stats_section.find('strong', {'class':'button-witch-tip'})['title'][16:])

    manga_minutes_read = int(manga_stats_section.find('strong', {'class':'button-with-tip'})['title'][:-4])

    manga_titles_read = int(soup.find('table',{'class':'data-view-table chapters'}).find_all('td')[1].text)
    manga_chapters_read = int(soup.find('table',{'class':'data-view-table chapters'}).find_all('td')[3].text)
    manga_chapters_reread = int(soup.find('table',{'class':'data-view-table chapters'}).find_all('td')[5].text)

    recent_manga_box = soup.find('section',{'class':'push6 col6 box'})

    recent_manga = []
    for result in recent_manga_box.find_all('div',{'class':'bd'}):
        manga_data = {}
        manga_name = result.find('a').text
        manga_url = base_url + result.find('a')['href']
        manga_status = result.find('span',{'class':'media-title-go'}).text.replace(' ','')

        manga_data['manga_name'] = manga_name
        manga_data['manga_url'] = manga_url
        manga_data['manga_status'] = manga_status

        recent_manga.append(manga_data)

    # finally collecting all the data within one dictionary
    # general user info
    info_dict['friend_list'] = friend_list
    info_dict['registered_time_ago'] = registered_time_ago
    info_dict['last_seen'] = last_seen
    info_dict['achievement_count'] = achievement_count
    info_dict['points'] = points

    # anime statistics
    info_dict['average_anime_ratings'] = average_anime_ratings
    info_dict['anime_rated'] = anime_rated
    info_dict['anime_minutes_watched'] = anime_minutes_watched
    info_dict['anime_titles_watched'] = anime_titles_watched
    info_dict['anime_episodes_watched'] = anime_episodes_watched
    info_dict['anime_episodes_rewatched'] = anime_episodes_rewatched
    info_dict['recent_anime'] = recent_anime

    # manga statistics
    info_dict['average_manga_ratings'] = average_manga_ratings
    info_dict['manga_rated'] = manga_rated
    info_dict['manga_minutes_read'] = manga_minutes_read
    info_dict['manga_titles_read'] = manga_titles_read
    info_dict['manga_chapters_read'] = manga_chapters_read
    info_dict['manga_chapters_reread'] = manga_chapters_reread
    info_dict['recent_manga'] = recent_manga

    return(info_dict)

# similar to get_first_page_search, except it get top ten titles by top score descending
def get_top_ten_titles(anime_or_manga = 'anime'):
    assert anime_or_manga in ['anime','manga']
    results = []

    if anime_or_manga == 'anime':
        url = base_url + '/series?sort_by=ranking-rate&sort_order=desc'
    else:
        url = base_url + '/manga?sort_by=ranking-rate&sort_order=desc'

    r = requests.get(url)

    assert r.status_code == 200, "Error with status code: " + str(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')

    # locating an element, where all the anime/manga results are shown
    search_result_box = soup.find('section', class_='title-table')
    animes = search_result_box.find_all('ul', class_='div-row')

    # iterating through results
    for anime in animes:
        tags=[]

        title = anime.find('h3')
        if title is None:
            continue

        anime_url = title.find('a')['href']

        tag_buttons = anime.find_all('a', {'data-tag-id':True})

        # collecting tags
        for tag in tag_buttons:
            tags.append(tag.text)

        rating_box = anime.find('li', {'class': 'ratings-col'})
        rating_dict = {}

        # ratings are divided into few categories
        # additionally, sometimes the ratings may not exist on the page, so we need to check if we can convert them to float
        spec_rating = rating_box.find('div', {'class': 'rating rating-total'})
        try:
            for t in spec_rating.text.split():
                try:
                    rating = float(t)
                except ValueError:
                    pass
        except AttributeError: # attempting to convert None type to float raises AttributeError
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

        # basic data about the result (although the variables often contain 'anime' word, it also works for manga)
        anime_type = anime.find('li', {'class': 'title-kind-col'})
        
        if anime_or_manga == 'anime':
            episodes = anime.find('li', {'class': 'episodes-col'})
        else:
            episodes = anime.find('li', {'class': 'chapters-col'})
        
        status = anime.find('li', {'class': 'title-status-col'})

        top_score = anime.find('li', {'class': 'rate-top'})

        image_url = anime.find('li', {'class': 'cover-col'}).find('a')['href']
        
        # we need to check top_score, because it sometimes can be a string (on the page), saying that there is no top score for that result
        try:
            checked_top_score = float(top_score.text)
        except:
            checked_top_score = top_score.text

        # creating Result object and passing all the data (title.text[1:] because there is always a blank space " " at the beginning for some reason)
        anime_object = Result(title.text[1:], tags, rating_dict['ratings'], anime_type.text, episodes.text, status.text, checked_top_score, base_url + anime_url, base_url + image_url)
        
        # appending new object to a list, that will be returned after the iteration
        results.append(anime_object)
    
    return results
