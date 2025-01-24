library(forecast)
require(quantmod)

getSymbols("^GSPC", from="2022-01-01")
amzn = diff(log(Cl(GSPC)))

# Now finding the best ARIMA model, optimizing AIC

azfinal.aic <- Inf
azfinal.order <- c(0,0,0)

for (p in 1:4) for (d in 0:1) for (q in 1:4) {
  test_arima = arima(amzn, order=c(p,d,q))
  azcurrent.aic = AIC(test_arima)
  if (azcurrent.aic < azfinal.aic) {
    azfinal.aic <- azcurrent.aic
    azfinal.order <- c(p,d,q)
    azfinal.arima <- test_arima
  }
}

azfinal.order

acf(resid(azfinal.arima), na.action = na.omit)
Box.test(resid(azfinal.arima), lag=20, type = "Ljung-Box")

plot(forecast(azfinal.arima, h=25))