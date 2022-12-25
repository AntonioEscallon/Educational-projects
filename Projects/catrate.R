require("here")

data_dir = here(
  "data")

dat_catrate <- data.frame(read.csv(here("data","catrate.csv")))

head(dat_catrate)

summary(dat_catrate)

hist(dat_catrate$cat.rate, main="Salamander Reproduction Catastrophic Rates", xlab="Catastorphic Rate")

shapiro.test(dat_catrate$cat.rate)

t.test(dat_catrate$cat.rate,mu= 0.2857143)

wilcox.test(dat_catrate$cat.rate, mu = 2 / 7)

require(palmerpenguins)

penguin_dat = droplevels(subset(penguins, species != "Gentoo"))

summary(penguin_dat)

boxplot(
  flipper_length_mm ~ species, 
  data = penguin_dat,
  ylab = "Flipper Length (mm)")
penguin_dat$species
dat_ade= subset(penguin_dat, species == "Adelie")
dat_chi = subset(penguin_dat, species == "Chinstrap") 
shapiro.test(dat_ade$flipper_length_mm)
shapiro.test(dat_chi$flipper_length_mm)

par(mfrow = c(1,2))


hist(dat_ade$flipper_length_mm, main="Normal Distribution of Flipper Length Ade", xlab="Flipper Length")
hist(dat_chi$flipper_length_mm, main="Normal Distribution of Flipper Length Chi", xlab="Flipper Length")

t.test(data = dat_adeloe, alternative="greater" ,mu= 0.2857143)

t.test(penguin_dat$flipper_length_mm ~ penguin_dat$species, mu =0)
levels(penguin_dat$species)
t.test(dat_ade~dat_chi, alternative = c('greater'), mu =0)
