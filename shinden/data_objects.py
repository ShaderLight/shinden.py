# an object used for returning anime or manga data
class Result(object):
    def __init__(self, title, tags, ratings, type_, episodes, status, top_score, url, cover_url, search_url):
        self.title = title
        self.tags = tags
        self.ratings = ratings
        self.type = type_
        self.episodes = episodes
        self.status = status
        self.top_score = top_score
        self.url = url
        self.cover_url = cover_url
        self.search_url = search_url
    
    def __repr__(self):
        return '<Result "' + self.title + '" object>'


# an object used for returning character data
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


# an object used for returning user data
# there is probably a better way to organise this
class User(object):
    def __init__(self, nickname, url, avatar_url, achievement_url, animelist_url, 
    mangalist_url, friend_list, registered_time_ago, last_seen, achievement_count, 
    points, average_anime_ratings, anime_rated, anime_minutes_watched, 
    anime_titles_watched, anime_episodes_watched, anime_episodes_rewatched, 
    recent_anime, average_manga_ratings, manga_rated, manga_minutes_read, 
    manga_titles_read, manga_chapters_read, manga_chapters_reread, recent_manga):

        # general stuff
        self.nickname = nickname
        self.url = url
        self.avatar_url = avatar_url
        self.achievement_url = achievement_url
        self.animelist_url = animelist_url
        self.mangalist_url = mangalist_url
        self.friend_list = friend_list
        self.registered_time_ago = registered_time_ago
        self.last_seen = last_seen
        self.achievement_count = achievement_count
        self.points = points

        # anime related stuff
        self.average_anime_ratings = average_anime_ratings
        self.anime_rated = anime_rated
        self.anime_minutes_watched = anime_minutes_watched
        self.anime_titles_watched = anime_titles_watched
        self.anime_episodes_watched = anime_episodes_watched
        self.anime_episodes_rewatched = anime_episodes_rewatched
        self.recent_anime = recent_anime

        # manga related stuff
        self.average_manga_ratings = average_manga_ratings
        self.manga_rated = manga_rated
        self.manga_minutes_read = manga_minutes_read
        self.manga_titles_read = manga_titles_read
        self.manga_chapters_read = manga_chapters_read
        self.manga_chapters_reread = manga_chapters_reread
        self.recent_manga = recent_manga

    def __repr__(self):
        return '<User "' + self.nickname + '" object>'
