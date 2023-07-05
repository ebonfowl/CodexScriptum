library(ICC.Sample.Size)

ss <- calculateIccSampleSize(p=0.90,p0=0.70,k=2,alpha=0.05,tails=2,power=0.80)

print(ss)