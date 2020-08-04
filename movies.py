import requests
from bs4 import BeautifulSoup

response = requests.get("https://movie.naver.com/movie/running/current.nhn")
soup = BeautifulSoup(response.text, 'html.parser')


movies_list = soup.select(
    '#content > .article > .obj_section > .lst_wrap > ul > li')
final_movie_data = []

for movie in movies_list:
    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0]
    movie_code = a_tag['href'].split('code=')[1]

    movie_data = {
        'title': movie_title,
        'code': movie_code
    }

    final_movie_data.append(movie_data)

print(final_movie_data)
