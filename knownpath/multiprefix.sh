#!/bin/sh

while IFS= read -r LINE; do
	echo "$LINE"
	ip_addr=`nslookup $LINE | awk '{ print $2}' | tail -n 2 | head -n 1`
	ip_prefix=`whois -h v4.whois.cymru.com "-v $ip_addr" | awk '{print $5}' | tail -n 1`
	time python knownpath.py $ip_prefix &
done
