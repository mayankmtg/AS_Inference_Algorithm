#!/bin/sh

while IFS= read -r LINE; do
	echo "$LINE"
	python knownpath.py $LINE &
done
