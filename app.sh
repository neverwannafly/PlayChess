#!/bin/sh

runscript() {
    file_path="scripts/$1"
    source $file_path
}

main() {
    if [ $# -lt 1 ]
    then 
        echo "\33[1m\33[31mERROR: Invalid Arguments\033[0m\033[0m"
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
        echo "\33[1m\33[31mERROR: Unrecognised Command!\033[0m\033[0m"
        exit -1
    fi
}

main $1