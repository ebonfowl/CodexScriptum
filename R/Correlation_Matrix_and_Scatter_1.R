library(ggcorrplot)
library(plotly)
library(GGally)

data <- read.csv("D:\\Anaconda\\Scripts\\My Scripts\\Dissertation\\PowerAgingAim2.csv")

OutPath <- "D:\\Anaconda\\Scripts\\My Scripts\\Dissertation\\Output\\Aim2\\"

corData <- data[, c('CMJ_PP', 'CMJ_PP_Est', 'STS_PP', 'TENDO_PP', 'PFQ', 'SPPB', 'PPT7')]

corData <- na.omit(corData)

corr <- round(cor(corData), 1)

p.mat <- cor_pmat(corData)

p1 <- ggcorrplot(corr, hc.order = TRUE, type = "lower", lab = TRUE) + theme_classic()

ggsave(paste0(OutPath, "CorrelationMatrix.png"), plot = p1)

p2 <- ggpairs(corData, title="Correlatons and Scatter Plots") + theme_linedraw() +
    theme(axis.text.x=element_blank(), 
      axis.ticks.x=element_blank(), 
      axis.text.y=element_blank(), 
      axis.ticks.y=element_blank(),
      panel.grid.major = element_blank(), 
      panel.grid.minor = element_blank()) 

ggsave(paste0(OutPath, "CorrelationScatters.png"), plot = p2)
