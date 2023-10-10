#Download numberbatch data

# URL to download
URL="https://conceptnet.s3.amazonaws.com/downloads/2019/numberbatch/numberbatch-19.08.txt.gz"

OUTPUT_FILE="numberbatch.txt.gz"

curl -o "$OUTPUT_FILE" "$URL"

# unzip the downloaded file
gunzip "$OUTPUT_FILE"
