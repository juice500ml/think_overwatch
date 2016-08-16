library(dplyr)
library(ggplot2)

# Load data from URL
dat = tbl_df(read.csv('parse_tracker/overwatch.data.csv'))

hero_atk = c("Soldier: 76", "Genji", "Tracer", "McCree", "Pharah", "Reaper")
hero_def = c("Torbjörn", "Widowmaker", "Mei", "Junkrat", "Bastion", "Hanzo")
hero_tank = c("D.Va", "Reinhardt", "Roadhog", "Winston", "Zarya")
hero_heal = c("Ana", "Lúcio", "Mercy", "Symmetra", "Zenyatta")

set.seed(1608)

dat %>%
  ggplot(aes(x=RATING)) +
  ggtitle('Overwatch Rating Counts') +
  geom_histogram(bins=30)

qqnorm(dat$RATING)
qqline(dat$RATING)

# Who chose this hero?
dat %>%
  group_by(BEST_HERO) %>%
  mutate(count=n()) %>%
  ggplot(aes(x=reorder(BEST_HERO, count, y=count))) +
  ggtitle('Overwatch Heroes') +
  geom_bar() +
  coord_flip() +
  xlab("Hero Chosen") +
  ylab("Number of People")

# Blizzard is great at game-matching!
dat %>%
  filter(BEST_HERO %in% hero_heal) %>%
  sample_n(1000) %>%
  ggplot(aes(x=TOT_KILL, y=TOT_DEATH)) +
  geom_jitter() + 
  geom_smooth() +
  scale_x_log10() +
  scale_y_log10() +
  geom_abline() +
  ggtitle("Total Kills per Death")

cor(dat$TOT_KILL, dat$TOT_DEATH)

# 1st Picks per Classes
dat %>%
  filter(BEST_HERO %in% hero_atk) %>%
  ggplot(aes(x=RATING, fill=BEST_HERO)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Offense Heroes 1st Pick")
dat %>%
  filter(BEST_HERO %in% hero_def) %>%
  ggplot(aes(x=RATING, fill=BEST_HERO)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Defence Heroes 1st Pick")
dat %>%
  filter(BEST_HERO %in% hero_tank) %>%
  ggplot(aes(x=RATING, fill=BEST_HERO)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Tank Heroes 1st Pick")
dat %>%
  filter(BEST_HERO %in% hero_heal) %>%
  ggplot(aes(x=RATING, fill=BEST_HERO)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Support Heroes 1st Pick")
dat %>%
  mutate(BEST_HERO_CLASS =
    ifelse(BEST_HERO %in% hero_atk, "Offense",
           ifelse(BEST_HERO %in% hero_def, "Defence",
                  ifelse(BEST_HERO %in% hero_tank, "Tank", "Support")))
  ) %>%
  ggplot(aes(x=RATING, fill=BEST_HERO_CLASS)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("Heroes 1st Pick")
dat %>%
  mutate(IS_GTWH = BEST_HERO %in% c("Genji", "Tracer", "Widowmaker", "Hanzo")) %>%
  ggplot(aes(x=RATING, fill=IS_GTWH)) + 
  geom_density(position = "fill") +
  xlim(20, 80) +
  ggtitle("GTWH 1st Pick")

dat %>%
  mutate(IS_HEALER = (BEST_HERO == "Mercy" | BEST_HERO == "Lúcio")) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=IS_HEALER)) +
  geom_point(alpha=0.2) +
  geom_smooth() +
  xlim(20, 80) +
  ggtitle("Does Healers get more cards?")
dat %>%
  mutate(IS_GTWH = BEST_HERO %in% c("Genji", "Tracer", "Widowmaker", "Hanzo")) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=IS_GTWH)) +
  geom_point(alpha = 0.2) +
  geom_smooth() +
  xlim(20, 80) +
  ggtitle("Does GTWH get less cards?")
dat %>%
  filter(BEST_HERO %in% hero_atk) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=BEST_HERO)) +
  geom_point(alpha=0.1) +
  geom_line(method = "lm", formula = y ~ 0 + I(1/x) + I((x-1)/x), stat="smooth", size = 1, alpha = 1) +
  xlim(20, 80) +
  ylim(0, 1) +
  ggtitle("Which offense heroes get most cards?")
dat %>%
  filter(BEST_HERO %in% hero_def) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=BEST_HERO)) +
  geom_point(alpha=0.1) +
  geom_line(method = "lm", formula = y ~ 0 + I(1/x) + I((x-1)/x), stat="smooth", size = 1, alpha = 1) +
  xlim(20, 80) +
  ylim(0, 1) +
  ggtitle("Which defence heroes get most cards?")
