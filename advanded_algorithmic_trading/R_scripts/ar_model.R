set.seed(1)
x <- w <- rnorm(100)
for (t in 3:100) x[t] <- -0.666 * x[t-1] - 0.333 * x[t-2] + w[t]
layout(1:2)
plot(x, type="l")
acf(x)

x.ar <- ar(x, method="mle")
x.ar$order
x.ar$ar

0.6023 + c(-1.96, 1.96)*0.0827
