require(quantmod)
getSymbols("^FTSE")

ft_ret = diff(log(Cl(FTSE)))
plot(ft_ret)

ft <- as.numeric(ft_ret)
ft <- ft[!is.na(ft)]

ft_final.aic <- Inf
ft_final.order <- c(0,0,0)

for (p in 1:4) for (d in 0:1) for (q in 1:4) {
	ft_current.aic <- AIC(arima(ft, order=c(p,d,q)))
	if (ft_current.aic < ft_final.aic) {
		ft_final.aic <- ft_current.aic
		ft_final.order <- c(p,d,q)
		ft_final.arima <- arima(ft, order=c(p,d,q))
  	}
}

ft_final.order

acf(resid(ft_final.arima)^2)

ft.garch <- garch(ft, trace=F)
ft.res <- ft.garch$res[-1]

acf(ft.res)
acf(ft.res^2)