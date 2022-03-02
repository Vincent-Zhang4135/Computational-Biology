####### Albert Nam  #######
####### 24 May 2017 #######

### Description ###

# Pairwise alignment function allowing for Needleman-Wunsch (type = "global") and
# Smith-Waterman (type = "local") type alignments with affine gap penalties via the 
# Gotoh algorithm with corrections from the following paper:

## Flouri, T., Kobert, K., Rognes, T., & Stamatakis, A. (2015). 
## "Are all global alignment algorithms and implementations correct?"
## http://biorxiv.org/content/early/2015/11/12/031500.abstract

### Arguments and usage ###

# `seq1` and `seq2` are concatenated uppercase sequence strings (i.e. "GAATTC")

# `substitutionMatrix` can have character values to access AA substitution matrices
# that are contained in the package "Biostrings" such as "BLOSUM62" or "PAM120"; see
# `data(package = "Biostrings")`. In addition to this, `substitutionMatrix` can be a
# named numeric matrix (like those created by nucleotideSubstitutionMatrix() from 
# the package Biostrings), which will be used as the lookup table for pairwise match
# scoring. Other datatypes are not accepted and will return a warning message.

# `gapOpening` is the gap opening penalty. A gap of length 1 will be assessed both 
# the gap opening and gap extension penalties. For a linear gap penalty, only 
# gapExtension need be provided.

# `gapExtension` is the gap extension penalty. In the absence of a declared value
# for `gapOpening`, this will be the penalty assessed against all gap positions.
# This allows for a linear gap penalty without explicitly declaring a value for
# the gap opening penalty.

# `type` takes character values of "global" or "local" to determine whether a global
# Needleman-Wunsch type alignment or a local Smith Waterman type alignment is done,
# respectively. Default value is "global".

# `scoreOnly = TRUE` will return only the alignment score as a double. This is 
# faster, as it skips the computation for traceback steps. Default value is FALSE.

## ** EXAMPLE: Global nucleotide seq. alignment with a match score of 3, a mismatch
## ** score of -1, a gap opening penalty of -8, and a gap extension penalty of -2:
## > pairAlign("AGTCGAT", "AGCCTCGATT", nucleotideSubstitutionMatrix(3, -1), -8, -2)

# Output has the form of a named 3-element list object. First element `$Pattern` is
# a char containing the alignment of `seq1`. Second element `$Subject` is a char
# containing the alignment of `seq2`. Third element `$Score` is a double containing 
# the alignment score. For the example given above, the output is as follows:

## $Pattern
## [1] "AG--TCGA-T"
## 
## $Subject
## [1] "AGCCTCGATT"
## 
## $Score
## [1] -1

