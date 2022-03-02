/* Albert Nam
 * 15 September 2017
 * Gotoh Algorithm for Rcpp
 */

// [[Rcpp::plugins(cpp11)]]

#include <Rcpp.h>
#include <limits>

const double NEG_INF = -std::numeric_limits<double>::infinity();

double findMaxScoreGlobal(double vert, double horiz, double diag);
Rcpp::List findMaxScoreLocal(Rcpp::NumericMatrix diagonalMatch);
void storeWhichMax(double top, double left, double diag, double& element, double& traceElement, bool global);
int findWhichMax(double top, double left, double diag);
Rcpp::List needlemanAffine(std::string pattern, std::string subject, Rcpp::NumericMatrix scoringMatrix, double gapOpening, double gapExtension, bool global);

// [[Rcpp::export]]
Rcpp::List needlemanAffine(std::string pattern, std::string subject, Rcpp::NumericMatrix scoringMatrix, double gapOpening, double gapExtension, bool global = true) {
    // Initialization of dynamic programming matrices
    Rcpp::NumericMatrix diagonalMatch(pattern.size() + 1, subject.size() + 1);
    Rcpp::NumericMatrix verticalGap(pattern.size() + 1, subject.size() + 1);
    Rcpp::NumericMatrix horizontalGap(pattern.size() + 1, subject.size() + 1);
    Rcpp::NumericMatrix diagonalTrace(pattern.size() + 1, subject.size() + 1);
	Rcpp::NumericMatrix verticalTrace(pattern.size() + 1, subject.size() + 1);
	Rcpp::NumericMatrix horizontalTrace(pattern.size() + 1, subject.size() + 1);
    
    for(int i = 1; i < diagonalMatch.nrow(); ++i) {
        diagonalMatch(i, 0) = NEG_INF;
    }
    for(int j = 1; j < diagonalMatch.ncol(); ++j) {
        diagonalMatch(0, j) = NEG_INF;
    }
    for(int j = 0; j < verticalGap.ncol(); ++j) {
        verticalGap(0, j) = NEG_INF;
    }
    for(int i = 0; i < horizontalGap.nrow(); ++i) {
        horizontalGap(i, 0) = NEG_INF;
    }
    if(global) {
		verticalGap(1, 0) = gapOpening + gapExtension;
		horizontalGap(0, 1) = gapOpening + gapExtension;
		verticalTrace(1, 0) = 1;
		horizontalTrace(0, 1) = 2;
		for(int i = 2; i < verticalGap.nrow(); ++i) {
			verticalGap(i, 0) = verticalGap(i - 1, 0) + gapExtension;
			verticalTrace(i, 0) = 1;
		}
		for(int j = 2; j < horizontalGap.ncol(); ++j) {
			horizontalGap(0, j) = horizontalGap(0, j - 1) + gapExtension;
			horizontalTrace(0, j) = 2;
		}
		for(int i = 1; i < diagonalMatch.nrow(); ++i) {
			diagonalTrace(i, 0) = 1;
		}
		for(int j = 1; j < diagonalMatch.ncol(); ++j) {
			diagonalTrace(0, j) = 2;
		}
		for(int j = 0; j < verticalGap.ncol(); ++j) {
			verticalTrace(0, j) = 3;
		}
		for(int i = 0; i < horizontalGap.nrow(); ++i) {
			horizontalTrace(i, 0) = 3;
		}
	} else {
		for(int i = 0; i < diagonalMatch.nrow(); ++i) {
		    diagonalTrace(i, 0) = 4;
		    verticalTrace(i, 0) = 4;
		    horizontalTrace(i, 0) = 4;
		}
		for(int j = 0; j < diagonalMatch.ncol(); ++j) {
		    diagonalTrace(0, j) = 4;
		    verticalTrace(0, j) = 4;
		    horizontalTrace(0, j) = 4;
		}
	}
    
    //Populate matrices
    for(int i = 1; i < diagonalMatch.nrow(); ++i) {
        for(int j = 1; j < diagonalMatch.ncol(); ++j) {
			double top;
			double left;
			double diag;
            top = verticalGap(i - 1, j - 1) + scoringMatrix(i - 1, j - 1);
            left = horizontalGap(i - 1, j - 1) + scoringMatrix(i - 1, j - 1);
            diag = diagonalMatch(i - 1, j - 1) + scoringMatrix(i - 1, j - 1);
            storeWhichMax(top, left, diag, diagonalMatch(i, j), diagonalTrace(i, j), global);
            top = verticalGap(i - 1, j) + gapExtension;
            left = horizontalGap(i - 1, j) + gapExtension + gapOpening;
            diag = diagonalMatch(i - 1, j) + gapExtension + gapOpening;
            storeWhichMax(top, left, diag, verticalGap(i, j), verticalTrace(i, j), global);
            top = verticalGap(i, j - 1) + gapExtension + gapOpening;
            left = horizontalGap(i, j - 1) + gapExtension;
            diag = diagonalMatch(i, j - 1) + gapExtension + gapOpening;
            storeWhichMax(top, left, diag, horizontalGap(i, j), horizontalTrace(i, j), global);
        }
    }
    int startingMatrix;
    if(global) {
        double finalScore = findMaxScoreGlobal(verticalGap(pattern.size(), subject.size()), horizontalGap(pattern.size(), subject.size()), diagonalMatch(pattern.size(), subject.size()));
    	startingMatrix = findWhichMax(verticalGap(pattern.size(), subject.size()), horizontalGap(pattern.size(), subject.size()), diagonalMatch(pattern.size(), subject.size()));
    	return Rcpp::List::create(diagonalTrace, verticalTrace, horizontalTrace, finalScore, startingMatrix);
    } else {
        startingMatrix = 3;
        Rcpp::List maxScoreAndPosition = findMaxScoreLocal(diagonalMatch);
        return Rcpp::List::create(diagonalTrace, verticalTrace, horizontalTrace, maxScoreAndPosition, startingMatrix);
    }
}

