library(ggcorrplot)
library(plotly)
library(GGally)
library(QuantPsyc)

data <- read.csv("D:\\Anaconda\\Scripts\\My Scripts\\Dissertation\\PowerAgingAim3.csv")

OutPath <- "D:\\Anaconda\\Scripts\\My Scripts\\Dissertation\\Output\\Aim3\\"

# df.mn <- subset(data, select = c(paste0(m1), paste0(m2), paste0(m3), paste0(m4)))

# Check multivariate normality

# mn <- mult.norm(df.mn)

# sink(paste0(OutPath, var, "MultNorm.txt"))
# mn
# sink()

# print(head(data))

corDataBiomotor <- data[, c('MBThrow', 'TENDO_PP', 'CMJ', 'HandGrip', 'ArmCurl', 'Zipper', 'SitReach', 'X6MW', 'TotalWork', 'PFQ_Scaled', 'SPPB', 'PPT7')]

corDataBiomotor <- na.omit(corDataBiomotor)

corDataPerformance <- data[, c('TUG', 'StairClimb', 'X5STS', 'X4mWalk', 'PFQ_Scaled', 'SPPB', 'PPT7')]

corDataPerformance <- na.omit(corDataPerformance)

p1 <- ggpairs(corDataBiomotor, title="Correlatons and Scatter Plots", upper = list(continuous = wrap('cor', size = 3))) + 
    theme_linedraw(base_size = 5) +
    theme(axis.text.x=element_blank(), 
      axis.ticks.x=element_blank(), 
      axis.text.y=element_blank(), 
      axis.ticks.y=element_blank(),
      panel.grid.major = element_blank(), 
      panel.grid.minor = element_blank(),
      strip.text.x = element_text(size = 6.5),
      strip.text.y = element_text(size = 6.5)) 

ggsave(paste0(OutPath, "CorrelationScattersBiomotor.png"), plot = p1)

p2 <- ggpairs(corDataPerformance, title="Correlatons and Scatter Plots") + theme_linedraw() +
    theme(axis.text.x=element_blank(), 
      axis.ticks.x=element_blank(), 
      axis.text.y=element_blank(), 
      axis.ticks.y=element_blank(),
      panel.grid.major = element_blank(), 
      panel.grid.minor = element_blank()) 

ggsave(paste0(OutPath, "CorrelationScattersPerformance.png"), plot = p2)