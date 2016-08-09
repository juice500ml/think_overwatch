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

if __name__ == '__main__':
    csvs = []
    outs = []

    try:
        with open('overwatch.data.csv', 'r') as f:
            csvs += [s.strip() for s in f.readlines()]
    except OSError:
        print('overwatch.data.csv not found.')

    for csv in csvs:
        csv = csv.split(',')
        if len(csv) != len(everyKey):
            print("Length doesn't match")
            print(csv)
            continue

        flag = False
        for i in range(len(everyKey)):
            if len(csv[i]) == 0:
                print("%d Element data is empty" % i)
                print(csv)
                flag = True
            if i != len(everyKey) - 3:
                try:
                    float(csv[i])
                except:
                    print("%d Element data type is wrong" % i)
                    print(csv)
                    flag = True
            if i == 1:
                try:
                    if int(csv[i]) == 0:
                        print("%d Element data is wrong" % i)
                        flag = True
                except:
                    print("%d Element data type is wrong" % i)
                    print(csv)
                    flag = True

        if flag:
            continue
        outs.append(','.join(csv))

    with open('overwatch.data.csv.clean', 'w') as f:
        for out in outs:
            f.write(out + '\n')
