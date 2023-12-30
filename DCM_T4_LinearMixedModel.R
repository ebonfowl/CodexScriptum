library(tidyr)
# library(lme4)
library(lmerTest)
# library(emmeans)
# library(lsmeans)

df <- read.csv("D:\\Anaconda\\Scripts\\My Scripts\\DCM_T4\\DCM_T4_Test.csv", header = TRUE)

dfLong <- pivot_longer(df, cols  = starts_with("var"), names_to = c(".value", "time"), names_prefix = "var",
    names_sep = "\\_", values_drop_na = TRUE)

dfLong$Month = NA

dfLong <- within(dfLong, Month[time == 'T1'] <- 0)
dfLong <- within(dfLong, Month[time == 'T2'] <- 4)
dfLong <- within(dfLong, Month[time == 'T3'] <- 12)
dfLong <- within(dfLong, Month[time == 'T4'] <- 24)

dfLong$TimePoint = NA

dfLong <- within(dfLong, TimePoint[time == 'T1'] <- "T1")
dfLong <- within(dfLong, TimePoint[time == 'T2'] <- "T2")
dfLong <- within(dfLong, TimePoint[time == 'T3'] <- "T3")
dfLong <- within(dfLong, TimePoint[time == 'T4'] <- "T4")

# write.table(dfLong, file="DCM_T4_test_long.txt",row.names=FALSE, col.names=TRUE)

ANU <- dfLong

ANU.model <- lmer(ANUADRIPROTECT ~ Group*Month + Age + (1 + Month|ID), data = ANU, REML = FALSE, control = lmerControl(optimizer ="Nelder_Mead"))
ANU.null <- lmer(ANUADRIPROTECT ~ Age + (1 + Month|ID), data = ANU, REML = FALSE, control = lmerControl(optimizer ="Nelder_Mead"))
ANU.compare <- anova(ANU.null,ANU.model)
ANU.anova <- anova(ANU.model)
# emmip(ANU.model, ANUADRIPROTECT ~ Group * Month)

ECOG.model <- lmer(ECOG ~ Group*Month + Age + (1 + Month|ID), data = ANU, REML = FALSE, control = lmerControl(optimizer ="Nelder_Mead"))
ECOG.null <- lmer(ECOG ~ Age + (1 + Month|ID), data = ANU, REML = FALSE, control = lmerControl(optimizer ="Nelder_Mead"))
ECOG.compare <- anova(ECOG.null,ECOG.model)
ECOG.anova <- anova(ECOG.model)

sink("DCM_T4_ANUTOTAL_LME4.txt")
"Null Model"
summary(ANU.null)
""
"Observed Model"
summary(ANU.model)
""
"Model Comparison"
ANU.compare
""
"Model Effects Table"
ANU.anova
""
"Inspect Table for Tests"
show_tests(ANU.anova, fractions = TRUE)$Month
""
"Random Effects Table"
ranova(ANU.model)
""
"Pairwise Comparisons"
(lsm <- ls_means(ANU.model))
ls_means(ANU.model, pairwise = TRUE)
# lsmeans(ANU.model, pairwise ~ Group : Month)
# emmeans(ANU.model, pairwise ~ Group : Month)
sink()

sink("DCM_T4_ECOG_LME4.txt")
"Null Model"
summary(ECOG.null)
""
"Observed Model"
summary(ECOG.model)
""
"Model Comparison"
ECOG.compare
""
"Model Effects Table"
ECOG.anova
""
"Inspect Table for Tests"
show_tests(ECOG.anova, fractions = TRUE)$Month
""
"Random Effects Table"
ranova(ECOG.model)
""
"Pairwise Comparisons"
(lsm <- ls_means(ECOG.model))
ls_means(ECOG.model, pairwise = TRUE)
# lsmeans(ECOG.model, pairwise ~ Group : Month)
# emmeans(ECOG.model, pairwise ~ Group : Month)
sink()