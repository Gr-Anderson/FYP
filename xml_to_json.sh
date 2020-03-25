#!/bin/sh

# finds the starting line for the ecg signal
startline=`grep "path clip" svg_image_test.svg -n | awk -F":" '{print $1+1}'`

# finds where the ecg signal stops
endline=`tail -n +$startline svg_image_test.svg | grep -n "L [0-9]" | tail -1 | awk -F":" '{print $1}'`

# using startline and endline, crops the entire ecg signal out of the svg file
tail +$startline svg_image_test.svg | head -$endline > tempfile

# creates the json file by starting an array
echo "[" > ecg.json

# converts the ecg signal into json format
sed 's/L /\{/g' tempfile | sed 's/ /, /g' | sed 's/, $/\},/g' >> ecg.json

# ammends the last line of the file to a variable
ammendedLastLine=`tail -1 ecg.json | sed 's/,$//'`

# removes the last line of the json file
sed -i '$d' ecg.json

# adds the ammended line back to the json file
echo $ammendedLastLine >> ecg.json

# closes the array on the json file
echo "]" >> ecg.json