library(psych)
library(dplyr)
library(irr)
library(blandr)
library(ggplot2)
library(plotROC)

data <- read.csv("d:/R/R-4.2.1/scripts/NTV_Database.csv", header = TRUE)

#pathpoints <- select(data, c("PathsRev", "Trail_Making_Time"))

#arrowmatch <- select(data, c("NT_Processing_Speed_Raw_Score", "flanker_score"))

#symbolmatch <- select(data, c("NT_Attention_Raw_Score", "Coding_Correct"))

#lightreaction <- select(data, c("LightRev", "gng_score"))

pathpoints <- select(data, c("PathsNormal", "TrailNormal"))

arrowmatch <- select(data, c("ArrowNormal", "FlankerNormal"))

symbolmatch <- select(data, c("SymbolNormal", "CodingNormal"))

lightreaction <- select(data, c("LightNormal", "GoNoNormal"))

#print(pathpoints)

#ICC(pathpoints)

print(cor.test(data$"PathsRev", data$"Trail_Making_Time", method = "pearson"))

print(cor.test(data$"NT_Processing_Speed_Raw_Score", data$"flanker_score", method = "pearson"))

print(cor.test(data$"NT_Attention_Raw_Score", data$"Coding_Correct", method = "pearson"))

print(cor.test(data$"LightRev", data$"gng_score", method = "pearson"))

print(icc(pathpoints, model = "oneway", type = "agreement", unit = "single"))

print(icc(arrowmatch, model = "oneway", type = "agreement", unit = "single"))

print(icc(symbolmatch, model = "oneway", type = "agreement", unit = "single"))

print(icc(lightreaction, model = "oneway", type = "agreement", unit = "single"))

print(blandr.output.text(data$"PathsNormal", data$"TrailNormal", sig.level=0.95))
blandr.draw(data$"PathsNormal", data$"TrailNormal", ciDisplay = FALSE, ciShading = FALSE)

print(blandr.output.text(data$"ArrowNormal", data$"FlankerNormal", sig.level=0.95))
blandr.draw(data$"ArrowNormal", data$"FlankerNormal", ciDisplay = FALSE, ciShading = FALSE)

print(blandr.output.text(data$"SymbolNormal", data$"CodingNormal", sig.level=0.95))
blandr.draw(data$"SymbolNormal", data$"CodingNormal", ciDisplay = FALSE, ciShading = FALSE)

print(blandr.output.text(data$"LightNormal", data$"GoNoNormal", sig.level=0.95))
blandr.draw(data$"LightNormal", data$"GoNoNormal", ciDisplay = FALSE, ciShading = FALSE)

D.ex <- data$"Sick"

# Switch these variables around to generate ROCs
M1 <- data$"NTComp"
M2 <- data$"GSComp"

test <- data.frame(D = D.ex, D.str = c("Healthy", "Ill")[D.ex + 1], 
                   M1 = M1, M2 = M2, stringsAsFactors = FALSE)

longtest <- melt_roc(test, "D", c("M1", "M2"))
ggplot(longtest, aes(d = D, m = M, color = name)) + geom_roc() + style_roc()