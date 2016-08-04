from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from glob import glob
import os
import requests
import time

everyParams = [
        'SCORE',          # 점수
        'CNT',            # 플레이 횟수
        'WIN',            # 승리 횟수
        'LOSE',           # 패배 횟수
        'KILL',           # 총 킬수
        'DEATH',          # 총 데스수
        'KD',             # 총 킬뎃
        'AVG_KILL',       # 경기당 평균킬수
        'AVG_DEATH',      # 경기당 평균데스수
        'AVG_DEAL',       # 경기당 평균 딜량
        'AVG_HEAL',       # 경기당 평균 힐량
        'PLAYTIME',       # 플레이 시간
        'AVG_FIRE',       # 평균 폭주 시간
        'AVG_MSN',        # 평균 임무 기여 시간
        'AVG_MKILL',      # 평균 임무 기여 처치
        'CARD',           # 칭찬카드
        'MEDAL',          # 전체 메달
        'GOLD',           # 금메달
        'SILVER',         # 은메달
        'BRONZE',         # 동메달
        'ATK_CNT',
        'ATK_WIN',
        'ATK_LOSE',
        'ATK_KILL',
        'ATK_DEATH',
        'ATK_KD',
        'ATK_AVG_DEAL',
        'ATK_AVG_HEAL',
        'ATK_PLAYTIME',
        'ATK_AVG_FIRE',
        'ATK_AVG_MSN',
        'DEF_CNT',
        'DEF_WIN',
        'DEF_LOSE',
        'DEF_KILL',
        'DEF_DEATH',
        'DEF_KD',
        'DEF_AVG_DEAL',
        'DEF_AVG_HEAL',
        'DEF_PLAYTIME',
        'DEF_AVG_FIRE',
        'DEF_AVG_MSN',
        'TANK_CNT',
        'TANK_WIN',
        'TANK_LOSE',
        'TANK_KILL',
        'TANK_DEATH',
        'TANK_KD',
        'TANK_AVG_DEAL',
        'TANK_AVG_HEAL',
        'TANK_PLAYTIME',
        'TANK_AVG_FIRE',
        'TANK_AVG_MSN',
        'HEAL_CNT',
        'HEAL_WIN',
        'HEAL_LOSE',
        'HEAL_KILL',
        'HEAL_DEATH',
        'HEAL_KD',
        'HEAL_AVG_DEAL',
        'HEAL_AVG_HEAL',
        'HEAL_PLAYTIME',
        'HEAL_AVG_FIRE',
        'HEAL_AVG_MSN',
        'HERO_1',         # 첫 번째로 많이 사용한 영웅
        'HERO_2',         # 두 번째로 많이 사용한 영웅
        'HERO_3',         # 세 번째로 많이 사용한 영웅
    ]

def strToSeconds(s):
    s = s.strip().rstrip()
    ls = s.split()
    ret = 0

    for lls in ls:
        h = lls.find('시간')
        m = lls.find('분')
        s = lls.find('초')
        if h != -1:
            ret += int(lls[:h]) * 3600
        if m != -1:
            ret += int(lls[:m]) * 60
        if s != -1:
            ret += int(lls[:s])

    return ret

def noComma(s):
    s = ''.join(str(s).strip().rstrip().split(','))
    try: s = int(s)
    except: s = '0'
    return s

def heroKoreanToEnglish(s):
    names = {
        '겐지': 'Genji',
        '한조': 'Hanzo',
        '리퍼': 'Reaper',
        '트레이서': 'Tracer',
        '맥크리': 'McCree',
        '파라': 'Pharah',
        '솔저: 76': 'Soldier76',
        '바스티온': 'Bastion',
        '정크랫': 'Junkrat',
        '메이': 'Mei',
        '토르비욘': 'Torbjorn',
        '위도우메이커': 'Widowmaker',
        'D.VA': 'DVa',
        '라인하르트': 'Reinhardt',
        '로드호그': 'Roadhog',
        '윈스턴': 'Winston',
        '자리야': 'Zarya',
        '아나': 'Ana',
        '루시우': 'Lucio',
        '메르시': 'Mercy',
        '시메트라': 'Symmetra',
        '젠야타': 'Zenyatta',
        }
    if s in names.keys(): return names[s]
    return ''

