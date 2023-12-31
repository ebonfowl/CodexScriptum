#install lavaan package iif you haven't already---------------------------------
#[Note: You do not need to install a package every time]
install.packages("lavaan")                 

#-------------------------------------------------------------------------------
#ESRM6523 Lecture 4 - Ex2: Path Modeling----------------------------------------
#-------------------------------------------------------------------------------

#AUTOMATING PACKAGES NEEDED FOR ANALYSES----------------------------------------
haspackage = require("lavaan")
if (haspackage==FALSE){
  install.packages("lavaan")
}
library("lavaan")

#Import Covariance Matrix-------------------------------------------------------
lower<-'
0.623076  
-0.307902 1.951609 
0.1983261 0.2905592 1.628176 
-2.315193 28.80666 18.21936 1375.4456 
'
#Using getCov() function to generate a full cov matrix--------------------------
L4Ex2data.cov<-
  getCov(lower, names=c("Read","Math","Goal","MathSAT"))


#Path Modeling (modelHW01)------------------------------------------------------
L4ex2a.syntax = 
"
#endogenous variable equations
Goal ~ Read + Math
MathSAT ~ Read + Math + Goal

#endogenous variable intercepts
#Gaol ~ 1
#MathSAT ~ 1

#endogenous variable residual variances
Goal ~~ Goal
MathSAT ~~ MathSAT

#exogenous variables covariate
Read ~~ Math

#endogenous variable residual covariances
#none specified in the original model so these have zeros:
#Goal ~ 0*Read + 0*Math
#MathSAT ~ 0*Read + 0*Math + 0*Goal

#indirect effect of interest:

"
#estimate model
L4ex2a.fit = sem(L4ex2a.syntax,
  sample.cov=L4Ex2data.cov,
  sample.nobs=523,
#  mimic="mplus",
  estimator = "ML")

#show summary of model fit statistics and parameters
summary(L4ex2a.fit, standardized=TRUE, fit.measures=TRUE, rsquare = TRUE)
  
