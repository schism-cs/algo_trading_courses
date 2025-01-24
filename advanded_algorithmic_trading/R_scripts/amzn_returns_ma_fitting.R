require(quantmod)

getSymbols("AMZN")

plot(Cl(AMZN))

amzn_ret = diff(log(Cl(AMZN)))
plot(amzn_ret)

amzn_ret.ma <- arima(x=amzn_ret, order = c(0,0,3))

acf(amzn_ret.ma$res[-1])