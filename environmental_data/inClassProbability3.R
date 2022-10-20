# Clear your R environment to make 
# sure there are no stray variables.

rm(list = ls())

pol_n_predation = 26
pol_n_no_predation = 184
pol_n_total = pol_n_no_predation + pol_n_predation
pol_predation_rate = pol_n_predation/pol_n_total
  
psd_n_predation = 25
psd_n_no_predation = 706
psd_n_total = psd_n_predation +  psd_n_no_predation
psd_predation_rate = psd_n_predation/psd_n_total

seed_predation_proportion = psd_predation_rate/pol_predation_rate

print(
  paste0(
    "The seed predation rate for Polyscias fulva is: ",
    round(pol_predation_rate, digits = 3))) 

print(
  paste0(
    "The seed predation rate for Pseudospondias microcarpa is: ",
    round(psd_predation_rate, digits = 3)))

x_bin = 0:6
y_bin_2 = dbinom(x_bin, size = 5, prob = 0.66)

barplot(
  height = y_bin_2,
  # the names to print with each bar:
  names.arg = x_bin,
  # Tells R to remove space between bars:
  space = 0,
  ylab = "Pr(x)",
  main = "Binomial: n = 6, p = 0.66")

x_bin= 0:6
y_bin_2= dbinom(x_bin, size=6, prob= 0)

y_bin_2 = pbinom(4, size = 6, prob = .67)

y_bin_2 = pbinom(4, size = 6, prob = .67, lower.tail = F)

y_bin_2 = pnorm(1, 0, 1)

pnorm(2, 0, 1) - pnorm(1, 0, 1) 

par(mfrow = c(1, 2))
y_cdf_1 = pnorm(x, mean = 0, sd = 1)
y_cdf_2 = pnorm(x, mean = 0, sd = 2)
y_cdf_3 = pnorm(x, mean = -2, sd = 1)
plot(y_cdf_1 ~ x, type = "l", ylab = "cumulative density", main = "Antonios CDF Plot")
lines(y_cdf_2 ~ x, type = "l", ylab = "cumulative density", lty = 'dotted')
lines(y_cdf_3 ~ x, type = "l", ylab = "cumulative density", lty = 'dashed')
n = 1000
x = seq(from = -6, to = 6, length.out = n)
y = dnorm(x, mean = 0, sd = 1)
y2 = dnorm(x, mean = 0, sd = 2)
y3 = dnorm(x, mean = -2, sd = 1)
plot(y ~ x, type = "l", ylab = "Probability Density", main = "Antonios PDF Plot")
lines(y2 ~ x, type = "l", ylab = "Probability Density", lty = 'dotted')
lines(y3 ~ x, type = "l", ylab = "Probability Density", lty = 'dashed')

par(mfrow = c(1,1))
x_bin = 0:6
y_bin_2 = dbinom(x_bin, size = 6, prob = 0.66)
barplot(
  height = y_bin_2,
  # the names to print with each bar:
  names.arg = x_bin,
  # Tells R to remove space between bars:
  space = 0,
  ylab = "Pr(x)",
  main = "Antonios Binomial Plot: n = 6, p = 2/3")

x = 0:20

barplot(
  dbinom(x, size = 20, prob = 0.1),
  names.arg = x, space = 0,
  main = "Binomial PMF: n = 20, p = 0.1",
  ylab = "Pr(x)", xlab = "x = n successes")

set.seed(12345)
sim_population = rbinom(n = 1000000, size = 20, prob = 0.1)

