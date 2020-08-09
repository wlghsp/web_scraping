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
    # split 사용하지 않고 가져오기
    # code = link[link.find('code=') + len('code='):]

    movie_data = {
        'title': movie_title,
        'code': movie_code
    }

    final_movie_data.append(movie_data)

# print(final_movie_data)

# select 간결하게 가져오기

# a_list = movie_code_soup.select(
#     'dl[class=lst_dsc] > dt > a')

# for a in a_list:
#     movie_title = a.text
#     movie_code = a['href'].split('code=')[1]
#     print(movie_code, ' ', movie_title)


headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=18847&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=WLRQQGYDCX7V4; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nx_ssl=2; page_uid=UyWxodp0YihssFqqSt8ssssstV4-500868; BMR=s=1596683670987&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Djosing616%26logNo%3D220744929196%26proxyReferer%3Dhttps%253A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; csrf_token=c6980166-7ad8-4e3a-8187-f8acb47abb73',
}


# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=18847&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=2', headers=headers)


for movie in final_movie_data:
    movie_code = movie['code']
    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get(
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    review_list = soup.select('body > div > div > div.score_result > ul > li')
    count = 0
    for review in review_list:
        score = review.select_one('div.star_score > em').text
        reple = ''

        # 일반적인 경우 먼저 처리 (일반적인 것을 먼저 처리하는 것이 효율적이다)
        if review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}') is None:
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count}').text.strip()
        # 리뷰가 긴 경우 처리
        elif review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}'):
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count} > span > a')['data-src']

        print(score, reple)

        count += 1
