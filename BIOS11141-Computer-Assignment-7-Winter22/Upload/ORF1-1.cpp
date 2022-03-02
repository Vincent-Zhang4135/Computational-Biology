/* Albert Nam
 * 6 October 2017
 * ORF Finder for Rcpp
 */

// [[Rcpp::plugins(cpp11)]]

#include <Rcpp.h>
#include <vector>
#include <string>

Rcpp::List findORF(Rcpp::CharacterVector sequence, unsigned int minLength);
bool isStartCodon(std::string codon);
bool isStopCodon(std::string codon);
std::string paste(Rcpp::CharacterVector charVec);

// [[Rcpp::export]]
Rcpp::List findORF(Rcpp::CharacterVector sequence, unsigned int minLength) {
    std::vector<int> ORFStart;
    std::vector<int> ORFStop;
    unsigned int numCodons;
    std::string seqString = paste(sequence);
    for(unsigned char frame = 0; frame < 3; ++frame) {
        size_t indexStart = frame;
        while(indexStart < seqString.size()) {
            if(isStartCodon(seqString.substr(indexStart, 3))) {
                numCodons = 2;
                for(size_t indexStop = indexStart + 3; indexStop < seqString.size() - 2; indexStop += 3) {
                    if(isStopCodon(seqString.substr(indexStop, 3))) {
                        if(numCodons >= minLength) {
                            ORFStart.emplace_back(indexStart + 1);
                            ORFStop.emplace_back(indexStop + 3);
                        }
                        indexStart = indexStop;
                        break;
                    }
                    ++numCodons;
                }
            }
            indexStart += 3;
        }
    }
    return Rcpp::List::create(ORFStart, ORFStop);
}

bool isStartCodon(std::string codon) {
    return codon.compare("atg") == 0;
}

bool isStopCodon(std::string codon) {
    return codon.compare("taa") == 0 || codon.compare("tag") == 0 || codon.compare("tga") == 0;
}

std::string paste(Rcpp::CharacterVector charVec) {
    std::string pasted;
    pasted.reserve(charVec.length());
    for(size_t i = 0; i < charVec.size(); ++i) {
        pasted.push_back(Rcpp::as<char>(charVec[i]));
    }
    return pasted;
}

// [[Rcpp::export]]
Rcpp::CharacterVector compStrand(Rcpp::CharacterVector sequence) {
    Rcpp::CharacterVector comp(sequence.size());
    for(size_t i = 0; i < sequence.size(); ++i) {
        comp[comp.size() - i - 1] = sequence[i];
    }
    return comp;
}