library(lavaan)
library(QuantPsyc)
library(tidyverse)
library(ggplot2)
library(dplyr)

data <- read.csv("D:\\DCM T4 Analyses\\DC-MARVEL_public_data.csv")

OutPath <- "D:\\Anaconda\\Scripts\\My Scripts\\DCM_LGM\\"

est <- "MLR" # Can change estimator for all analyses here,
            # maybe make this into an array so each var can have its own estimator,
            # or make a new csv with all vars and associated estimators

# Make a list of variable names without time designations

VarsList <- list("ANUADRI_TOTAL",
                 "ANUADRI_PROTECT",
                 "ANUADRI_RISK",
                 "ECOG12",
                 "CAIDE")
                 #"RBANS_ImmediateMemoryIndex",
                 #"RBANS_VisuospatialConstructionalIndex",
                 #"RBANS_LanguageIndex",
                 #"RBANS_AttentionIndex",
                 #"RBANS_DelayedMemoryIndex",
                 #"RBANS_TotalIndex",
                 #"NT_AttentionRaw",
                 #"NT_ExecutiveFunctionRaw",
                 #"NT_InhibitionRaw",
                 #"NT_ProcessingSpeedRaw",
                 #"NT_AssociativeLearningRaw",
                 #"NT_AssociativeMemoryRaw")
                 #"ANUADRI_TOTAL",
                 #"ANUADRI_PROTECT",
                 #"ANUADRI_RISK",
                 #"ECOG12",
                 #"CAIDE"

col_grid <- rgb(235, 235, 235, 100, maxColorValue = 255)

# Inside for loop below here

