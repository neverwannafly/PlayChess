#!/bin/sh

runscript() {
    file_path="scripts/$1"
    source $file_path
}

main() {
    if [ $# -lt 1 ]
    then 
        echo ERROR: Invalid Arguments
        exit 1
    fi
    if [ $1 = "dev" ]
    then
        runscript "rundev.sh"
    elif [ $1 = "commitall" ]
    then
        runscript "commitall.sh"
    elif [ $1 = "logs" ]
    then
        runscript "logs.sh"
    else
        echo ERROR: Unrecognised Command!
        exit -1
    fi
}

main $1