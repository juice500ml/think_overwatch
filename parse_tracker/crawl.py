from bs4 import BeautifulSoup as bs
from multiprocessing import Pool, Lock
import time
import requests


def crawl_names(index):
    url = "https://overwatchtracker.com/leaderboards/pc/global/CompetitiveRank"
    url += "?page=%d&mode=1" % index

    print('Crawling %d...\n', index)

    while True:
        try:
            req = requests.get(url)
            break
        except:
            time.sleep(5)

    if not req.ok:
        with open('err_names.txt', 'a') as f:
            f.write(url + '\n')
            raise Exception('Response Error', 'While bsearching')

    soup = bs(req.text, 'html.parser')
    table = soup.find('table', {'class': 'table table-bordered table-striped'})
    tbody = table.find('tbody')

    if 'lock' in dir():
        for tr in tbody.find_all('tr'):
            a = tr.find('a', {'data-tooltip': 'notooltip'})
            if not a:
                continue
            lock.acquire()
            with open('links.txt', 'a') as f:
                f.write(a.text + '\t' + a['href'] + '\n')
            lock.release()
    else:
        print('No lock found at %d...\nRecording skipped.\n' % index)

    return len(tbody.find_all('tr'))


def __init_lock(l):
    global lock
    lock = l


# Search for last index
def bsearch_names(s=1, f=800):
    if s >= (f - 1):
        return s

    if crawl_names((s+f)//2) > 0:
        return bsearch_names((s+f)//2 + 1, f)
    else:
        return bsearch_names(s, (s+f)//2)


if __name__ == '__main__':
    index = bsearch_names()
    print('Searching through 1 ~ %d' % index)

    params = [i for i in range(1, index + 1)]
    pool = Pool(16, initializer=__init_lock, initargs=(Lock(),))
    pool.map(crawl_names, params)
