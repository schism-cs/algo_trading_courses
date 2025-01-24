set.seed(1)
x <- w <- rnorm(100)
for (t in 2:100) x[t] <- 0.6 * x[t-1] + w[t]
layout(1:2)
plot(x, type="l")
acf(x)

x.ar <- ar(x, method="mle")
x.ar$order
x.ar$ar
x.ar$ar + c(-1.96, 1.96) * sqrt(x.ar$asy.var)