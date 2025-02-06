library("depmixS4")
library("quantmod")

set.seed(1)

# Main parameters for the two ts
Nk_lower <- 50
Nk_upper <- 150

bull_mean <- 0.1
bull_var <- 0.1

bear_mean <- -0.05
bear_var <- 0.2

# Create the list of durations for each regime
days <- replicate(5, sample(Nk_lower:Nk_upper, 1))

# Create the different bear and bull runs
market_bull_1 <- rnorm(days[1], bull_mean, bull_var)
market_bear_2 <- rnorm(days[2], bear_mean, bear_var)
market_bull_3 <- rnorm(days[3], bull_mean, bull_var)
market_bear_4 <- rnorm(days[4], bear_mean, bear_var)
market_bull_5 <- rnorm(days[5], bull_mean, bull_var)

# Creating the ground truth for regimes (1 = bull, 2 = bear) and the
# returns ts
true_regimes <- c( rep(1, days[1]), rep(2, days[2]), rep(1, days[3]), 
                   rep(2, days[4]), rep(1, days[5]))

returns <- c(market_bull_1, market_bear_2, market_bull_3, 
             market_bear_4, market_bull_5)

plot(returns, type="l", 
     xlab="Simulated returns with alternating regimes", 
     ylab="returns")

# Create and fit the HMM
hmm <- depmix(returns ~ 1, family=gaussian(), nstates = 2, 
              data = data.frame(returns=returns))
hmmfit <- fit(hmm, verbose = FALSE)

# Plot the true regimes and the posterios probabilities of the regimes
post_probs <- posterior(hmmfit)
layout(1:2)

plot(post_probs$state, type="s", main="True Regimes", xlab="", ylab="Regime")
matplot(post_probs[,-1], type="l", main="Regime Posterior Probabilities", 
        ylab="Probability")
legend(x="topright", c("Bull", "Bear"), fill = 1:2, bty = "n")