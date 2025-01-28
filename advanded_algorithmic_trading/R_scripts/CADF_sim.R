library("tseries")

set.seed(123)

# Random Walk
z <- rep(0, 1000)
for (i in 2:1000)
  z[i] <- z[i-1] + rnorm(1)

# Simulated cointegrated ts
p <- q <- rep(0, 1000)
p <- 0.3 * z + rnorm(1000)
q <- 0.6 * z + rnorm(1000)

# Perform Linear Regression on ts
comb <- lm(p~q)
comb

# ADF test on LR residuals for stationarity
adf.test(comb$residuals, k=1)