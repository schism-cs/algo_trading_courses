# Testing the cointegration of simialr equities: EWA, EWC and IGE
layout(1)

library("quantmod")

date_from <- "2011-01-01"
date_to <- "2024-12-31"

# Downloading the historical data
getSymbols("SPY", from = date_from, to = date_to)
getSymbols("IVV", from = date_from, to = date_to)
getSymbols("VOO", from = date_from, to = date_to)

spy_adj <- unclass(SPY$SPY.Adjusted)
ivv_adj <- unclass(IVV$IVV.Adjusted)
voo_adj <- unclass(VOO$VOO.Adjusted)

plot(spy_adj, type = "l",
     xlab = paste(date_from, "to", date_to),
     ylab = "SPY, IVV and VOO Backward-Adjusted Price", col = "blue")
par(new = TRUE)
plot(ivv_adj, type = "l", xlab = "", ylab = "", col = "green", axes = FALSE)
par(new = TRUE)
plot(voo_adj, type = "l", xlab = "", ylab = "", col = "red", axes = FALSE)
par(new = FALSE)

summary(spy_adj)

# Performing Johansen test on series

joh_test <- ca.jo(data.frame(spy_adj, ivv_adj, voo_adj),
                  type = "trace", K = 2,
                  ecdet = "none", spec = "longrun")

summary(joh_test)