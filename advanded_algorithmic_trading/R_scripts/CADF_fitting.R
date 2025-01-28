library("quantmod")

layout(1)
# Downloading data of related equities
fromDate <- "2006-04-26"
toDate <- "2012-04-09"
getSymbols("EWA", from=fromDate, to=toDate)
getSymbols("EWC", from=fromDate, to=toDate)

ewaAdj = unclass(EWA$EWA.Adjusted)
ewcAdj = unclass(EWC$EWC.Adjusted)

plot(ewaAdj, type="l", xlim=c(0,1500), ylim=c(5.0, 35.0),
     xlab=paste(fromDate,"to",toDate),
     ylab="ETF Backward-Adjusted price in USD", col="blue")
par(new=T)
plot(ewcAdj, type="l", xlim=c(0,1500), ylim=c(5.0, 35.0),
     xlab="", ylab="", col="red", axes=F)
par(new=F)

# Scatterplot of Adjusted Values
plot(ewaAdj, ewcAdj, 
     xlab="EWA Backward-Adjusted Price", 
     ylab="EWC Backward-Adjusted Price")

# We need to find which is the independent variable
comb1 <- lm(ewcAdj~ewaAdj)
comb2 <- lm(ewaAdj~ewcAdj)

# Perform ADF test to find the independent variable
adf.test(comb1$residuals, k=1)
adf.test(comb2$residuals, k=1)

# Comb2 is lower -> ewaAdj is the independent variable
