#!/bin/sh

filename="v102s.svg"
json_filename="v102s.json"
## finds the starting line for the ecg signal
startline=`grep "path clip" sampledata/$filename -n | awk -F":" '{print $1+1}'`

# finds where the ecg signal stops
endline=`tail -n +$startline sampledata/$filename | grep -n "L [0-9]" | tail -1 | awk -F":" '{print $1}'`

# using startline and endline, crops the entire ecg signal out of the svg file
tail +$startline sampledata/$filename | head -$endline > tempfile

# creates the json file by starting an array
echo "{" > $json_filename
echo "\t\"position\":" >> $json_filename
echo "\t\t[" >> $json_filename


# converts the ecg signal into json format
sed 's/L /\t\t\t\{\"x\"\:/g' tempfile | sed 's/ /, \"y\"\:/g' | sed 's/, \"y\"\:$/\},/g' >> $json_filename

# ammends the last line of the file to a variable
ammendedLastLine=`tail -1 $json_filename | sed 's/,$//'`

# removes the last line of the json file
sed -i '$d' $json_filename

# adds the ammended line back to the json file
echo "$ammendedLastLine" >> $json_filename

# closes the array on the json file
echo "\t\t]" >> $json_filename
echo "}" >> $json_filename