from bs4 import BeautifulSoup as bs
from multiprocessing import Pool, Lock
import time
import requests

everyKey = """
LEVEL
RATING
KILL_PER_MIN
KILL_PER_GAME
HEAL_PER_MIN
HEAL_PER_GAME
DMG_PER_MIN
DMG_PER_GAME
TOT_SOLO_KILL
TOT_OBJ_KILL
TOT_BLOW
TOT_DMG
TOT_KILL
TOT_ENV_KILL
TOT_MUL_KILL
TOT_DEATH
TOT_ENV_DEATH
TOT_WIN
TOT_GAME
TOT_FIRE_TIME
TOT_OBJ_TIME
TOT_TIME
TOT_ASSIST
TOT_HEAL_ASSIST
TOT_DEF_ASSIST
TOT_ATK_ASSIST
BEST_KILL
BEST_BLOW
BEST_DMG
BEST_HEAL
BEST_DEF_ASSIST
BEST_ATK_ASSIST
BEST_OBJ_KILL
BEST_OBJ_TIME
BEST_SOLO_KILL
BEST_FIRE_TIME
TOT_CARD
TOT_MEDAL
TOT_GOLD_MEDAL
TOT_SILVER_MEDAL
TOT_BRONZE_MEDAL
BEST_HERO
BEST_HERO_WIN
BEST_HERO_LOSE
"""
everyKey = everyKey.split()


def clean_int(s):
    f = 0.0
    s = s.strip()

    # comma deletion
    s = ''.join(s.split(','))

    # day hour minute second
    try:
        for ss in s.split():
            if ss[-1] == 'd':
                f += int(ss[:-1]) * 60 * 60 * 24
            elif ss[-1] == 'h':
                f += int(ss[:-1]) * 60 * 60
            elif ss[-1] == 'm':
                f += int(ss[:-1]) * 60
            elif ss[-1] == 's':
                f += int(ss[:-1])
            else:
                f += float(ss)
    except ValueError:
        print('clean_int cannot understand', s)
        print('returning 0')
        return '0'

    # float value
    if f != int(f):
        return '%.2f' % f

    return str(int(f))


