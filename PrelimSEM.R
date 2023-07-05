library(QuantPsyc)
library(sem)
library(lavaan)


data <- read.csv("d:/R/R-4.2.1/data/Dissertation/Preliminary_Data_Set.csv", header = TRUE)

# print(data)

normdf <- subset(data, select = c("HG_Total", "STS", "PkPwAv", "X10mHabAv", "X4mFastAv", "X6minWalk"))

mn <- mult.norm(normdf)

print(mn)

HS.model <- ' contract =~ HG_Total + STS + PkPwAv
              walk =~ X10mHabAv + X4mFastAv + X6minWalk '

cfafit <- cfa(HS.model, data = data, estimator = "DWLS")

summary(cfafit, standardized = TRUE, fit.measures = TRUE)

model <- '
    # measurement model
        contract =~ HG_Total + STS + PkPwAv
        walk =~ X10mHabAv + X4mFastAv + X6minWalk
    # regressions
        walk ~ contract
        contract ~ Age
'

fit <- sem(model, data = data, estimator = "DWLS")

summary(fit, standardized = TRUE, fit.measures = TRUE)
