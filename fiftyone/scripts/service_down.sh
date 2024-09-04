#!/bin/bash
# echo/printf colors
DEBUG='\033[0;32m[DEBUG] '
INFO='\033[0;37m[INFO] '
NC='\033[0m' # No Color
WARN='\033[0;33m[WARN] '

echo -e "${WARN}stop the container${NC}"
docker stop fiftyone