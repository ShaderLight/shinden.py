# shinden.py  ![GitHub](https://img.shields.io/github/license/shaderlight/shinden.py)
bs4 based web scrapping api for shinden.pl


## Required libraries:
- BeautifulSoup4
- requests

## Usage

### Result
Results are returned using **Result** object with following attributes:
- **title**: the title of the series,
- **tags**: list of tags,
- **ratings**: dict of specific ratings,
- **type**: type of series,
- **episodes**: number of episodes,
- **status**: status of series (eg. ongoing, finished)
- **top_score**: overall score
- **url**: url to the shinden.pl page of the series
- **cover_url**: url to the cover image

### Example

Generating a list of **Result** objects based on first page of shinden search engine
```python
anime_list = get_first_page_search('alchemist')

#    [a list of Result objects]
```
Getting the title of the first result
```python
anime_list[0].title

#    "Fullmetal Alchemist" 
```
