#!/bin/bash
# echo/printf colors
DEBUG='\033[0;32m[DEBUG] '
INFO='\033[0;37m[INFO] '
NC='\033[0m' # No Color
WARN='\033[0;33m[WARN] '

echo -e "${DEBUG}docker build image${NC}"
docker build -t tulin/fiftyone:$(cat version.txt) .

echo -e "${DEBUG}run the container${NC}"
docker run -v ${PWD}/fiftyone:/root/fiftyone --network host --name fiftyone -it tulin/fiftyone