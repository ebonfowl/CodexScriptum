library(rstan)
library(blavaan)
library(psych)
library(tidyverse)
library(coda)
library(future)
library(ggplot2)
library(bayesplot)
library(timeR)

# All dem cores!

plan("multisession")

# Let's time this sucker

timer <- createTimer(precision = "s")
timer$start("runtime")

data <- read.csv("D:\\DCM T4 Analyses\\DC-MARVEL_public_data.csv")

# Grab all the old person data and stuff into data frame

old.data <- subset(data, Age >= 65)

OutPath <- "D:\\Anaconda\\Scripts\\My Scripts\\DCM_MCMC_LGM\\"

OutPath.default <- "D:\\Anaconda\\Scripts\\My Scripts\\DCM_MCMC_LGM\\DefaultPriors\\"

OutPath.dblits <- "D:\\Anaconda\\Scripts\\My Scripts\\DCM_MCMC_LGM\\DoubleIterations\\"

OutPath.variance <- "D:\\Anaconda\\Scripts\\My Scripts\\DCM_MCMC_LGM\\StrongVariancePriors\\"

# Load prior specification file

df.priors <- read.csv("D:\\DCM T4 Analyses\\MCMC_Quadratic_Priors.csv")

# Make a list of variable names without time designations

VarsList <- list("ANUADRI_TOTAL"
                 , "ANUADRI_PROTECT"
                 , "ANUADRI_RISK"
                 , "ECOG12"
                 , "CAIDE"
                 )

# Lets try placing the correlation prior in dpriors()

def.priors <- dpriors(rho = "beta(1,2)")

color_scheme_set("purple") # diggin the purp!

# Inside for loop below here

