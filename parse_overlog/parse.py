from bs4 import BeautifulSoup as bs
import requests
from multiprocessing import Pool

def crawl(param):
    url, i = param
    while True:
        try:
            req = requests.get(url)
            break
        except:
            pass
    if not req.ok:
        with open('err.txt', 'a') as f:
            f.write(url + '\n')
            return
    soup = bs(req.text, 'html.parser')
    with open('link%04d.txt' % i, 'w') as f:
        for a in soup.find_all('a', {'class' : 'name'}):
            f.write(a['href'] + '\n')
    print(i)

if __name__ == '__main__':
    params = [('http://overlog.gg/leaderboards/global/rank/' + str(i), i) for i in range(1000, 6219)]
    pool = Pool(6)
    pool.map(crawl, params)
