# Loop over each line in the file
for Line in InFile:
	# Check the line number, process if you are past the first line (number == 0)
	if LineNumber > 0:
				# Remove the line ending characters
		# print line  # uncomment for debugging
		Line = Line.strip('\n')
		# Split the line into a list of ElementList, using tab as a delimiter
		ElementList = Line.split('\t')
		# Returns a list in this format:
		# ['Tiburon 596', '19-Jul-03', '36 36.12 N', '122 22.48 W', '1190', 'holotype']

		Dive    = ElementList[0] # includes vehicle and dive number
		Date    = ElementList[1]
		Depth   = float(ElementList[4])
		Comment = ElementList[5]

		LatDegrees = decimalat(ElementList[2])
		LonDegrees = decimalat(ElementList[3])
		
		#Isolate the vehicle and dive number from the Dive field
		SearchStr='(.+?) (\d+)'
		Result = re.search(SearchStr, Dive)
		Vehicle = Result.group(1)
		DiveNum = int(Result.group(2))
		
		#Reformat date
		DateParsed = datetime.strptime(Date, "%d-%b-%y") # Create a datetime object from a string
		DateOut = DateParsed.strftime("%Y-%m-%d") # Create a string from a datetime object
		
		print Vehicle, DiveNum, DateOut, LatDegrees, LonDegrees, Depth, Comment
		
	LineNumber += 1 # This is outside the if, but inside the for loop