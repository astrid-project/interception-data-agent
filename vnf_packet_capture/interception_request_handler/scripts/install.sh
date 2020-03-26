#!/bin/bash

# check if python3
if [ ! $(type -p python3) ]; then
    echo "Error: \"python3\" not found"
    echo ""
    exit 1
fi

# check if pip3 exist and execute pip3 requirements
if [ ! $(type -p pip3) ]; then
    echo "Error: \"pip3\" not found"
    echo ""
    exit 1
else
    pip3 install -r ./scripts/requirements.txt
fi

# download git repository
#if [ ! -d .git ]; then
#    echo Clone repository
#    rm -rf env/lcp
#    git clone https://astrid-dev:PDskARWrfWHSxJtk9yzQ@gitlab.com/astrid-repositories/wp2/interception-data-agent.git
#else
#    echo Pull repository
#    git pull origin master
#fi

