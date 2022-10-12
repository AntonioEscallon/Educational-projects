require(palmerpenguins)
pairs(penguins)
require(here)

pairs(penguins[, c("bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g")])

bird_sta <- data.frame(read.csv(here("data", "bird.sta.csv")))

hab_sta <- data.frame(read.csv(here("data", "hab.sta.csv")))

head(hab_sta)

pairs(hab_sta[,c("p.edge.1", "ba.con", "snag.l")])

hist(bird_sta$CBCH, xlab="Number of birds counted", breaks = 0:7 - 0.5)