dat %>%
  filter(BEST_HERO %in% hero_tank) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=BEST_HERO)) +
  geom_point(alpha=0.1) +
  geom_line(method = "lm", formula = y ~ 0 + I(1/x) + I((x-1)/x), stat="smooth", size = 1, alpha = 1) +
  xlim(20, 80) +
  ylim(0, 1) +
  ggtitle("Which tank heroes get most cards?")
dat %>%
  filter(BEST_HERO %in% hero_heal) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=BEST_HERO)) +
  geom_point(alpha=0.1) +
  geom_line(method = "lm", formula = y ~ 0 + I(1/x) + I((x-1)/x), stat="smooth", size = 1, alpha = 1) +
  xlim(20, 80) +
  ylim(0, 1) +
  ggtitle("Which support heroes get most cards?")
dat %>%
  mutate(BEST_HERO_CLASS =
           ifelse(BEST_HERO %in% hero_atk, "Offense",
                  ifelse(BEST_HERO %in% hero_def, "Defence",
                         ifelse(BEST_HERO %in% hero_tank, "Tank", "Support")))
  ) %>%
  ggplot(aes(x=RATING, y=TOT_CARD / TOT_GAME, color=BEST_HERO_CLASS)) +
  geom_point(alpha=0.1) +
  geom_line(method = "lm", formula = y ~ 0 + I(1/x) + I((x-1)/x), stat="smooth", size = 1, alpha = 1) +
  xlim(20, 80) +
  ylim(0, 1) +
  ggtitle("Which hero classes get most cards?")

dat %>%
  mutate(IS_HEALER = (BEST_HERO == "Mercy" | BEST_HERO == "Lúcio")) %>%
  filter(RATING > 20 & RATING < 80) %>%
  ggplot(aes(x=IS_HEALER, y=TOT_CARD / TOT_GAME)) +
  geom_boxplot() +
  ggtitle("Does Healers get more cards?")

dd <- dat %>%
  sample_n(3000) %>%
  mutate(IS_HEALER = (BEST_HERO == "Mercy" | BEST_HERO == "Lúcio"))
summary(lm(TOT_CARD/TOT_GAME ~ IS_HEALER, data=dd))

dat_each <- dat %>%
  filter(BEST_HERO == 'Soldier: 76') %>%
  select(BEST_KILL, - BEST_HERO)


for (hero in c(hero_atk)) {
  print(hero)
  dat_each <- dat %>%
    filter(BEST_HERO == hero) %>%
      transmute(KILL_PER_GAME,
                HEAL_PER_GAME,
                DMG_PER_GAME,
                AVG_SOLO_KILL = TOT_SOLO_KILL / TOT_GAME,
                AVG_OBJ_KILL = TOT_OBJ_KILL / TOT_GAME,
                AVG_BLOW = TOT_BLOW / TOT_GAME,
                AVG_DMG = TOT_DMG / TOT_GAME,
                AVG_KILL = TOT_KILL / TOT_GAME,
                AVG_ENV_KILL = TOT_ENV_KILL / TOT_GAME,
                AVG_MUL_KILL = TOT_MUL_KILL / TOT_GAME,
                AVG_DEATH = TOT_DEATH / TOT_GAME,
                AVG_ENV_DEATH = TOT_ENV_DEATH / TOT_GAME,
                AVG_FIRE_TIME = TOT_FIRE_TIME / TOT_GAME,
                AVG_OBJ_TIME = TOT_OBJ_TIME / TOT_GAME,
                AVG_HEAL_ASSIST = TOT_HEAL_ASSIST / TOT_GAME,
                AVG_DEF_ASSIST = TOT_DEF_ASSIST / TOT_GAME,
                AVG_ATK_ASSIST = TOT_ATK_ASSIST / TOT_GAME,
                RATING)
  
  hero_lm = lm(RATING ~ ., data = dat_each)
  hero_lm %>%
    ggplot(aes(.fitted, .resid)) +
    geom_point() +
    stat_smooth(method="loess") +
    geom_hline(yintercept=0, col="red", linetype="dashed") +
    xlab("Fitted values") +
    ylab("Residuals") +
    ggtitle(paste("Residual vs Fitted Plot of Linear Model of Hero", hero, sep = " "))
  print(summary(hero_lm))
}
