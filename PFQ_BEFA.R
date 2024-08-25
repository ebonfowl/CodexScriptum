library(rstan)
library(blavaan)
library(psych)
library(tidyverse)
library(coda)
library(future)
library(ggplot2)
library(bayesplot)
library(timeR)
library(corrplot)
library(BayesFM)

# All dem cores!

plan("multisession")

# Let's time this sucker

timer <- createTimer(precision = "s")
timer$start("runtime")

data.full <- read.csv("D:\\Anaconda\\Scripts\\My Scripts\\Dissertation\\PowerAgingAim1.csv")

OutPath <- "D:\\Anaconda\\Scripts\\My Scripts\\Dissertation\\Output\\"

#vars <- c(PickupWalk, FourmWalk, StairClimb, TUG, FiveSTS) # ADD ALL VARIABLE NAMES AS THEY APPEAR IN THE DATA SET

data <- na.omit(subset(data.full, select = c(FourmWalk, StairClimb, TUG, FiveSTS)))

dataOut <- na.omit(subset(data.full, select = c(ID, FourmWalk, StairClimb, TUG, FiveSTS)))

#corr.matrix <- corrplot.mixed(corr = cor(data), upper = "ellipse", order = "hclust")

png(paste0(OutPath, "CorrelationMatrix.png"), width = 1920, height = 1440, pointsize = 60)
#corr.matrix
corrplot.mixed(corr = cor(data), upper = "ellipse", order = "hclust")
dev.off()

Nid <- 2              ## minimum number of variables per factor
pmax <- trunc(ncol(data)/Nid)   ## maximum number of factors
#pmax

set.seed(123)
Rsim <- simul.R.prior(pmax, nu0 = pmax + c(1, 2, 3, 4, 5))

png(paste0(OutPath, "CorrelationSimulationPlot.png"), width = 1920, height = 1440, pointsize = 60)
plot(Rsim)
dev.off()

sink(paste0(OutPath, "PowerAgingEFA_CorrSimulation.txt"))
"Correlation Prior Simulation"
summary(Rsim)
sink()

Ksim <- simul.nfac.prior(nvar = ncol(data), Nid = Nid, Kmax = pmax, kappa = c(.1, .2, .5, 1))

png(paste0(OutPath, "FactorSimulationPlot.png"), width = 1920, height = 1440, pointsize = 60)
plot(Ksim)
dev.off()

sink(paste0(OutPath, "PowerAgingEFA_FactorSimulation.txt"))
"Number Of Factors Simulation"
summary(Ksim)
sink()

set.seed(222)
fitbefa <- befa(data, Nid = 2, Kmax = pmax, nu0 = 3, kappa = 0.5, kappa0 = 0.1, xi0 = 0.1,
                burnin = 5000, iter = 50000)
fitbefa <- post.column.switch(fitbefa)   ## column reordering
fitbefa <- post.sign.switch(fitbefa)     ## sign switching
sumbefa <- summary(fitbefa)

sink(paste0(OutPath, "PowerAgingEFA.txt"))
"Number Of Factors Simulation"
sumbefa
sink()

# START MCMC CFA

color_scheme_set("purple")

# Default Priors

def.priors <- dpriors(rho = "beta(1,2)", theta = "gamma(.5,.5)[sd]")
priors.variance <- dpriors(rho = "beta(1,2)", theta = "gamma(.1,.1)[sd]")

# Null Model
mod.null <- 'FourmWalk ~~ FourmWalk
             StairClimb ~~ StairClimb
             TUG ~~ TUG
             FiveSTS ~~ FiveSTS'

# CFA Model
mod.CFA <- 'PFQ =~ FourmWalk + StairClimb + TUG + FiveSTS'

# Fit Models

