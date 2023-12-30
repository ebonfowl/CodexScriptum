# detach("package:sem",unload=TRUE)
library(lavaan)
library(QuantPsyc)
# library(sem)

data <- read.csv("D:\\Anaconda\\Scripts\\My Scripts\\SEM_class_project\\nhanes_merge_full_completecases_older.csv", header = TRUE)

data$MET <- data$MET / 168

# print(data)

# normdf <- subset(data, select = c("WAIST", "GLU", "TRG", "HDL", "SBP"))

# mn <- mult.norm(normdf)

# print(mn)

data_full <- data

set.seed(40)
sampleframe <- rep(1:3, ceiling( nrow( data)/3 ) ) 

data$grp <- 0
data[  , "grp"  ] <- sample( sampleframe , size=nrow( data) ,  replace=FALSE )

data_m1 <- data[data$grp %in% 1 ,]
data_m2 <- data[data$grp %in% 2 ,]
data_m3 <- data[data$grp %in% 3 ,]

HS.model <- '
            MetSyn =~ WAIST + GLU + TRG + HDL + SBP
            TRG ~~ HDL
            '

MetSynCFA <- cfa(HS.model, data = data_full, estimator = "DWLS") # estimator = "DWLS"

sink("MetSyn_CFA.txt")
summary(MetSynCFA, standardized = TRUE, fit.measures = TRUE)
# lavResiduals(MetSynCFA, type = "raw")
sink()

# Structural model with sedentary time and actvity
model1 <- '
    # measurement model
        MetSyn =~ WAIST + GLU + TRG + HDL + SBP
        TRG ~~ HDL
    # regressions
        MetSyn ~ SED
'

MetSynSEM.m1 <- sem(model1, data = data_m1, estimator = "DWLS") # estimator = "DWLS"

sink("MetSyn_SEM.m1.txt")
summary(MetSynSEM.m1, standardized = TRUE, fit.measures = TRUE)
# lavResiduals(MetSynSEM.m1, type = "raw")
sink()

# Structural model with sedentary time and actvity
model2 <- '
    # measurement model
        MetSyn =~ WAIST + GLU + TRG + HDL + SBP
        TRG ~~ HDL
    # regressions
        MetSyn ~ SED
        MetSyn ~ MET
'

MetSynSEM.m2 <- sem(model2, data = data_m2, estimator = "DWLS") # estimator = "DWLS"

sink("MetSyn_SEM.m2.txt")
summary(MetSynSEM.m2, standardized = TRUE, fit.measures = TRUE)
# lavResiduals(MetSynSEM.m2, type = "raw")
sink()

# Structural model with actvity
model3 <- '
    # measurement model
        MetSyn =~ WAIST + GLU + TRG + HDL + SBP
        TRG ~~ HDL
    # regressions
        MetSyn ~ MET
'

MetSynSEM.m3 <- sem(model3, data = data_m3, estimator = "DWLS") # estimator = "DWLS"

sink("MetSyn_SEM.m3.txt")
summary(MetSynSEM.m3, standardized = TRUE, fit.measures = TRUE)
# lavResiduals(MetSynSEM.m3, type = "raw")
sink()