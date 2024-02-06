#! /bin/bash

clear && grep -Rn '"360"' $(find projects/ -name "*.json") |
while read LINE
do
	MMRE=$(echo $LINE | cut -d: -f4)
	PROJECT=$(echo $LINE | cut -d: -f1)
	echo $MMRE:$PROJECT
done | sort -n
