
# ebonfowl: not super useful unless you want to use a directory other than the one the script is in

getwd()
setwd("E:/ESRM6523/R")

#AUTOMATING PACKAGES NEEDED FOR ANALYSES----------------------------------------
haspackage = require("lavaan")
if (haspackage==FALSE){
  install.packages("lavaan")
}
library("lavaan")

#Data Preparation---------------------------------------------------------------
#Read Corr, names, and SDs 
lower<-'
1.00
0.75 1.00
0.70 0.76 1.00
0.28 0.12 0.20 1.00
0.39 0.28 0.38 0.67 1.00
0.33 0.27 0.36 0.56 0.71 1.00
0.33 0.20 0.31 0.66 0.63 0.57 1.00'
vnames<-c("V1", "V2", "V3", "V4", "V5", "V6", "V7")
L09EX1.cor<-getCov(lower, names=vnames)
L09EX1.sd<-c(5.80, 8.59, 7.78, 6.39, 6.05, 5.86, 5.03)

#Covert Corr Matrix into Cov Matrix

L09EX1.cov<-cor2cov(L09EX1.cor, L09EX1.sd, names = vnames)
#save Cov matrix in a txt file
write.table(L09EX1.cov, file = "L09EX1COV.txt", row.names=FALSE, col.names=TRUE)


#CFA Model----------------------------------------------------------------------
L09EX1.m1 <- '
  F1 =~ V1+V2+V3
  '

# ebonfowl: the functions below use the sem() function instead of cfa() - there is currently not really a difference in lavaan
L09EX1.m1fit <- sem(L09EX1.m1,
                sample.cov = L09EX1.cov,
                sample.nobs = 192,
                estimator = "ML")

sink("L09EX1m1.txt")
#show summary of model fit statistics and parameters
summary(L09EX1.m1fit, standardized = TRUE, fit.measures = TRUE, rsquare = TRUE)
sink()  


L09EX1.m2 <- '
  F1 =~ NA*V1+V2+V3
  F1 ~~ 1*F1
  '

L09EX1.m2fit <- sem(L09EX1.m2,
                  sample.cov = L09EX1.cov,
                  sample.nobs = 192,
                  estimator = "ML")

sink("L09EX1m2.txt")
#show summary of model fit statistics and parameters
summary(L09EX1.m2fit, standardized = TRUE, fit.measures = TRUE, rsquare = TRUE)
sink()  


L09EX1.m3 <- '
  F1 =~ NA*V1+V2+V3
  F2 =~ NA*V4+V5+V6+V7
  F1 ~~ 0*F2
    F1 ~~ 1*F1
      F2 ~~ 1*F2
  '

L09EX1.m3fit <- sem(L09EX1.m3,
         sample.cov = L09EX1.cov,
         sample.nobs = 192,
         #mimic="mplus",
         estimator = "ML")

sink("L09EX1m3.txt")
#show summary of model fit statistics and parameters
summary(L09EX1.m3fit, standardized = TRUE, fit.measures = TRUE, rsquare = TRUE)
sink()  


L09EX1.m4<-'
  F1 =~ V1+V2+V3
  F2 =~ V4+V5+V6+V7
  F1 ~~ F2
  '

L09EX1.m4fit<-sem(L09EX1.m4,
                  sample.cov = L09EX1.cov,
                  sample.nobs = 192,
                  #mimic="mplus",
                  estimator = "ML")

sink("L09EX1m4.txt")
#show summary of model fit statistics and parameters
summary(L09EX1.m4fit, standardized = TRUE, fit.measures = TRUE, rsquare = TRUE)
sink()  


L09EX1.m5<-'
  F1 =~ V1+V2+V3+V4+V5+V6+V7
  '

L09EX1.m5fit<-sem(L09EX1.m5,
                  sample.cov = L09EX1.cov,
                  sample.nobs = 192,
                  #mimic="mplus",
                  estimator = "ML")

sink("L09EX1m5.txt")
#show summary of model fit statistics and parameters
summary(L09EX1.m5fit, standardized = TRUE, fit.measures = TRUE, rsquare = TRUE)
sink()  