for (var in VarsList)
{
    # Concatonate strings and assign variable names to m1-m4

    m1 <- paste0(var, "_T1")
    m2 <- paste0(var, "_T2")
    m3 <- paste0(var, "_T3")
    m4 <- paste0(var, "_T4")

    # Assign prior hyperparameters to objects

    # Regressions
    IonGroupA <- df.priors[df.priors$Parameter == "IonGROUP", paste0(var, "a")]
    IonGroupB <- df.priors[df.priors$Parameter == "IonGROUP", paste0(var, "b")]
    SonGroupA <- df.priors[df.priors$Parameter == "SonGROUP", paste0(var, "a")]
    SonGroupB <- df.priors[df.priors$Parameter == "SonGROUP", paste0(var, "b")]
    QonGroupA <- df.priors[df.priors$Parameter == "QonGROUP", paste0(var, "a")]
    QonGroupB <- df.priors[df.priors$Parameter == "QonGROUP", paste0(var, "b")]

    # Intercepts
    IceptA <- df.priors[df.priors$Parameter == "Icept", paste0(var, "a")]
    IceptB <- df.priors[df.priors$Parameter == "Icept", paste0(var, "b")]
    SceptA <- df.priors[df.priors$Parameter == "Scept", paste0(var, "a")]
    SceptB <- df.priors[df.priors$Parameter == "Scept", paste0(var, "b")]
    QceptA <- df.priors[df.priors$Parameter == "Qcept", paste0(var, "a")]
    QceptB <- df.priors[df.priors$Parameter == "Qcept", paste0(var, "b")]

    # Factor Variances
    IvarA <- df.priors[df.priors$Parameter == "Ivar", paste0(var, "a")]
    IvarB <- df.priors[df.priors$Parameter == "Ivar", paste0(var, "b")]
    SvarA <- df.priors[df.priors$Parameter == "Svar", paste0(var, "a")]
    SvarB <- df.priors[df.priors$Parameter == "Svar", paste0(var, "b")]
    QvarA <- df.priors[df.priors$Parameter == "Qvar", paste0(var, "a")]
    QvarB <- df.priors[df.priors$Parameter == "Qvar", paste0(var, "b")]

    # Error Variances
    m1evarA <- df.priors[df.priors$Parameter == "m1evar", paste0(var, "a")]
    m1evarB <- df.priors[df.priors$Parameter == "m1evar", paste0(var, "b")]
    m2evarA <- df.priors[df.priors$Parameter == "m2evar", paste0(var, "a")]
    m2evarB <- df.priors[df.priors$Parameter == "m2evar", paste0(var, "b")]
    m3evarA <- df.priors[df.priors$Parameter == "m3evar", paste0(var, "a")]
    m3evarB <- df.priors[df.priors$Parameter == "m3evar", paste0(var, "b")]
    m4evarA <- df.priors[df.priors$Parameter == "m4evar", paste0(var, "a")]
    m4evarB <- df.priors[df.priors$Parameter == "m4evar", paste0(var, "b")]

    # Define the models

    # Null model
    mod.null <- paste0(m1, ' ~~ ', m1,'
                       ', m2, ' ~~ ', m2,'
                       ', m3, ' ~~ ', m3,'
                       ', m4, ' ~~ ', m4)

    #linear growth model with covariate group
    mod1 <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ 0*',m1,' + 4*',m2,' + 12*',m3,' + 24*',m4,'
             i ~ prior("normal(',IonGroupA,',',IonGroupB,')")*group
             s ~ prior("normal(',SonGroupA,',',SonGroupB,')")*group
             i ~ prior("normal(',IceptA,',',IceptB,')")*1
             s ~ prior("normal(',SceptA,',',SceptB,')")*1
             i ~~ prior("gamma(',IvarA,',',IvarB,')[sd]")*i
             s ~~ prior("gamma(',SvarA,',',SvarB,')[sd]")*s
             ',m1,' ~~ prior("gamma(',m1evarA,',',m1evarB,')[sd]")*',m1,'
             ',m2,' ~~ prior("gamma(',m2evarA,',',m2evarB,')[sd]")*',m2,'
             ',m3,' ~~ prior("gamma(',m3evarA,',',m3evarB,')[sd]")*',m3,'
             ',m4,' ~~ prior("gamma(',m4evarA,',',m4evarB,')[sd]")*',m4)

    #centered quadratic growth model with covariate group
    mod2 <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ (-12)*',m1,' + (-8)*',m2,' + 0*',m3,' + 12*',m4,'
             q =~ 144*',m1,' + 64*',m2,' + 0*',m3,' + 144*',m4,'
             i ~ prior("normal(',IonGroupA,',',IonGroupB,')")*group
             s ~ prior("normal(',SonGroupA,',',SonGroupB,')")*group
             q ~ prior("normal(',QonGroupA,',',QonGroupB,')")*group
             i ~ prior("normal(',IceptA,',',IceptB,')")*1
             s ~ prior("normal(',SceptA,',',SceptB,')")*1
             q ~ prior("normal(',QceptA,',',QceptB,')")*1
             i ~~ prior("gamma(',IvarA,',',IvarB,')[sd]")*i
             s ~~ prior("gamma(',SvarA,',',SvarB,')[sd]")*s
             q ~~ prior("gamma(',QvarA,',',QvarB,')[sd]")*q
             ',m1,' ~~ prior("gamma(',m1evarA,',',m1evarB,')[sd]")*',m1,'
             ',m2,' ~~ prior("gamma(',m2evarA,',',m2evarB,')[sd]")*',m2,'
             ',m3,' ~~ prior("gamma(',m3evarA,',',m3evarB,')[sd]")*',m3,'
             ',m4,' ~~ prior("gamma(',m4evarA,',',m4evarB,')[sd]")*',m4)

    #linear growth model with covariate group with no priors
    mod1.default <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ 0*',m1,' + 4*',m2,' + 12*',m3,' + 24*',m4,'
             i ~ group
             s ~ group')

    #centered quadratic growth model with covariate group with no priors
    mod2.default <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ (-12)*',m1,' + (-8)*',m2,' + 0*',m3,' + 12*',m4,'
             q =~ 144*',m1,' + 64*',m2,' + 0*',m3,' + 144*',m4,'
             i ~ group
             s ~ group
             q ~ group')
    
    #linear growth model with covariate group with strong variance priors
    mod1.variance <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ 0*',m1,' + 4*',m2,' + 12*',m3,' + 24*',m4,'
             i ~ prior("normal(',IonGroupA,',',IonGroupB,')")*group
             s ~ prior("normal(',SonGroupA,',',SonGroupB,')")*group
             i ~ prior("normal(',IceptA,',',IceptB,')")*1
             s ~ prior("normal(',SceptA,',',SceptB,')")*1
             i ~~ prior("gamma(.1,.1)[sd]")*i
             s ~~ prior("gamma(.1,.1)[sd]")*s
             ',m1,' ~~ prior("gamma(.1,.1)[sd]")*',m1,'
             ',m2,' ~~ prior("gamma(.1,.1)[sd]")*',m2,'
             ',m3,' ~~ prior("gamma(.1,.1)[sd]")*',m3,'
             ',m4,' ~~ prior("gamma(.1,.1)[sd]")*',m4)

    #centered quadratic growth model with covariate group with strong variance priors
    mod2.variance <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ (-12)*',m1,' + (-8)*',m2,' + 0*',m3,' + 12*',m4,'
             q =~ 144*',m1,' + 64*',m2,' + 0*',m3,' + 144*',m4,'
             i ~ prior("normal(',IonGroupA,',',IonGroupB,')")*group
             s ~ prior("normal(',SonGroupA,',',SonGroupB,')")*group
             q ~ prior("normal(',QonGroupA,',',QonGroupB,')")*group
             i ~ prior("normal(',IceptA,',',IceptB,')")*1
             s ~ prior("normal(',SceptA,',',SceptB,')")*1
             q ~ prior("normal(',QceptA,',',QceptB,')")*1
             i ~~ prior("gamma(.1,.1)[sd]")*i
             s ~~ prior("gamma(.1,.1)[sd]")*s
             q ~~ prior("gamma(.1,.1)[sd]")*q
             ',m1,' ~~ prior("gamma(.1,.1)[sd]")*',m1,'
             ',m2,' ~~ prior("gamma(.1,.1)[sd]")*',m2,'
             ',m3,' ~~ prior("gamma(.1,.1)[sd]")*',m3,'
             ',m4,' ~~ prior("gamma(.1,.1)[sd]")*',m4)
    
    # Fit the models

    fit.null <- bgrowth(mod.null, data = data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod1 <- bgrowth(mod1, data = data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod2 <- bgrowth(mod2, data = data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod1.dblits <- bgrowth(mod1, data = data, n.chains = 3, burnin = 10000, sample = 20000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod2.dblits <- bgrowth(mod2, data = data, n.chains = 3, burnin = 10000, sample = 20000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod1.default <- bgrowth(mod1.default, data = data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", bcontrol = list(cores = 3))
    fit.mod2.default <- bgrowth(mod2.default, data = data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", bcontrol = list(cores = 3))
    fit.mod1.variance <- bgrowth(mod1.variance, data = data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod2.variance <- bgrowth(mod2.variance, data = data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    
    # Plot trace plots and export

    png(paste0(OutPath, var, "_LGM_Traceplot.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod1, pars = 1:10, plot.type = "trace")
    dev.off()

    png(paste0(OutPath, var, "_QLGM_Traceplot.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod2, pars = 1:13, plot.type = "trace")
    dev.off()

    # Obtain Gelman-Rubin Diagnostic and export plots

    mcmc.list1 <- blavInspect(fit.mod1, what = "mcmc")
    gelmanRubin1 <- gelman.diag(mcmc.list1)

    mcmc.list2 <- blavInspect(fit.mod2, what = "mcmc")
    gelmanRubin2 <- gelman.diag(mcmc.list2)

    png(paste0(OutPath, var, "_LGM_GelmanRubinPlot.png"), width = 1920, height = 1440, pointsize = 30)
    gelman.plot(mcmc.list1)
    dev.off()

    png(paste0(OutPath, var, "_QLGM_GelmanRubinPlot.png"), width = 1920, height = 1440, pointsize = 30)
    gelman.plot(mcmc.list2)
    dev.off()

    # Make posterior histogram plots and export

    png(paste0(OutPath, var, "_LGM_PostHist.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod1, pars = 1:10, plot.type = "hist")
    dev.off()

    png(paste0(OutPath, var, "_QLGM_PostHist.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod2, pars = 1:13, plot.type = "hist")
    dev.off()

    # Make autocorrelation plots and export

    png(paste0(OutPath, var, "_LGM_AutocorPlot.png"), width = 4000, height = 3000, pointsize = 60)
    par(mfrow = c(2,2))
    plot(fit.mod1, pars = 1:10, plot.type = "acf")
    dev.off()

    png(paste0(OutPath, var, "_QLGM_AutocorPlot.png"), width = 4000, height = 3000, pointsize = 60)
    par(mfrow = c(2,2))
    plot(fit.mod2, pars = 1:13, plot.type = "acf")
    dev.off()

    # Make posterior density plots and export

    p1 <- mcmc_dens_overlay(mcmc.list1)
    ggsave(paste0(OutPath, var, "_LGM_PostDensity.png"), plot = p1)

    p2 <- mcmc_dens_overlay(mcmc.list2)
    ggsave(paste0(OutPath, var, "_QLGM_PostDensity.png"), plot = p2)
    
    # Make summary text file and save

    Indices.mod1 <- blavFitIndices(fit.mod1, baseline.model = fit.null)
    Indices.mod2 <- blavFitIndices(fit.mod2, baseline.model = fit.null)

    sink(paste0(OutPath, var, "_GrowthModels.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1, fit.mod2))
    sink()

    # Make summary for default priors and save

    Indices.mod1.default <- blavFitIndices(fit.mod1.default, baseline.model = fit.null)
    Indices.mod2.default <- blavFitIndices(fit.mod2.default, baseline.model = fit.null)

    mcmc.default.list1 <- blavInspect(fit.mod1.default, what = "mcmc")
    gelmanRubin1.default <- gelman.diag(mcmc.default.list1)

    mcmc.default.list2 <- blavInspect(fit.mod2.default, what = "mcmc")
    gelmanRubin2.default <- gelman.diag(mcmc.default.list2)

    sink(paste0(OutPath.default, var, "_GrowthModels.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1.default))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1.default, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1.default)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2.default))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2.default, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2.default)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1.default, fit.mod2.default))
    sink()

    # Make summary for double iterations and save

    Indices.mod1.dblits <- blavFitIndices(fit.mod1.dblits, baseline.model = fit.null)
    Indices.mod2.dblits <- blavFitIndices(fit.mod2.dblits, baseline.model = fit.null)

    mcmc.dblits.list1 <- blavInspect(fit.mod1.dblits, what = "mcmc")
    gelmanRubin1.dblits <- gelman.diag(mcmc.dblits.list1)

    mcmc.dblits.list2 <- blavInspect(fit.mod2.dblits, what = "mcmc")
    gelmanRubin2.dblits <- gelman.diag(mcmc.dblits.list2)

    sink(paste0(OutPath.dblits, var, "_GrowthModels.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1.dblits))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1.dblits, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1.dblits)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2.dblits))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2.dblits, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2.dblits)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1.dblits, fit.mod2.dblits))
    sink()

    # Make summary for strong variance priors and save

    Indices.mod1.variance <- blavFitIndices(fit.mod1.variance, baseline.model = fit.null)
    Indices.mod2.variance <- blavFitIndices(fit.mod2.variance, baseline.model = fit.null)
    
    mcmc.variance.list1 <- blavInspect(fit.mod1.variance, what = "mcmc")
    gelmanRubin1.variance <- gelman.diag(mcmc.variance.list1)

    mcmc.variance.list2 <- blavInspect(fit.mod2.variance, what = "mcmc")
    gelmanRubin2.variance <- gelman.diag(mcmc.variance.list2)

    sink(paste0(OutPath.variance, var, "_GrowthModels.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1.variance))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1.variance, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1.variance)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2.variance))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2.variance, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2.variance)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1.variance, fit.mod2.variance))
    sink()

    # Output indices posterior distribution histograms
    # Using if conditional as quick and dirty fix for ECOG error

    if (var != "ECOG12" && var != "CAIDE") {
    
        dist_fits.mod1 <- data.frame(Indices.mod1@indices)
        dist_fits.mod2 <- data.frame(Indices.mod2@indices)

        p1 <- mcmc_pairs(dist_fits.mod1, diag_fun = "hist")
        ggsave(paste0(OutPath, var, "_LGM_IndicesDistributions.png"), plot = p1)

        p2 <- mcmc_pairs(dist_fits.mod2, diag_fun = "hist")
        ggsave(paste0(OutPath, var, "_QLGM_IndicesDistributions.png"), plot = p2)

    }

    # Clean up big stuff - not sure how important this is since it will all be overwritten in the loop...
    rm(fit.mod1, fit.mod2, fit.null)

    ####################################################
    ###     Do it all again for the older adults     ###
    ####################################################
    
    # Fit the models

    fit.null <- bgrowth(mod.null, data = old.data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod1 <- bgrowth(mod1, data = old.data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod2 <- bgrowth(mod2, data = old.data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod1.dblits <- bgrowth(mod1, data = old.data, n.chains = 3, burnin = 10000, sample = 20000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod2.dblits <- bgrowth(mod2, data = old.data, n.chains = 3, burnin = 10000, sample = 20000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod1.default <- bgrowth(mod1.default, data = old.data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", bcontrol = list(cores = 3))
    fit.mod2.default <- bgrowth(mod2.default, data = old.data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", bcontrol = list(cores = 3))
    fit.mod1.variance <- bgrowth(mod1.variance, data = old.data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    fit.mod2.variance <- bgrowth(mod2.variance, data = old.data, n.chains = 3, burnin = 5000, sample = 10000, target = "stan", dp = def.priors, bcontrol = list(cores = 3))
    
    # Plot trace plots and export

    png(paste0(OutPath, var, "_LGM_Traceplot_Older.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod1, pars = 1:10, plot.type = "trace")
    dev.off()

    png(paste0(OutPath, var, "_QLGM_Traceplot_Older.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod2, pars = 1:13, plot.type = "trace")
    dev.off()

    # Obtain Gelman-Rubin Diagnostic and export plots

    mcmc.list1 <- blavInspect(fit.mod1, what = "mcmc")
    gelmanRubin1 <- gelman.diag(mcmc.list1)

    mcmc.list2 <- blavInspect(fit.mod2, what = "mcmc")
    gelmanRubin2 <- gelman.diag(mcmc.list2)

    png(paste0(OutPath, var, "_LGM_GelmanRubinPlot_Older.png"), width = 1920, height = 1440, pointsize = 30)
    gelman.plot(mcmc.list1)
    dev.off()

    png(paste0(OutPath, var, "_QLGM_GelmanRubinPlot_Older.png"), width = 1920, height = 1440, pointsize = 30)
    gelman.plot(mcmc.list2)
    dev.off()

    # Make posterior histogram plots and export

    png(paste0(OutPath, var, "_LGM_PostHist_Older.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod1, pars = 1:10, plot.type = "hist")
    dev.off()

    png(paste0(OutPath, var, "_QLGM_PostHist_Older.png"), width = 1920, height = 1440, pointsize = 60)
    plot(fit.mod2, pars = 1:13, plot.type = "hist")
    dev.off()

    # Make autocorrelation plots and export

    png(paste0(OutPath, var, "_LGM_AutocorPlot_Older.png"), width = 4000, height = 3000, pointsize = 60)
    par(mfrow = c(2,2))
    plot(fit.mod1, pars = 1:10, plot.type = "acf")
    dev.off()

    png(paste0(OutPath, var, "_QLGM_AutocorPlot_Older.png"), width = 4000, height = 3000, pointsize = 60)
    par(mfrow = c(2,2))
    plot(fit.mod2, pars = 1:13, plot.type = "acf")
    dev.off()

    # Make posterior density plots and export

    p1 <- mcmc_dens_overlay(mcmc.list1)
    ggsave(paste0(OutPath, var, "_LGM_PostDensity_Older.png"), plot = p1)

    p2 <- mcmc_dens_overlay(mcmc.list2)
    ggsave(paste0(OutPath, var, "_QLGM_PostDensity_Older.png"), plot = p2)
    
    # Make summary text file and save

    Indices.mod1 <- blavFitIndices(fit.mod1, baseline.model = fit.null)
    Indices.mod2 <- blavFitIndices(fit.mod2, baseline.model = fit.null)

    sink(paste0(OutPath, var, "_GrowthModels_Older.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1, fit.mod2))
    sink()

    # Make summary for default priors and save

    Indices.mod1.default <- blavFitIndices(fit.mod1.default, baseline.model = fit.null)
    Indices.mod2.default <- blavFitIndices(fit.mod2.default, baseline.model = fit.null)

    mcmc.default.list1 <- blavInspect(fit.mod1.default, what = "mcmc")
    gelmanRubin1.default <- gelman.diag(mcmc.default.list1)

    mcmc.default.list2 <- blavInspect(fit.mod2.default, what = "mcmc")
    gelmanRubin2.default <- gelman.diag(mcmc.default.list2)

    sink(paste0(OutPath.default, var, "_GrowthModels_Older.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1.default))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1.default, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1.default)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2.default))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2.default, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2.default)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1.default, fit.mod2.default))
    sink()

    # Make summary for double iterations and save

    Indices.mod1.dblits <- blavFitIndices(fit.mod1.dblits, baseline.model = fit.null)
    Indices.mod2.dblits <- blavFitIndices(fit.mod2.dblits, baseline.model = fit.null)

    mcmc.dblits.list1 <- blavInspect(fit.mod1.dblits, what = "mcmc")
    gelmanRubin1.dblits <- gelman.diag(mcmc.dblits.list1)

    mcmc.dblits.list2 <- blavInspect(fit.mod2.dblits, what = "mcmc")
    gelmanRubin2.dblits <- gelman.diag(mcmc.dblits.list2)

    sink(paste0(OutPath.dblits, var, "_GrowthModels_Older.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1.dblits))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1.dblits, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1.dblits)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2.dblits))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2.dblits, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2.dblits)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1.dblits, fit.mod2.dblits))
    sink()

    # Make summary for strong variance priors and save

    Indices.mod1.variance <- blavFitIndices(fit.mod1.variance, baseline.model = fit.null)
    Indices.mod2.variance <- blavFitIndices(fit.mod2.variance, baseline.model = fit.null)
    
    mcmc.variance.list1 <- blavInspect(fit.mod1.variance, what = "mcmc")
    gelmanRubin1.variance <- gelman.diag(mcmc.variance.list1)

    mcmc.variance.list2 <- blavInspect(fit.mod2.variance, what = "mcmc")
    gelmanRubin2.variance <- gelman.diag(mcmc.variance.list2)

    sink(paste0(OutPath.variance, var, "_GrowthModels_Older.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1.variance))
    print("")
    print("Linear Model Fit Indices")
    print(summary(Indices.mod1.variance, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Linear Model Gelman-Rubin")
    print(gelmanRubin1.variance)
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2.variance))
    print("")
    print("Quadratic Model Fit Indices")
    print(summary(Indices.mod2.variance, central.tendency = c("mean","median","mode"), prob = .90))
    print("")
    print("Quadratic Model Gelman-Rubin")
    print(gelmanRubin2.variance)
    print("")
    print("Linear-Quadratic Model Comparson")
    print(blavCompare(fit.mod1.variance, fit.mod2.variance))
    sink()

    # Output indices posterior distribution histograms

    if (var != "ECOG12" && var != "CAIDE") {
    
        dist_fits.mod1 <- data.frame(Indices.mod1@indices)
        dist_fits.mod2 <- data.frame(Indices.mod2@indices)

        p1 <- mcmc_pairs(dist_fits.mod1, diag_fun = "hist")
        ggsave(paste0(OutPath, var, "_LGM_IndicesDistributions_Older.png"), plot = p1)

        p2 <- mcmc_pairs(dist_fits.mod2, diag_fun = "hist")
        ggsave(paste0(OutPath, var, "_QLGM_IndicesDistributions_Older.png"), plot = p2)

    }

    # Clean up big stuff - not sure how important this is since it will all be overwritten in the loop...
    rm(fit.mod1, fit.mod2, fit.null)
}

timer$stop("runtime")

sink(paste0(OutPath, "Runtime.txt"))
"Start time"
timer$getStartTime("runtime")
""
"Stop time"
timer$getStopTime("runtime")
""
"Elapsed Time"
timer$getTimeElapsed("runtime")
sink()


# Garbage Bin

             #q ~~ prior("beta(',QcovSA,',',QcovSB,')")*s
             #s ~~ prior("beta(',ScovIA,',',ScovIB,')")*i
             #i ~~ prior("beta(',QcovIA,',',QcovIB,')")*q

    # Covariances (Correlations)
    #QcovSA <- df.priors[df.priors$Parameter == "QcovS", paste0(var, "a")]
    #QcovSB <- df.priors[df.priors$Parameter == "QcovS", paste0(var, "b")]
    #ScovIA <- df.priors[df.priors$Parameter == "ScovI", paste0(var, "a")]
    #ScovIB <- df.priors[df.priors$Parameter == "ScovI", paste0(var, "b")]
    #QcovIA <- df.priors[df.priors$Parameter == "QcovI", paste0(var, "a")]
    #QcovIB <- df.priors[df.priors$Parameter == "QcovI", paste0(var, "b")]

    #pars = c("BRMSEA", "BGammaHat", "BCFI", "BTLI"), 