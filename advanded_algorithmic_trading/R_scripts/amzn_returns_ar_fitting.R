require(quantmod)
layout(1:3)

getSymbols("AMZN")
AMZN
plot(Cl(AMZN))
amzn_ret = diff(log(Cl(AMZN)))
plot(amzn_ret)
acf(amzn_ret, na.action=na.omit)

amzn_ret.ar <- ar(amzn_ret, na.action=na.omit)
amzn_ret.ar$order
amzn_ret.ar$ar
amzn_ret.ar$asy.var
-0.0226 + c(-1.96, 1.96)*sqrt(2.2e-4)
-0.0410 + c(-1.96, 1.96)*sqrt(2.2e-4)