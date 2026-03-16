#!/bin/env bash

# example of download link: https://data.discogs.com/?download=data%2F2026%2Fdiscogs_20260301_artists.xml.gz
DATA_URL_STEM="https://data.discogs.com/?download=data%2F"$(date "+%Y")"%2Fdiscogs_"$(date "+%Y%m")"01_"
DUMP_TYPES="artists labels masters releases"

rm -rf "discogs_dumps/" # try to remove old dumps; won't error if it doesn't exist because of -f
mkdir "discogs_dumps/" # and then make new directory to store dumps


for dump_type in $DUMP_TYPES; do # run through DUMP_TYPES and construct the download url for each, appending it to discogs_dump_urls.txt
	echo "Dump type: $dump_type"
	dump_url="${DATA_URL_STEM}${dump_type}.xml.gz"
	wget "$dump_url" -O "discogs_dumps/discogs_$(date "+%Y%m")01_${dump_type}.xml.gz" # download all dumps in discogs_dump_urls.txt to discogs_dumps/
done

wget "${DATA_URL_STEM}CHECKSUM.txt" -O "discogs_dumps/CHECKSUM.txt" # grab checksum
cd discogs_dumps/ # and then go to verify checksum
if sha256sum -c CHECKSUM.txt; then
	echo "Checksum verification passed."
else
	echo "Checksum verification failed. Please check the downloaded files."
	exit 1
fi
cd .. # and move back to start