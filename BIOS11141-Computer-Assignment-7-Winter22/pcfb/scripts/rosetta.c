#include <stdio.h> 

// rosetta.c from PCfB

char Let; 
int Num; 
int main(void){ 
 for (Let = 65; Let<= 72; Let++) { 
     for(Num = 1; Num <= 12; Num++) { 
   printf("%c%d ",Let,Num); 
  } 
  printf("\n"); 
 } 
 return 0; 
} 
