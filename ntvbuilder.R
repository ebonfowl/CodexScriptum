df <- data.frame(matrix(ncol = 3, nrow = 0))

i <- 101

while (i < 131) {

    str1 <- "NTV"
    str2 <- as.character(i)
    str3 <- "_Validation_Flanker*.txt"
    str4 <- "_Validation_Go*.txt"

    pname <- paste(str1, str2, str3, sep = "")
    qname <- paste(str1, str2, str4, sep = "")

    pfile <- dir("d:/R/R-4.2.1/data/NTV", full.names = TRUE, pattern = glob2rx(pname))
    qfile <- dir("d:/R/R-4.2.1/data/NTV", full.names = TRUE, pattern = glob2rx(qname))

    if (isTRUE(file.size(pfile) > 0)) {

        data <- read.table(pfile)

        colnames(data) <- c("V1", "V2", "V3", "V4")

        data2 <- subset(data, V3 != 3)

        time <- sum(data2$V4) / 1000

        correct <- sum(data2$V3 == 1)

        flanker_score <- correct / time

        gngdata <- read.table(qfile)

        colnames(gngdata) <- c("V1", "V2", "V3")

        gngdata2 <- subset(gngdata, V3 != 1)

        gngtime <- sum(gngdata2$V2)

        gngcorrect <- sum(gngdata2$V3 == 0)

        gng_score <- gngtime / gngcorrect

        df <- rbind(df, c(i, flanker_score, gng_score))

    } else {

        df <- rbind(df, c(i, "", ""))

    }

    i <- i + 1
}

colnames(df) <- c("ID", "flanker_score", "gng_score")

write.csv(df, "d:/R/R-4.2.1/data/NTV/psytoolkit.csv", row.names = FALSE)