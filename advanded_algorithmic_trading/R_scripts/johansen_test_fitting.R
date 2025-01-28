# Testing the cointegration of simialr equities: EWA, EWC and IGE

library("quantmod")

date_from <- "2006-04-26"
date_to <- "2012-04-09"

# Downloading the historical data
getSymbols("EWA", from = date_from, to = date_to)
getSymbols("EWC", from = date_from, to = date_to)
getSymbols("IGE", from = date_from, to = date_to)

ewa_adj <- unclass(EWA$EWA.Adjusted)
ewc_adj <- unclass(EWC$EWC.Adjusted)
ige_adj <- unclass(IGE$IGE.Adjusted)

# Performing Johansen test on series

joh_test <- ca.jo(data.frame(ewa_adj, ewc_adj, ige_adj),
                  type = "trace", K = 2,
                  ecdet = "none", spec = "longrun")

summary(joh_test)