fit.null <- bcfa(mod.null, data = data, n.chains = 3, burnin = 40000, sample = 80000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
fit.null.dblits <- bcfa(mod.null, data = data, n.chains = 3, burnin = 80000, sample = 160000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
fit.CFA <- bcfa(mod.CFA, data = data, n.chains = 3, burnin = 40000, sample = 80000, target = "stan", dp = def.priors, bcontrol = list(cores = 3), save.lvs = TRUE, std.lv = TRUE)
fit.CFA.dblits <- bcfa(mod.CFA, data = data, n.chains = 3, burnin = 80000, sample = 160000, target = "stan", dp = def.priors, bcontrol = list(cores = 3), std.lv = TRUE)
fit.CFA.default <- bcfa(mod.CFA, data = data, n.chains = 3, burnin = 40000, sample = 80000, target = "stan", bcontrol = list(cores = 3), std.lv = TRUE)
fit.CFA.variance <- bcfa(mod.CFA, data = data, n.chains = 3, burnin = 40000, sample = 80000, target = "stan", dp = priors.variance, bcontrol = list(cores = 3), std.lv = TRUE)

# Plot trace plots and export

png(paste0(OutPath, "TracePlot.png"), width = 1920, height = 1440, pointsize = 60)
plot(fit.CFA, pars = 1:8, plot.type = "trace")
dev.off()

# Gelman-Rubin Plot

mcmc.list <- blavInspect(fit.CFA, what = "mcmc")
png(paste0(OutPath, "GelmanRubinPlot.png"), width = 1920, height = 1440, pointsize = 30)
gelman.plot(mcmc.list)
dev.off()

# Make posterior histogram plots and export

png(paste0(OutPath, "PosteriorHistogram.png"), width = 1920, height = 1440, pointsize = 60)
plot(fit.CFA, pars = 1:8, plot.type = "hist")
dev.off()

# Make autocorrelation plots and export

png(paste0(OutPath, "AutocorrelationPlot.png"), width = 4000, height = 3000, pointsize = 60)
par(mfrow = c(2,2))
plot(fit.CFA, pars = 1:8, plot.type = "acf")
dev.off()

# Make posterior density plots and export

p1 <- mcmc_dens_overlay(mcmc.list)
ggsave(paste0(OutPath, "PosteriorDensity.png"), plot = p1)

# Make summary text file and save

Indices.CFA <- blavFitIndices(fit.CFA, baseline.model = fit.null)
gelmanRubin <- gelman.diag(mcmc.list)

sink(paste0(OutPath, "PowerAgingCFA.txt"))
"Model Summary"
summary(fit.CFA)
""
"Model Fit Indices"
summary(Indices.CFA, central.tendency = c("mean","median","mode"), prob = .90)
""
"Model Gelman-Rubin"
gelmanRubin
sink()

# Posterior distributions of fit indices

dist_fits.CFA <- data.frame(Indices.CFA@indices)

dist_fits.CFA <- na.omit(dist_fits.CFA)

p1 <- mcmc_pairs(dist_fits.CFA, diag_fun = "hist")
ggsave(paste0(OutPath, "FitIndicesDistributions.png"), plot = p1)

# Make summary for default priors and save

Indices.CFA.default <- blavFitIndices(fit.CFA.default, baseline.model = fit.null)

mcmc.default.list <- blavInspect(fit.CFA.default, what = "mcmc")
gelmanRubin.default <- gelman.diag(mcmc.default.list)

sink(paste0(OutPath, "PowerAgingCFA_DefaultPriors.txt"))
"Model Summary"
summary(fit.CFA.default)
""
"Model Fit Indices"
summary(Indices.CFA.default, central.tendency = c("mean","median","mode"), prob = .90)
""
"Model Gelman-Rubin"
gelmanRubin.default
sink()

# Make summary for double iterations and save

Indices.CFA.dblits <- blavFitIndices(fit.CFA.dblits, baseline.model = fit.null.dblits)

mcmc.dblits.list <- blavInspect(fit.CFA.dblits, what = "mcmc")
gelmanRubin.dblits <- gelman.diag(mcmc.dblits.list)

sink(paste0(OutPath, "PowerAgingCFA_DoubleIterations.txt"))
"Model Summary"
summary(fit.CFA.dblits)
""
"Model Fit Indices"
summary(Indices.CFA.dblits, central.tendency = c("mean","median","mode"), prob = .90)
""
"Model Gelman-Rubin"
gelmanRubin.dblits
sink()

# Make summary for strong variance priors and save

Indices.CFA.variance <- blavFitIndices(fit.CFA.variance, baseline.model = fit.null)

mcmc.variance.list <- blavInspect(fit.CFA.variance, what = "mcmc")
gelmanRubin.variance <- gelman.diag(mcmc.variance.list)

sink(paste0(OutPath, "PowerAgingCFA_StrongVariance.txt"))
"Model Summary"
summary(fit.CFA.variance)
""
"Model Fit Indices"
summary(Indices.CFA.variance, central.tendency = c("mean","median","mode"), prob = .90)
""
"Model Gelman-Rubin"
gelmanRubin.variance
sink()

# Get factor scores

FacScores <- blavInspect(fit.CFA, "lvs", "means")

write.csv(FacScores, paste0(OutPath, "FactorScores.csv"), row.names = FALSE)

write.csv(dataOut, paste0(OutPath, "FactorIDs.csv"), row.names = FALSE)