for (var in VarsList)
{
    # Concatonate strings and assign variable names to m1-m4

    m1 <- paste0(var, "_T1")
    m2 <- paste0(var, "_T2")
    m3 <- paste0(var, "_T3")
    m4 <- paste0(var, "_T4")

    # Make a new data frame with only m1-m4

    df.mn <- subset(data, select = c(paste0(m1), paste0(m2), paste0(m3), paste0(m4)))

    # Check multivariate normality

    mn <- mult.norm(df.mn)

    sink(paste0(OutPath, var, "MultNorm.txt"))
    print(mn)
    sink()

    # Define the models

    #linear growth model with covariate group
    mod1 <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ 0*',m1,' + 4*',m2,' + 12*',m3,' + 24*',m4,'
             i ~ group
             s ~ group')

    #quadratic growth model with covariate group
    mod2 <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ 0*',m1,' + 4*',m2,' + 12*',m3,' + 24*',m4,'
             q =~ 0*',m1,' + 16*',m2,' + 144*',m3,' + 576*',m4,'
             i ~ group
             s ~ group
             q ~ group')

    #centered quadratic growth model with covariate group
    mod3 <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ (-12)*',m1,' + (-8)*',m2,' + 0*',m3,' + 12*',m4,'
             q =~ 144*',m1,' + 64*',m2,' + 0*',m3,' + 144*',m4,'
             i ~ group
             s ~ group
             q ~ group')

    #cubic growth model with covariate group
    mod4 <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ 0*',m1,' + 4*',m2,' + 12*',m3,' + 24*',m4,'
             q =~ 0*',m1,' + 16*',m2,' + 144*',m3,' + 576*',m4,'
             c =~ 0*',m1,' + 64*',m2,' + 1728*',m3,' + 13824*',m4,'
             i ~ group
             s ~ group
             q ~ group
             c ~ group')

    #centered cubic growth model with covariate group
    mod5 <- paste0('i =~ 1*',m1,' + 1*',m2,' + 1*',m3,' + 1*',m4,'
             s =~ (-12)*',m1,' + (-8)*',m2,' + 0*',m3,' + 12*',m4,'
             q =~ 144*',m1,' + 64*',m2,' + 0*',m3,' + 144*',m4,'
             c =~ (-1728)*',m1,' + (-512)*',m2,' + 0*',m3,' + 1728*',m4,'
             i ~ group
             s ~ group
             q ~ group
             c ~ group')

    # Fit the models

    fit.mod1 <- growth(mod1, data = data, estimator = est)
    fit.mod2 <- growth(mod2, data = data, estimator = est)
    fit.mod3 <- growth(mod3, data = data, estimator = est)
    #fit.mod4 <- growth(mod4, data = data, estimator = est)
    #fit.mod5 <- growth(mod5, data = data, estimator = est)

    # Summarize fit models and export

    # R is a stupid language, I have to print() in a loop to make output available to the terminal and thus sink()

    sink(paste0(OutPath, var, "LGM.txt"))
    print("Linear LGM with Group Covariate")
    print(summary(fit.mod1, fit.measures = TRUE))
    print("")
    print("Quadratic LGM with Group Covariate")
    print(summary(fit.mod2, fit.measures = TRUE))
    print("")
    print("Centered Quadratic LGM with Group Covariate")
    print(summary(fit.mod3, fit.measures = TRUE))
    #print("")
    #print("Cubic LGM with Group Covariate")
    #print(summary(fit.mod4, fit.measures = TRUE))
    #print("")
    #print("Centered Cubic LGM with Group Covariate")
    #print(summary(fit.mod5, fit.measures = TRUE))
    #print("")
    sink()

    dfHC <- data[data$group == 1,]
    dfHE <- data[data$group == 0,]

    # Make means plot
    listMonth <- c(0,4,12,24)
    listMeans <- c(mean(data[[paste0(m1)]], na.rm = TRUE), mean(data[[paste0(m2)]], na.rm = TRUE), mean(data[[paste0(m3)]], na.rm = TRUE), mean(data[[paste0(m4)]], na.rm = TRUE))
    HCmeans <- c(mean(dfHC[[paste0(m1)]], na.rm = TRUE), mean(dfHC[[paste0(m2)]], na.rm = TRUE), mean(dfHC[[paste0(m3)]], na.rm = TRUE), mean(dfHC[[paste0(m4)]], na.rm = TRUE))
    HEmeans <- c(mean(dfHE[[paste0(m1)]], na.rm = TRUE), mean(dfHE[[paste0(m2)]], na.rm = TRUE), mean(dfHE[[paste0(m3)]], na.rm = TRUE), mean(dfHE[[paste0(m4)]], na.rm = TRUE))
    dfMeans <- data.frame(listMonth, listMeans)
    dfHCmeans <- data.frame(listMonth, HCmeans)
    dfHEmeans <- data.frame(listMonth, HEmeans)
    OverallMeans <- data.frame(listMeans, HCmeans, HEmeans)
    yMax <- max(OverallMeans, na.rm = TRUE)
    yMin <- min(OverallMeans, na.rm = TRUE)

    ggplot(dfMeans, aes(x=listMonth, y=listMeans)) + 
    geom_line(color = "#9000ff", linewidth = 2, lineend = "round") +
    geom_point(color = "#9000ff", size = 4) +
    geom_line(data = dfHCmeans, y = HCmeans, color = "#ff000093", linewidth = 2, lineend = "round") +
    geom_point(data = dfHCmeans, y = HCmeans, color = "#ff000093", size = 4) +
    geom_line(data = dfHEmeans, y = HEmeans, color = "#1e00ff96", linewidth = 2, lineend = "round") +
    geom_point(data = dfHEmeans, y = HEmeans, color = "#1e00ff96", size = 4) +
    ylim(yMin, yMax) +
    scale_x_continuous(limits = c(0, 24), breaks = seq(from = 0, to = 24, by = 4)) +
    theme_classic(base_size = 20) +
    labs(title = str_replace_all(var, "_", " "), y = "Score", # labels
        x = "Month") +
    theme(plot.title = element_text(hjust = 0.5, size=22, face= "bold", colour= "black"),
        axis.title.x = element_text(size=20, face="bold", colour = "black"),    
        axis.title.y = element_text(size=20, face="bold", colour = "black"),    
        axis.text.x = element_text(size=18, face="bold", colour = "black"), 
        axis.text.y = element_text(size=18, face="bold", colour = "black"), # bold
        strip.text.x = element_text(size = 16, face="bold", colour = "black" ),
        strip.text.y = element_text(size = 16, face="bold", colour = "black"),
        axis.line.x = element_line(color = "black", size = 1.2),
        axis.line.y = element_line(color = "black", size = 1.2)
    )

    ggsave(paste0(OutPath, var, "_MeansPlot.png"))

    # Make growth plots
    pred_lgm <- predict(fit.mod1)
    pred_qgm <- predict(fit.mod3)

    pred_lgm_long <- map(0:24, function(x) pred_lgm[, 1] + x * pred_lgm[, 2]) %>% 
        reduce(cbind) %>% # bring together the time predictions 
        as.data.frame() %>% # make data frame
        setNames(str_c(0:24)) %>% # give names to variables
        mutate(id = row_number()) %>% # make unique id
        gather(-id, key = month, value = pred) # make long format

    pred_lgm_long$month <- factor(pred_lgm_long$month,levels = unique(pred_lgm_long$month), ordered = TRUE)

    pred_qgm_long <- map(-12:12, function(x) pred_qgm[, 1] + x * pred_qgm[, 2] + x^2 * pred_qgm[, 3]) %>%
        reduce(cbind) %>% # bring together the time predictions 
        as.data.frame() %>% # make data frame
        setNames(str_c(0:24)) %>% # give names to variables
        mutate(id = row_number()) %>% # make unique id
        gather(-id, key = month, value = pred) # make long format

    pred_qgm_long$month <- factor(pred_qgm_long$month,levels = unique(pred_qgm_long$month), ordered = TRUE)

    pred_lgm_long %>% 
    ggplot(aes(month, pred, group = id)) + # what variables to plot?
    geom_line(alpha = 0.1) + # add a transparent line for each person
    scale_x_discrete(breaks = function(x){x[c(TRUE, FALSE, FALSE, FALSE)]}) +
    stat_summary( # add average line
        aes(group = 1),
        fun = mean,
        geom = "line",
        size = 1.5,
        color = "#FF00DD", 
        linewidth = 2, 
        lineend = "round"
    ) +
    theme_classic(base_size = 20) + # makes graph look nicer
    labs(title = str_replace_all(var, "_", " "), y = "Score", # labels
        x = "Month") +
    theme(plot.title = element_text(hjust = 0.5, size=22, face= "bold", colour= "black"),
        axis.title.x = element_text(size=20, face="bold", colour = "black"),    
        axis.title.y = element_text(size=20, face="bold", colour = "black"),    
        axis.text.x = element_text(size=18, face="bold", colour = "black"), 
        axis.text.y = element_text(size=18, face="bold", colour = "black"), # bold
        strip.text.x = element_text(size = 16, face="bold", colour = "black" ),
        strip.text.y = element_text(size = 16, face="bold", colour = "black"),
        axis.line.x = element_line(color = "black", size = 1.2),
        axis.line.y = element_line(color = "black", size = 1.2)
    )

    ggsave(paste0(OutPath, var, "_LinearGrowthPlot.png"))

    pred_qgm_long %>% 
    ggplot(aes(month, pred, group = id)) + # what variables to plot?
    geom_line(alpha = 0.1) + # add a transparent line for each person
    scale_x_discrete(breaks = function(x){x[c(TRUE, FALSE, FALSE, FALSE)]}) +
    stat_summary( # add average line
        aes(group = 1),
        fun = mean,
        geom = "line",
        size = 1.5,
        color = "#FF00DD", 
        linewidth = 2, 
        lineend = "round"
    ) +
    theme_classic(base_size = 20) + # makes graph look nicer
    labs(title = str_replace_all(var, "_", " "), y = "Score", # labels
        x = "Month") +
    theme(plot.title = element_text(hjust = 0.5, size=22, face= "bold", colour= "black"),
        axis.title.x = element_text(size=20, face="bold", colour = "black"),    
        axis.title.y = element_text(size=20, face="bold", colour = "black"),    
        axis.text.x = element_text(size=18, face="bold", colour = "black"), 
        axis.text.y = element_text(size=18, face="bold", colour = "black"), # bold
        strip.text.x = element_text(size = 16, face="bold", colour = "black" ),
        strip.text.y = element_text(size = 16, face="bold", colour = "black"),
        axis.line.x = element_line(color = "black", size = 1.2),
        axis.line.y = element_line(color = "black", size = 1.2)
    )

    ggsave(paste0(OutPath, var, "_QuadraticGrowthPlot.png"))
}