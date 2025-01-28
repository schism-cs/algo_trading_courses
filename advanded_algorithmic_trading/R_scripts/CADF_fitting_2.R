library("quantmod")

layout(1)
# Downloading data of related equities
fromDate <- "2006-01-01"
toDate <- "2015-12-31"
getSymbols("RDS.A", from=fromDate, to=toDate)
getSymbols("RDS.B", from=fromDate, to=toDate)

RDSA <- get("RDS-A")
RDSB <- get("RDS-B")

rdsaAdj = unclass(RDSA$"RDS-A.Adjusted")
rdsbAdj = unclass(RDSB$"RDS-B.Adjusted")

plot(rdsaAdj, type="l", xlim=c(0,1500), ylim=c(5.0, 35.0),
     xlab=paste(fromDate,"to",toDate),
     ylab="RDS-A and RDS-B Backward-Adjusted Price in GBP", col="blue")
par(new=T)
plot(rdsbAdj, type="l", xlim=c(0,1500), ylim=c(5.0, 35.0),
     xlab="", ylab="", col="red", axes=F)
par(new=F)

# Scatterplot of Adjusted Values
plot(rdsaAdj, rdsbAdj, 
     xlab="RDS-A Backward-Adjusted Price", 
     ylab="RDS-B Backward-Adjusted Price")

# We need to find which is the independent variable
comb1 <- lm(rdsaAdj~rdsbAdj)
comb2 <- lm(rdsbAdj~rdsaAdj)

# Perform ADF test to find the independent variable
adf.test(comb1$residuals, k=1)
adf.test(comb2$residuals, k=1)

# Comb2 is lower -> ewaAdj is the independent variable
