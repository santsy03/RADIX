#!/bin/bash
clear
params="$@"

SESSIONID="$RANDOM"${params// /}
DELIMITER=${params// /-}
FILE_NAME="1"${params// /-}".menu.log"

for var in "$@"
do
    echo ">>>> Input: $var"
    echo "----------------------------------------------------"
    ./client.py $SESSIONID $var
    echo "----------------------------------------------------"
done