pairAlign <- function(seq1, seq2, substitutionMatrix, gapOpening = gapExtension, gapExtension, type = "global", scoreOnly = FALSE){
    # require `Biostrings` package to access AA substitution matrix data
    suppressMessages(require(Biostrings, quietly = TRUE))
    
    ## Load and process sequence strings, abbreviate gap penalty variables
    seq1Char <- strsplit(seq1, "")[[1]]
    seq2Char <- strsplit(seq2, "")[[1]]
    size1 <- length(seq1Char)
    size2 <- length(seq2Char)
    if(missing(gapOpening)){
        gOpen <- -gapOpening
    } else {
        gOpen <- -gapOpening-gapExtension
    }
    gExt <- -gapExtension
    
    ## Detect and assign substitution matrix for scoring
    if(class(substitutionMatrix) == "character"){
        lut <- get(data(list = substitutionMatrix))
    } else if(class(substitutionMatrix) == "matrix" && !is.null(dimnames(substitutionMatrix))){
        lut <- substitutionMatrix
    } else {
        return("Invalid Substitution Matrix Format!")
    }
    
    ## Generate scoring matrix from substitution matrix and sequences
    scoreMat <- as.matrix(lut[seq1Char, seq2Char])
    
    ## Allocate diagonal and affine gap arrays for alignment (dim 3 index 1) 
    ## and traceback (dim 3 index 2) matrices
    diagScore <- array(0, c(size1 + 1, size2 + 1, 2)) #dimensions are N+1 by M+1 by 2
    vertGap <- array(0, c(size1 + 1, size2 + 1, 2))
    horizGap <- array(0, c(size1 + 1, size2 + 1, 2))
    
    ## General initialization for NW/SW
    diagScore[1, ,1] <- -Inf
    diagScore[ ,1,1] <- -Inf
    diagScore[1,1,1] <- 0
    
    vertGap[1, ,1] <- -Inf
    horizGap[ ,1,1] <- -Inf
    
    ## Populate NW matrix
    if(type == "global"){
        # initialize diagonal traceback matrix
        diagScore[1, ,2] <- 3
        diagScore[ ,1,2] <- 2
        
        # initialize vertical gap array for NW and traceback
        if(gExt == 0){
            if(gOpen != 0){
                vertGap[ ,1,1] <- -gOpen
            }
        } else {
            vertGap[ ,1,1] <- c(-Inf, seq(-gOpen, (-gExt*(size1-1)-gOpen), -gExt))
        }
        vertGap[2, ,1] <- -gOpen
        vertGap[ ,1,2] <- 3
        vertGap[1, ,2] <- 1
        
        # initialize horizontal gap array for NW and traceback
        if(gExt == 0){
            if(gOpen != 0){
                horizGap[1, ,1] <- -gOpen
            }
        } else {
            horizGap[1, ,1] <- c(-Inf, seq(-gOpen,(-gExt*(size2-1)-gOpen),-gExt))
        }
        horizGap[ ,2,1] <- -gOpen
        horizGap[ ,1,2] <- 1
        horizGap[1, ,2] <- 3
        
        if(scoreOnly){ #If scoreOnly == TRUE, do not populate traceback matrices
            for(i in 2:nrow(diagScore)){
                for(j in 2:ncol(diagScore)){
                    # diagonals matrix
                    opt <- c(diagScore[i-1,j-1,1], vertGap[i-1,j-1,1], horizGap[i-1,j-1,1]) + scoreMat[i-1,j-1]
                    diagScore[i,j,1] <- max(opt)
                    # vertical gap matrix (gap in sequence 2)
                    opt <- c(c(diagScore[i-1,j,1], horizGap[i-1,j,1]) - gOpen, vertGap[i-1,j,1] - gExt)
                    vertGap[i,j,1] <- max(opt)
                    # horizontal gap matrix (gap in sequence 1)
                    opt <- c(c(diagScore[i,j-1,1], vertGap[i,j-1,1]) - gOpen, horizGap[i,j-1,1] - gExt)
                    horizGap[i,j,1] <- max(opt)
                }
            }
        } else { #Otherwise, fill traceback matrices and store which matrix to begin traceback in
            for(i in 2:nrow(diagScore)){
                for(j in 2:ncol(diagScore)){
                    # diagonals matrix
                    opt <- c(diagScore[i-1,j-1,1], vertGap[i-1,j-1,1], horizGap[i-1,j-1,1]) + scoreMat[i-1,j-1]
                    diagScore[i,j,1] <- max(opt)
                    diagScore[i,j,2] <- which.max(opt)
                    # vertical gap matrix (gap in sequence 2)
                    opt <- c(c(diagScore[i-1,j,1], horizGap[i-1,j,1]) - gOpen, vertGap[i-1,j,1] - gExt)
                    vertGap[i,j,1] <- max(opt)
                    vertGap[i,j,2] <- which.max(opt)
                    # horizontal gap matrix (gap in sequence 1)
                    opt <- c(c(diagScore[i,j-1,1], vertGap[i,j-1,1]) - gOpen, horizGap[i,j-1,1] - gExt)
                    horizGap[i,j,1] <- max(opt)
                    horizGap[i,j,2] <- which.max(opt)
                }
            }
            mat <- which.max(c(diagScore[i,j,1], vertGap[i,j,1], horizGap[i,j,1]))
        }
        score <- max(diagScore[i,j,1], vertGap[i,j,1], horizGap[i,j,1])
        
    ## Populate SW matrix
    } else if(type == "local"){
        # initialize diagonal, vertical, and horizontal traceback matrices for SW
        diagScore[1, ,2] <- 4 #value of 4 in the traceback matrix tells the traceback routine to break
        diagScore[ ,1,2] <- 4
        vertGap[ ,1,2] <- 4
        vertGap[1, ,2] <- 4
        horizGap[ ,1,2] <- 4
        horizGap[1, ,2] <- 4
        # SW matrix generation; same method as NW but 0 is now a candidate for max
        if(scoreOnly){
            for(i in 2:nrow(diagScore)){
                for(j in 2:ncol(diagScore)){
                    opt <- c(c(diagScore[i-1,j-1,1], vertGap[i-1,j-1,1], horizGap[i-1,j-1,1]) + scoreMat[i-1,j-1], 0)
                    diagScore[i,j,1] <- max(opt)
                    diagScore[i,j,2] <- which.max(opt)
                    opt <- c(c(diagScore[i-1,j,1], horizGap[i-1,j,1]) - gOpen, vertGap[i-1,j,1] - gExt, 0)
                    vertGap[i,j,1] <- max(opt)
                    vertGap[i,j,2] <- which.max(opt)
                    opt <- c(c(diagScore[i,j-1,1], vertGap[i,j-1,1]) - gOpen, horizGap[i,j-1,1] - gExt, 0)
                    horizGap[i,j,1] <- max(opt)
                    horizGap[i,j,2] <- which.max(opt)
                }
            }
        } else {
            for(i in 2:nrow(diagScore)){
                for(j in 2:ncol(diagScore)){
                    opt <- c(c(diagScore[i-1,j-1,1], vertGap[i-1,j-1,1], horizGap[i-1,j-1,1]) + scoreMat[i-1,j-1], 0)
                    diagScore[i,j,1] <- max(opt)
                    diagScore[i,j,2] <- which.max(opt)
                    opt <- c(c(diagScore[i-1,j,1], horizGap[i-1,j,1]) - gOpen, vertGap[i-1,j,1] - gExt, 0)
                    vertGap[i,j,1] <- max(opt)
                    vertGap[i,j,2] <- which.max(opt)
                    opt <- c(c(diagScore[i,j-1,1], vertGap[i,j-1,1]) - gOpen, horizGap[i,j-1,1] - gExt, 0)
                    horizGap[i,j,1] <- max(opt)
                    horizGap[i,j,2] <- which.max(opt)
                }
            }
            # only really concerned with diagScore; no end gaps for local alignments. 
            # But for rigor's sake, will detect which matrix holds the high score and assign appropriately
            mat <- which.max(c(max(diagScore), max(vertGap), max(horizGap)))
            if(mat == 1){
                highScore <- which(diagScore == max(diagScore), arr.ind = TRUE)
            } else if(mat == 2){
                highScore <- which(vertGap == max(vertGap), arr.ind = TRUE)
            } else if(mat == 3){
                highScore <- which(horizGap == max(horizGap), arr.ind = TRUE)
            }
            
            # set indices i and j to position of highest score in matrix
            i <- highScore[1,1]
            j <- highScore[1,2]
        }
        score <- max(c(max(diagScore), max(vertGap), max(horizGap)))
    }
    rm(scoreMat)
    if(scoreOnly == TRUE){
        return(score)
    } else {
    ## Traceback routine
        
        # condense arrays, only storing the traceback matrices
        diagTrace <- diagScore[,,2]
        rm(diagScore) #array cleanup
        vertTrace <- vertGap[,,2]
        rm(vertGap)
        horizTrace <- horizGap[,,2]
        rm(horizGap)
        
        # initialize empty chars to store growing alignments
        align1 <- character(size1+size2)
        align2 <- character(size1+size2)
        index <- (size1+size2)
        
        while(i > 1 || j > 1){
            if(mat == 4){ #breaks main loop if SW algorithm hits 0
                break
            }
            
            # matrix loop for main alignment matrix
            while(mat == 1 && (i > 1 || j > 1)){
                # breaks out of matrix loop to main loop if SW algorithm hits 0
                if(diagTrace[i,j] == 4 && type == "local"){
                    mat <- 4
                    break
                } else if(diagTrace[i,j] == 2){
                    mat <- 2
                } else if(diagTrace[i,j] == 3){
                    mat <- 3
                }
                align1[index] <- seq1Char[i-1]
                align2[index] <- seq2Char[j-1]
                i <- i-1
                j <- j-1
                index <- index-1
            } 
            
            # matrix loop for vertical gap matrix (gap in seq 2)
            while(mat == 2 && (i > 1)){
                if(vertTrace[i,j] == 4 && type == "local"){ 
                    mat <- 4
                    break
                } else if(vertTrace[i,j] == 1){
                    mat <- 1
                } else if(vertTrace[i,j] == 2){
                    mat <- 3
                }
                align1[index] <- seq1Char[i-1]
                align2[index] <- "-"
                i <- i-1
                index <- index-1
            } 
            
            # matrix loop for horizontal gap matrix (gap in seq 1)
            while(mat == 3 && j > 1){
                if(horizTrace[i,j] == 4 && type == "local"){
                    mat <- 4
                    break
                } else if(horizTrace[i,j] == 1){
                    mat <- 1
                } else if(horizTrace[i,j] == 2){
                    mat <- 2
                }
                align1[index] <- "-"
                align2[index] <- seq2Char[j-1]
                j <- j-1
                index <- index-1
            }
        }
        
        ## Trim and concatenate alignments 
        align1 <- paste0(align1[(index+1):(size1+size2)], collapse = "")
        align2 <- paste0(align2[(index+1):(size1+size2)], collapse = "")
        
        ## Return named list
        output <- list(Pattern = align1, Subject = align2, Score = score)
        return(output)
    }
}