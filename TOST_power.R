library(TOSTER)

ss <- powerTOSTtwo.raw(alpha=0.05,statistical_power=0.8,low_eqbound=204,high_eqbound=284,sdpooled=100.4)

print(ss)