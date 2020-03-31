#echo "[" > tempfile
ls -l *.dat | awk '{print $9}' | sed 's/.dat/ /g' > tempfile
#echo "]" >> tempfile
