#!/bin/sh

# check if python3
if [ ! $(type -p python3) ]; then
    echo "Error: \"python3\" not found"
    echo ""
    exit 1
fi

python3 ./code/interceptionCoreHandlerMain.py
