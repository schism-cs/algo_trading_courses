library("urca")

set.seed(123)

z <- rep(0, 10000)

for (i in 2:10000) {
  z[i] <- z[i - 1] + rnorm(1)
}

p <- q <- r <- rep(0, 10000)

p <- 0.3 * z + rnorm(10000)
q <- 0.6 * z + rnorm(10000)
r <- 0.2 * z + rnorm(10000)

# Performing Johansen test on simulated cointegrated series

joh_test <- ca.jo(data.frame(p, q, r),
                  type = "trace", K = 2,
                  ecdet = "none", spec = "longrun")

summary(joh_test)

# From the summary, we can extract the following information:
# - Eigenvalues: we can find the highest eigenvalue, to select
#                the relative eigenvector
# - Test statistic: here we can evaluate the hypotesis for each possible rank
#                   If test > confidence interval, we can asses the strength
#                   of the hypotesis.
# - Eigenvectors: the components of the eigenvector with higest eigenvalue
#                 can be used as coefficients to create a stationary ts,
#                 as a linear combination of the original ts.

s <- 1.000 * p + 0.7065 * q + -3.6156 * q

plot(s, type = "line")

# Let's do an ADF test for stationarity

library("tseries")
adf.test(s)