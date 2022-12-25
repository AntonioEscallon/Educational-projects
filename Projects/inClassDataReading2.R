require(palmerpenguins)
pairs(penguins)
require(here)



t.test(subset(penguins, species == "Gentoo")$flipper_length_mm)

t.test(
  x = subset(penguins, species == "Gentoo")$flipper_length_mm,
  mu = 218
)

t.test(
  x = subset(penguins, species == "Gentoo")$flipper_length_mm,
  mu = 218,
  alternative = "less"
)
t.test(flipper_length_mm ~ species, data = subset(penguins, species != "Chinstrap"))

par(mfrow = c(1, 1))
hist(penguins$body_mass_g, breaks = 80, main = "histogram of body mass", xlab = "body mass (g)")
plot(density(penguins$body_mass_g, na.rm = TRUE), main = "density plot of body mass")

require(palmerpenguins)
boxplot(body_mass_g ~ species, data = penguins)

dat_chinstrap = subset(penguins, species == "Chinstrap")
mean(dat_chinstrap$body_mass_g, na.rm = TRUE)

shapiro.test(dat_chinstrap$body_mass_g)

aggregate(body_mass_g ~ species, data = penguins, FUN = mean)

aggregate(
  body_mass_g ~ species,
  data = penguins,
  FUN = function(x) shapiro.test(x)$p.value)

fit_species = lm(body_mass_g ~ species, data = penguins)

summary(fit_species)

anova(fit_species)

fit_species = lm(body_mass_g ~ species, data = penguins)

summary(fit_species)

anova(fit_species)

boxplot(body_mass_g ~ species, data = penguins)

penguins_female = penguins[penguins$sex=="female",]
penguins_female2 = penguins_female[penguins_female$species == "Chinstrap",]
penguins_female3 <- data.frame(penguins_female2)
mean(penguins_female3$body_mass_g, na.rm=TRUE)

mean(penguins_female2$body_mass_g)


lm(body_mass_g ~ species, data = penguins_female2)

fit_additive = lm(body_mass_g ~ sex + species, data = penguins)

fit_interactive = lm(body_mass_g ~ sex+ species, data = penguins)

fit_both= lm(body_mass_g ~ sex * species, data = penguins)
summary(fit_both)

require(palmerpenguins)

labels =c("female \n Adelie", "male \n Adelie", "female \n Chinstrap", "male \n Chinstrap", "female \n Gentoo", "male \n Gentoo")

boxplot(body_mass_g ~ species + sex, data = penguins, names=labels)


lm(bill_length_mm ~ body_mass_g, data = penguins, names= c(penguins$sex, "/n" ,penguins$species))



pairs(penguins[, c("bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g")])

bird_sta <- data.frame(read.csv(here("data", "bird.sta.csv")))

hab_sta <- data.frame(read.csv(here("data", "hab.sta.csv")))

head(hab_sta)

pairs(hab_sta[,c("p.edge.1", "ba.con", "snag.l")])

hist(bird_sta$CBCH, xlab="Number of birds counted", breaks = 0:7 - 0.5)

