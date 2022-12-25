install.packages("palmerpenguins")

install.packages("here")

require(palmerpenguins)
require(here)

penguins = data.frame(penguins)

mean(penguins$body_mass_g)

head(penguins)
boxplot(penguins$bill_depth_mm)

boxplot(bill_depth_mm ~ sex, data = penguins)

par(mfrow = c(1, 3))


boxplot(penguins$bill_depth_mm)
boxplot(bill_length_mm ~ sex, data = penguins)
coplot(body_mass_g ~ bill_length_mm | island, data = penguins, rows = 1)

png(filename = here("basic_histogram.png"), width = 800, height = 600)
hist(penguins$body_mass_g)
dev.off()
