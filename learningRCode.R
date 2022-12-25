a <- "Antonio Escallon"
b1 <- 45.6
b2 <- "45.6"
c1 <- c(0, 1, 2, 3)

v1 <- c(- 2, -1, 0, 1, 2)

v2 <- 3*v1

v3 <- sum(v2, na.rm = F)

vec_4 <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

mat_1 <- matrix(data = vec_4, nrow = 3, ncol = 4, byrow = T)

print(mat_1)

mat_2 <- matrix(data = vec_4, nrow = 3, ncol = 4)

print(mat_2)

my_list_1 <- c(5.2, "five point two", c(0, 1, 2, 3, 4, 5))

names(my_list_1) <- c("two", "one", "three")

my_list_1[['three']]

my_list_1[['one']]

my_vec = rep(1:3, 5)
my_vec

my_bool_vec <- my_vec == 3

data.frame(my_vec, my_bool_vec)

my_vec[my_bool_vec == T]

