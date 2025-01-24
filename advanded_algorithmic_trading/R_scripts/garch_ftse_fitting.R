require(quantmod)
getSymbols("^FTSE")

ftrt = diff(log(Cl(FTSE)))

ft <- as.numeric(ftrt)
ft <- ft[!is.na(ft)]

plot(ft, type="line")

# ft_final.aic <- Inf
# ft_final.order <- c(0,0,0)
# 
# for (p in 1:4) for (d in 0:1) for (q in 1:4) {
#   arima_test = arima(ft, order=c(p,d,q))
#   ft_current.aic = AIC(arima_test)
#   if (ft_current.aic < ft_final.aic) {
#     ft_final.aic <- ft_current.aic
#     ft_final.order <- c(p,d,q)
#     ft_final.arima = test_arima
#   }
# }
# 
# ft_final.order

arima_test = arima(ft, order=c(4,0,3))

acf(resid(ft_final.arima), na.action = na.omit)

acf(resid(ft_final.arima)^2, na.action = na.omit)

ft.garch <- garch(ft, trace=F)
ft.res <- ft.garch$res[-1]

acf(ft.res)
acf(ft.res^2)