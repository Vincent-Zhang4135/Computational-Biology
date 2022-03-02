findORF <- function(sequence, minLength) {
    ## initialize 3D array for codon to AA lookup table
    LUT <- array(
        data = strsplit("FLIVSPTAYHNDCRSGFLIVSPTAYHNDCRSGLLIVSPTAXQKEXRRGLLMVSPTAXQKEWRRG", "")[[1]], 
        dim = c(4, 4, 4) #for each dimension: indices 1, 2, 3, 4 correspond to t, c, a, g
    )
    
    ## encode nucleotides in sequence as integers to correspond to array indices; faster than hashing
    sequenceNumericCode <- as.integer(factor(sequence, levels = c("t", "c", "a", "g")))
    
    ## convert codons to AA sequence in each reading frame
    AASeqs <- vapply(1:3, function(i) {
        endIndex <- (3 * (length(sequence) - i + 1) %/% 3) + i - 1
        paste0(LUT[matrix(sequenceNumericCode[i:endIndex], ncol = 3, byrow = T)], collapse = "")
    }, "")
    
    ## build regex to detect ORFs, and then find matches
    pattern <- paste0("M[ACDEFGHIKLMNPQRSTVWY]{", minLength - 2, ",}X")
    readingFrameMatches <- gregexpr(pattern, AASeqs, perl = T)
    
    ## format data and output
    ORFs <- matrix(0, ncol = 3, nrow = 0)
    for(i in 1:3) {
        if(readingFrameMatches[[i]][1] > 0) {
            ORFs <- rbind(ORFs, cbind((readingFrameMatches[[i]] - 1) * 3 + i, attr(readingFrameMatches[[i]], "match.length") * 3, rep(i, length(readingFrameMatches[[i]]))))
        }
    }
    ORFs <- data.frame("Start" = ORFs[,1], "Stop" = ORFs[,1] + ORFs[,2] - 1, "Length" = ORFs[,2], "Frame" = ORFs[,3])
    colnames(ORFs) <- c("Start", "Stop", "Length", "Frame")
    return(ORFs)
}

compStrand <- function(sequence) {
    return(rev(chartr("atcg", "tagc", sequence)))
}