def crawl_names(url):
    while True:
        try:
            req = requests.get(url)
            break
        except:
            time.sleep(5)

    if not req.ok:
        print('Request Error: ' + url)

    row = dict()
    soup = bs(req.text, 'html.parser')
    div = soup.find('div', {'class': 'col-md-4 col-md-push-8'})

    if 'lock' in globals():
        # row = dict()
        for panel in div.find_all('div', {'class': 'panel panel-dark'}):
            heading = panel.find('div', {'class': 'panel-heading'})
            if not heading:
                continue

            title = heading.find('h2', {'class': 'panel-title'})
            if not title:
                continue
            if title.text == 'Level':
                span_value = panel.find(
                        'span',
                        {'class': 'value'})
                if not span_value:
                    continue

                row['LEVEL'] = span_value.text

            elif title.text == 'Skill Rating':
                span_value = panel.find(
                        'span',
                        {'class': 'value', 'style': 'font-size:30px;'})
                if not span_value:
                    continue

                row['RATING'] = span_value.text

            elif title.text == 'Performance':
                for div in panel.find_all('div', {'class': 'stat-item'}):
                    span_value = div.find(
                            'span',
                            {'class': 'value'})
                    span_name = div.find(
                            'span',
                            {'class': 'name'})
                    if not span_value or not span_name:
                        continue

                    key = '_PER_'
                    if span_name.text.find('Eliminations') != -1:
                        key = 'KILL' + key
                    elif span_name.text.find('Healing') != -1:
                        key = 'HEAL' + key
                    elif span_name.text.find('Damage') != -1:
                        key = 'DMG' + key

                    if span_name.text.find('Game') != -1:
                        key = key + 'GAME'
                    elif span_name.text.find('Min') != -1:
                        key = key + 'MIN'

                    row[key] = span_value.text

            elif title.text == 'Combat':
                for div in panel.find_all('div', {'class': 'stat-item'}):
                    span_value = div.find(
                            'span',
                            {'class': 'value'})
                    span_name = div.find(
                            'span',
                            {'class': 'name'})
                    if not span_value or not span_name:
                        continue

                    key = 'TOT'
                    if span_name.text.find('Blows') != -1:
                        key = key + '_BLOW'
                    elif span_name.text.find('Damage') != -1:
                        key = key + '_DMG'
                    elif span_name.text.find('Solo') != -1:
                        key = key + '_SOLO'
                    elif span_name.text.find('Objective') != -1:
                        key = key + '_OBJ'
                    elif span_name.text.find('Environmental') != -1:
                        key = key + '_ENV'
                    elif span_name.text.find('Multi') != -1:
                        key = key + '_MUL'

                    if span_name.text.find('Kills') != -1:
                        key = key + '_KILL'

                    if span_name.text.find('Eliminations') != -1:
                        key = key + '_KILL'

                    row[key] = span_value.text

            elif title.text == 'Deaths':
                for div in panel.find_all('div', {'class': 'stat-item'}):
                    span_value = div.find(
                            'span',
                            {'class': 'value'})
                    span_name = div.find(
                            'span',
                            {'class': 'name'})
                    if not span_value or not span_name:
                        continue

                    key = 'TOT'
                    if span_name.text.find('Environmental') != -1:
                        key = key + '_ENV'

                    if span_name.text.find('Deaths') != -1:
                        key = key + '_DEATH'

                    row[key] = span_value.text

            elif title.text == 'Game':
                for div in panel.find_all('div', {'class': 'stat-item'}):
                    span_value = div.find(
                            'span',
                            {'class': 'value'})
                    span_name = div.find(
                            'span',
                            {'class': 'name'})
                    if not span_value or not span_name:
                        continue

                    key = 'TOT'
                    if span_name.text.find('Won') != -1:
                        key = key + '_WIN'
                    elif span_name.text.find('Games') != -1:
                        key = key + '_GAME'
                    elif span_name.text.find('Fire') != -1:
                        key = key + '_FIRE'
                    elif span_name.text.find('Objective') != -1:
                        key = key + '_OBJ'

                    if span_name.text.find('Time') != -1:
                        key = key + '_TIME'

                    row[key] = span_value.text

            elif title.text == 'Assists':
                for div in panel.find_all('div', {'class': 'stat-item'}):
                    span_value = div.find(
                            'span',
                            {'class': 'value'})
                    span_name = div.find(
                            'span',
                            {'class': 'name'})
                    if not span_value or not span_name:
                        continue

                    key = 'TOT'
                    if span_name.text.find('Healing') != -1:
                        key = key + '_HEAL'
                    elif span_name.text.find('Defensive') != -1:
                        key = key + '_DEF'
                    elif span_name.text.find('Offensive') != -1:
                        key = key + '_ATK'

                    key = key + '_ASSIST'

                    row[key] = span_value.text

            elif title.text == 'Best':
                for div in panel.find_all('div', {'class': 'stat-item'}):
                    span_value = div.find(
                            'span',
                            {'class': 'value'})
                    span_name = div.find(
                            'span',
                            {'class': 'name'})
                    if not span_value or not span_name:
                        continue

                    key = 'BEST'
                    if span_name.text.find('Eliminations') != -1:
                        key = key + '_KILL'
                    elif span_name.text.find('Blows') != -1:
                        key = key + '_BLOW'
                    elif span_name.text.find('Damage') != -1:
                        key = key + '_DMG'
                    elif span_name.text.find('Healing') != -1:
                        key = key + '_HEAL'
                    elif span_name.text.find('Defensive') != -1:
                        key = key + '_DEF'
                    elif span_name.text.find('Offensive') != -1:
                        key = key + '_ATK'
                    elif span_name.text.find('Objective') != -1:
                        key = key + '_OBJ'
                    elif span_name.text.find('Solo') != -1:
                        key = key + '_SOLO'
                    elif span_name.text.find('Fire') != -1:
                        key = key + '_FIRE'

                    if span_name.text.find('Kills') != -1:
                        key = key + '_KILL'
                    elif span_name.text.find('Time') != -1:
                        key = key + '_TIME'
                    elif span_name.text.find('Assists') != -1:
                        key = key + '_ASSIST'

                    row[key] = span_value.text

            elif title.text == 'Match Awards':
                for div in panel.find_all('div', {'class': 'stat-item'}):
                    span_value = div.find(
                            'span',
                            {'class': 'value'})
                    span_name = div.find(
                            'span',
                            {'class': 'name'})
                    if not span_value or not span_name:
                        continue

                    key = 'TOT'
                    if span_name.text.find('Cards') != -1:
                        key = key + '_CARD'
                    elif span_name.text.find('Gold') != -1:
                        key = key + '_GOLD'
                    elif span_name.text.find('Silver') != -1:
                        key = key + '_SILVER'
                    elif span_name.text.find('Bronze') != -1:
                        key = key + '_BRONZE'

                    if span_name.text.find('Medals') != -1:
                        key = key + '_MEDAL'

                    row[key] = span_value.text

        div = soup.find('div', {'class': 'heroes'})
        if div:
            a = div.find('a')
            if a:
                row['BEST_HERO'] = a.text

            div_left = div.find('div', {'class': 'left-text'})
            if div_left:
                row['BEST_HERO_WIN'] = div_left.text[:-1]

            div_right = div.find('div', {'class': 'right-text'})
            if div_right:
                row['BEST_HERO_LOSE'] = div_right.text[:-1]

        output_str = str()
        error_str = str()
        for key in everyKey:
            if key in row:
                if key != 'BEST_HERO':
                    row[key] = clean_int(row[key])
                output_str += row[key] + ','
            else:
                output_str += ','
                error_str += 'Key %s not found while parsing %s\n' % (key, url)
        output_str = output_str[:-1]

        lock.acquire()
        with open('overwatch.data.csv', 'a') as f:
            f.write(output_str + '\n')
        if error_str.strip():
            print(error_str)
        lock.release()
    else:
        print('No lock found at %s...\nRecording skipped.\n' % url)


def __init_lock(l):
    global lock
    lock = l

if __name__ == '__main__':
    params = []

    try:
        with open('overwatch.response_error.log', 'r') as f:
            params += [s.strip() for s in f.readlines()]
            for i in range(len(params)):
                if len(params[i]) == 0:
                    del(params[i])
    except OSError:
        print('overwatch.response_error.log not found.')

    try:
        with open('overwatch.parse_error.log', 'r') as f:
            paramset = set()
            for s in f.readlines():
                s = s.strip()
                if not s:
                    continue
                s = s.split()
                if not s:
                    continue
                paramset.add(s[-1])
            params += list(paramset)
    except OSError:
        print('overwatch.parse_error.log not found.')

    pool = Pool(16, initializer=__init_lock, initargs=(Lock(),))
    pool.map(crawl_names, params)
