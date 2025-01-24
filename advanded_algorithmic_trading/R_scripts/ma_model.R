set.seed(3)
x <- w <- rnorm(1000)
for (t in 4:1000) x[t] <- w[t] + 0.6 * w[t-1] + 0.4 * w[t-2] + 0.3 * w[t-3]

layout(1:2)
plot(x, type="l")
acf(x)

x.ma <- arima(x, order=c(0,0,3))
x.ma

0.6023 + c(-1.96, 1.96)*0.0827