void storeWhichMax(double top, double left, double diag, double& element, double& traceElement, bool global) {
    if(!global) {
        if(top <= 0 && left <= 0 && diag <= 0) {
            element = 0;
            traceElement = 4;
            return;
        }
    }
    // 1 is top, 2 is left, 3 is diagonal
    if(top >= left) { // left <= top; ?diag
        if(top >= diag) { // {left, diag} <= top; top is max
            element = top;
            traceElement = 1;
        } else { // left <= top < diag; diag is max
            element = diag;
            traceElement = 3;
        }
    } else { // top < left
        if(left >= diag) { // {top, diag} <= left; left is max
        	element = left;
        	traceElement = 2;
        } else { // top < left < diag; diag is max
        	element = diag;
        	traceElement = 3;
        }
    }
}

int findWhichMax(double top, double left, double diag) {
    // 1 is top, 2 is left, 3 is diagonal
    if(top >= left) { // left <= top; ?diag
        if(top >= diag) { // {left, diag} <= top; top is max
            return 1;
        } else { // left <= top < diag; diag is max
            return 3;
        }
    } else { // top < left
        if(left >= diag) { // {top, diag} <= left; left is max
            return 2;
        } else { // top < left < diag; diag is max
            return 3;
        }
    }
}

double findMaxScoreGlobal(double vert, double horiz, double diag) {
    double maxScore = std::numeric_limits<double>::lowest();
    if(diag > maxScore) {
        maxScore = diag;
    }
    if(vert > maxScore) {
        maxScore = vert;
    }
    if(horiz > maxScore) {
        maxScore = horiz;
    }
    return maxScore;
}

Rcpp::List findMaxScoreLocal(Rcpp::NumericMatrix diagonalMatch) {
    double maxScore = std::numeric_limits<double>::lowest();
    int maxRow = -1;
    int maxCol = -1;
    for(int i = 0; i < diagonalMatch.nrow(); ++i) {
        for(int j = 0; j < diagonalMatch.ncol(); ++j) {
            if(diagonalMatch(i, j) > maxScore) {
                maxScore = diagonalMatch(i, j);
                maxRow = i + 1;
                maxCol = j + 1;
            }
        }
    }
    return(Rcpp::List::create(maxScore, maxRow, maxCol));
}