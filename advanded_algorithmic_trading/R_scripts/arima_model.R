set.seed(2)
x <- arima.sim(list(order=c(1,1,1), ar=0.6, ma=-0.5), n=1000)
plot(x)
x.arima <- arima(x, order = c(1,1,1))
x.arima
acf(resid(x.arima))

Box.test(resid(x.arima), lag=20, type = "Ljung-Box")