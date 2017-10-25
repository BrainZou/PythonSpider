import requests
from bs4 import BeautifulSoup
movie_name_list = []

def parse_html(html):
    soup = BeautifulSoup(html,'html.parser')
    movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div',attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None

def download_page(url):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'  
    }
    data = requests.get(url,headers=headers).content
    return data

def main():
    DOWNLOAD_URL = 'https://movie.douban.com/top250'
    while(DOWNLOAD_URL):
        movies,DOWNLOAD_URL = parse_html(download_page(DOWNLOAD_URL))
    print(movies)
if __name__ == '__main__':
    main()
