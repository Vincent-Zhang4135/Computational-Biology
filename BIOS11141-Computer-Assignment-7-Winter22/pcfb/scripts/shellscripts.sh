#### examples from chapter 5

# save all reports in one text file:
curl "http://www.wunderground.com/history/airport/MIA/1992/08/[01-30]/DailyHistory.html?&format=1" >> miamiweather.txt 

# save each month's report in its own numbered file 
curl "http://www.wunderground.com/history/airport/MIA/1979/[01-12]/01/DailyHistory.html?&format=1" -o Miami_1979_#1.txt

#### examples from chapter 6

# the lines to set your path in ~/.bash_profile
export PATH="$PATH:$HOME/scripts"
set -o noclobber

# general crossref search format
http://www.crossref.org/openurl/?title=Nature&date=2008&volume=452&spage=745&pid=demo@practicalcomputing.org

#  crossref search format returning XML
http://www.crossref.org/openurl/?title=Nature&date=2008&volume=452&spage=745&pid=demo@practicalcomputing.org&redirect=false&format=unixref

# reformatted for a regular expression
curl "http://www.crossref.org/openurl/?title=\1\&date=\2\&volume=\3\&spage=\4\&pid=demo@practicalcomputing.org\&redirect=false\&format=unixref" 