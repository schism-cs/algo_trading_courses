library("depmixS4")
library("quantmod")

getSymbols("^GSPC", from="2004-01-01")

gspcRets <- diff(log(Cl(GSPC)))
returns <- as.numeric(gspcRets)

plot(gspcRets)

hmm <- depmix(returns ~ 1, family = gaussian(), nstates = 2, 
              data = data.frame(returns=returns))

hmmfit <- fit(hmm, verbose=FALSE)

post_probs <- posterior(hmmfit)

layout(1:2)
plot(returns, type="l", main="Regime Detection", xlab="", ylab="Returns")

matplot(post_probs[, -1], type="l", main="Regime Posterior Probabilities",
        ylab="Probability")

legend(x="bottomleft", c("Regime #1", "Regime #2"), fill=1:2, bty="n")


hmm <- depmix(returns ~ 1, family = gaussian(), nstates = 3, 
              data = data.frame(returns=returns))

hmmfit <- fit(hmm, verbose=FALSE)

post_probs <- posterior(hmmfit)

layout(1:2)
plot(returns, type="l", main="Regime Detection", xlab="", ylab="Returns")

matplot(post_probs[, -1], type="l", main="Regime Posterior Probabilities",
        ylab="Probability")

legend(x="bottomleft", c("Regime #1", "Regime #2", "Regime #3"), fill=1:3, bty="n")