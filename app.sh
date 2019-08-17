#!/bin/sh

runscript() {
    file_path="scripts/$1"
    . $file_path
}

main() {
    if [ $# -lt 1 ]
    then 
        echo "Invalid Arguments"
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
    elif [ $1 == "prod" ]
    then
        runscript "runprod.sh"
    elif [ $1 == "shell" ]
    then
        runscript "shell.sh"
    elif [ $1 == "redis" ]
    then
        runscript "redis.sh"
    elif [ $1 == "celery" ]
    then
        runscript "celery.sh"
    elif [ $1 == "mongo" ]
    then
        runscript "mongo.sh"
    else
        exit -1
    fi
}

main $1