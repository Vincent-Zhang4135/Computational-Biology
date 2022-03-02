# Example shell function definitions 
# Along with aliases, these can be inserted into your 
# .bash_profile to become available each time you open a shell

function listall {
  ls -la
  echo "Above are the directory listings for this folder:"
  pwd
  date
}

repeater(){	
 echo "$1 is what you said first"	
 echo "$@ is everything you said"	
}	

myphyml(){	
 echo "myphyml filename performs 100 bootstraps on AA data"	
 phyml $1 1 i 1 100 WAG 0 8 e BIONJ y y	
}	

myecho(){
 # same as above, but just echoes the command, doesn't run it
 echo "myphyml filename performs 100 bootstraps on AA data"	
 phyml $1 1 i 1 100 WAG 0 8 e BIONJ y y
}

phymlaa(){	
  BOOTS=100	
  if [ $2 ]	
  then	
    BOOTS=$2	
  fi      	
  phyml $1 1 i 1 $BOOTS WAG 0 8 e BIONJ y y	
}	


blastx(){	
 echo "Blasting protein vs swissprot..."; date;	
 echo $1 | blastall -d swissprot -p blastp -m 8 -i stdin	
}	

unix2mac(){	
# this line test if the number of arguments is zero	
if [ $# -lt 1 ]	
then	
    echo "convert mac to unix end of line"	
else	
        tr '\r' '\n' < "${1}" > u_"${1}"	
        echo "converting ${1} to u_${1}"	
fi	
}


 renamer(){	
  # Edit these to change how this works	
  EXT="dat"	
  PRE="u_"	
  if [ $# -lt 1 ]	
  then	
    echo "Rename a file.txt list as $PREfile.$EXT"	
  else	
    for FILENAME in "$@" 	
      do   	
        ROOTNAME="${FILENAME%.*}"	
        	
        cp "$FILENAME" "$PRE$ROOTNAME.$EXT"	
      echo "Copying $FILENAME to $PRE$ROOTNAME.$EXT"	
      done 	
  fi	
}