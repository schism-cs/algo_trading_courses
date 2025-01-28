set.seed(123)

z <- rep(0, 1000)

for (i in 2:1000) 
  z[i] <- z[i-1] + rnorm(1)

plot(z, type="l")

layout(1:2)
acf(z)
acf(diff(z))

x <- y <- rep(0, 1000)
x <- 0.3 * z + rnorm(1000)
y <- 0.6 * z + rnorm(1000)

layout(1:2)
plot(x, type="l")
plot(y, type="l")

comb <- 2*x - y

layout(1:2)
plot(comb, type="l")
acf(comb)

library("tseries")
adf.test(comb)

pp.test(comb)

po.test(cbind(2*x, -1.0*y))