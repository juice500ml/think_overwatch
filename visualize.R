library(dplyr)
library(ggplot2)

# Load data from URL
dat = read.csv('parse_tracker/overwatch.data.csv')
names(dat) <- c('LEVEL','RATING','KILL_PER_MIN','KILL_PER_GAME','HEAL_PER_MIN','HEAL_PER_GAME','DMG_PER_MIN','DMG_PER_GAME','TOT_SOLO_KILL','TOT_OBJ_KILL','TOT_BLOW','TOT_DMG','TOT_KILL','TOT_ENV_KILL','TOT_MUL_KILL','TOT_DEATH','TOT_ENV_DEATH','TOT_WIN','TOT_GAME','TOT_FIRE_TIME','TOT_OBJ_TIME','TOT_TIME','TOT_ASSIST','TOT_HEAL_ASSIST','TOT_DEF_ASSIST','TOT_ATK_ASSIST','BEST_KILL','BEST_BLOW','BEST_DMG','BEST_HEAL','BEST_DEF_ASSIST','BEST_ATK_ASSIST','BEST_OBJ_KILL','BEST_OBJ_TIME','BEST_SOLO_KILL','BEST_FIRE_TIME','TOT_CARD','TOT_MEDAL','TOT_GOLD_MEDAL','TOT_SILVER_MEDAL','TOT_BRONZE_MEDAL','BEST_HERO','BEST_HERO_WIN','BEST_HERO_LOSE')

dat %>%
  ggplot(aes(x=RATING)) +
  ggtitle('Overwatch Rating Counts') +
  geom_histogram(bins=30)

qqline(dat$RATING)

# Who chose this hero?
dat %>%
  group_by(BEST_HERO) %>%
  mutate(count=n()) %>%
  ggplot(aes(x=reorder(BEST_HERO, count, y=count))) +
  ggtitle('Overwatch Heroes') +
  geom_bar() +
  coord_flip() +
  ylab("Hero Chosen") +
  xlab("Number of People")

# Blizzard is great at game-matching!
dat %>%
  sample_n(1000) %>%
  ggplot(aes(x=log2(TOT_KILL), y=log2(TOT_DEATH))) +
  geom_jitter() + 
  geom_smooth() +
  ggtitle("Total Kills per Death") +
  xlab("Total kills while Playing") +
  ylab("Total deaths while playing")

cor(dat$TOT_KILL, dat$TOT_DEATH)

# 1st Picks per Classes
dat %>%
  filter(BEST_HERO == "Soldier: 76" | BEST_HERO == "Genji" | BEST_HERO == "Tracer" | BEST_HERO == "McCree" | BEST_HERO == "Pharah" | BEST_HERO == "Reaper") %>%
  ggplot(aes(x=RATING, fill=BEST_HERO, alpha=.1)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Offense Heroes 1st Pick")
dat %>%
  filter(BEST_HERO == "Torbjörn" | BEST_HERO == "Widowmaker" | BEST_HERO == "Mei" | BEST_HERO == "Junkrat" | BEST_HERO == "Bastion" | BEST_HERO == "Hanzo") %>%
  ggplot(aes(x=RATING, fill=BEST_HERO, alpha=.1)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Defense Heroes 1st Pick")
dat %>%
  filter(BEST_HERO == "D.Va" | BEST_HERO == "Reinhardt" | BEST_HERO == "Roadhog" | BEST_HERO == "Winston" | BEST_HERO == "Zarya") %>%
  ggplot(aes(x=RATING, fill=BEST_HERO, alpha=.1)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Tank Heroes 1st Pick")
dat %>%
  filter(BEST_HERO == "Ana" | BEST_HERO == "Lúcio" | BEST_HERO == "Mercy" | BEST_HERO == "Symmetra" | BEST_HERO == "Zenyatta") %>%
  ggplot(aes(x=RATING, fill=BEST_HERO, alpha=.1)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Support Heroes 1st Pick")
dat %>%
  ggplot(aes(x=RATING, fill=BEST_HERO, alpha=.1)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Heroes 1st Pick")

dat %>%
  sample_n(3000) %>%
  mutate(IS_HEALER = (BEST_HERO == "Mercy" | BEST_HERO == "Lúcio")) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=IS_HEALER, alpha=.1)) +
  geom_point() + 
  xlim(20, 80) +
  ggtitle("Does Healers get more cards?")

#cut(rota2$age_mnth, 
#    breaks = c(-Inf, 6, 12, 24, 60, 167, Inf), 
#    labels = c("0-5 mnths", "6-11 mnths", "12-23 mnths", "24-59 mnths", "5-14 yrs", "adult"), 
#    right = FALSE)

dat %>%
  filter()