def crawl(param):
    try:
        folder, link = param
        filename = link.split('/')[-1]

        while True:
            try:
                req = requests.get(link)
                break
            except:
                print('trying again... ' + link)
                time.sleep(5)
        
        if not req.ok:
            with open('err.txt', 'a') as f:
                f.write(folder + '/' + link + '\n')
                return

        soup = bs(req.text, 'html.parser')

        d = dict()
        for param in everyParams:
            d[param] = '0'

        # 1.  SCORE           점수
        l = soup.find('dd', {'class':'avg_score'})
        try: d['SCORE'] = str(int(l.text))
        except: d['SCORE'] = 0

        l = soup.findAll('dl')
        for ll in l:
            lll = ll.find('dt')
            lllt = ''

            if lll:
                lllt = lll.text.rstrip().strip()

            if lllt == '승률':
                # 2.  CNT             플레이 횟수
                d['CNT'] = noComma(ll.find('dd').text.split()[0][:-1])
                # 3.  WIN             승리 횟수
                d['WIN'] = noComma(ll.find('dd').text.split()[1][:-1])
                # 4.  LOSE            패배 횟수
                d['LOSE'] = noComma(ll.find('dd').text.split()[2][:-1])

            if lllt == 'K/D':
                # 5.  KILL            총 킬수
                d['KILL'] = noComma(ll.find('dd').text.split()[0])
                # 6.  DEATH           총 데스수
                d['DEATH'] = noComma(ll.find('dd').text.split()[2])

            if lllt == '게임당 평균 K/D':
                kr = float(ll.find('dd').text.split()[0])
                dr = float(ll.find('dd').text.split()[3])
                # 7.  KD              총 킬뎃
                if dr != 0:
                    d['KD'] = '%.2f' % (kr/dr)
                else:
                    d['KD'] = '0'
                # 8.  AVG_KILL        경기당 평균킬수
                d['AVG_KILL'] = '%.2f' % kr
                # 9.  AVG_DEATH       경기당 평균데스수
                d['AVG_DEATH'] = '%.2f' % dr
            
            if lllt == '게임당 평균 딜량':
                # 10. AVG_DEAL        경기당 평균 딜량
                d['AVG_DEAL'] = noComma(ll.find('dd').text.split()[0])
            
            if lllt == '게임당 평균 힐량':
                # 11. AVG_HEAL        경기당 평균 힐량
                d['AVG_HEAL'] = noComma(ll.find('dd').text.split()[0])
            
            if lllt == '플레이 시간':
                # 12. PLAYTIME        플레이 시간
                d['PLAYTIME'] = str(strToSeconds(ll.find('dd').text))

            if lllt == '평균 폭주 시간':
                # 13. AVG_FIRE        평균 폭주 시간
                d['AVG_FIRE'] = str(strToSeconds(ll.find('dd').text))

            if lllt == '평균 임무 기여 시간':
                # 14. AVG_MSN         평균 임무 기여 시간
                d['AVG_MSN'] = str(strToSeconds(ll.find('dd').text))

            if lllt == '평균 임무 기여 처치':
                # 15. AVG_MKILL       평균 임무 기여 처치
                d['AVG_MKILL'] = str(ll.find('dd').text).strip().rstrip()

            if lllt == '칭찬카드':
                # 16. CARD            칭찬카드
                d['CARD'] = noComma(ll.find('dd').text)

            if lllt == '전체 메달':
                # 17. MEDAL           전체 메달
                d['MEDAL'] = noComma(ll.find('dd').text)

            if lllt == '금메달':
                # 18. GOLD            금메달
                d['GOLD'] = noComma(ll.find('dd').text)

            if lllt == '은메달':
                # 19. SILVER          은메달
                d['SILVER'] = noComma(ll.find('dd').text)

            if lllt == '동메달':
                # 20. BRONZE          동메달
                d['BRONZE'] = noComma(ll.find('dd').text)

        l = soup.find('div', {'class':'timeByRole'}).find('tbody').findAll('tr')
        for ll in l:
            titleName = ll.find('span', {'class': 'name'}).text

            if titleName == '공격': titleName = 'ATK'
            elif titleName == '수비': titleName = 'DEF'
            elif titleName == '돌격': titleName = 'TANK'
            elif titleName == '지원': titleName = 'HEAL'
            else: continue

            # WIN
            if not ll.find('div', {'class': 'wins progress-bar progress-bar-striped'}):
                d[titleName + '_WIN'] = 0
            else:
                d[titleName + '_WIN'] = ll.find('div', {'class': 'wins progress-bar progress-bar-striped'}).text.strip().rstrip()[:-1]

            # LOSE
            if not ll.find('div', {'class': 'loses progress-bar progress-bar-striped progress-bar-danger'}):
                d[titleName + '_LOSE'] = 0
            else:
                d[titleName + '_LOSE'] = ll.find('div', {'class': 'loses progress-bar progress-bar-striped progress-bar-danger'}).text.strip().rstrip()[:-1]

            # CNT
            d[titleName + '_CNT'] = int(d[titleName + '_WIN']) + int(d[titleName + '_LOSE'])

            # KILL
            if not ll.find('span', {'class': 'kills'}):
                d[titleName + '_KILL'] = '0'
            else:
                d[titleName + '_KILL'] = noComma(ll.find('span', {'class': 'kills'}).text)

            # DEATH
            if not ll.find('span', {'class': 'deaths'}):
                d[titleName + '_DEATH'] = '0'
            else:
                d[titleName + '_DEATH'] = noComma(ll.find('span', {'class': 'deaths'}).text)

            # KD
            if int(d[titleName + '_DEATH']) != 0:
                d[titleName + '_KD'] = '%.2f' % (int(d[titleName + '_KILL']) / int(d[titleName + '_DEATH']))
            else:
                d[titleName + '_KD'] = '0'

            # AVG_DEAL
            ll.find('td', {'class':'avg_deals'}).find('p').extract()
            d[titleName + '_AVG_DEAL'] = noComma(ll.find('td', {'class':'avg_deals'}).text)

            # AVG_HEAL
            ll.find('td', {'class':'avg_heals'}).find('p').extract()
            d[titleName + '_AVG_HEAL'] = noComma(ll.find('td', {'class':'avg_heals'}).text)

            # PLAYTIME
            d[titleName + '_PLAYTIME'] = strToSeconds(ll.find('td', {'class':'time_played'}).find('p', {'class':'text'}).text)

            # AVG_FIRE
            ll.find('td', {'class':'fire'}).find('p').extract()
            d[titleName + '_AVG_FIRE'] = strToSeconds(ll.find('td', {'class':'fire'}).text)

            # AVG_MSN
            ll.find('td', {'class':'objective'}).find('p').extract()
            d[titleName + '_AVG_MSN'] = strToSeconds(ll.find('td', {'class':'objective'}).text)
        
        # 65. HERO_1          첫 번째로 많이 사용한 영웅
        d['HERO_1'] = heroKoreanToEnglish(soup.find('tr', {'class':'heroBasic', 'data-id':'0'}).find('span', {'class':'name'}).text)

        # 66. HERO_2          두 번째로 많이 사용한 영웅
        d['HERO_2'] = heroKoreanToEnglish(soup.find('tr', {'class':'heroBasic', 'data-id':'1'}).find('span', {'class':'name'}).text)

        # 67. HERO_3          세 번째로 많이 사용한 영웅
        d['HERO_3'] = heroKoreanToEnglish(soup.find('tr', {'class':'heroBasic', 'data-id':'2'}).find('span', {'class':'name'}).text)

        # Write to file
        filename = 'out/' + folder + '/' + filename + '.out'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            for param in everyParams:
                if param != 'SCORE':
                    f.write('\t')
                f.write(str(d[param]))
        print(filename)
    except:
        with open('err.txt', 'a') as f:
            f.write(folder + '/' + link + '\n')

if __name__ == '__main__':
    params = []
    for links in glob('links/link*.txt'):
        folder = str(links).replace('/','.').split('.')[1]
        if not os.path.exists('out/' + folder):
            with open(links, 'r') as f:
                for link in f.readlines():
                    params.append((folder, 'http://overlog.gg' + link.rstrip().strip()))
        else:
            print(folder + ' exists')

    pool = Pool(16)
    pool.map(crawl, params)
