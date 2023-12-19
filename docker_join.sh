#!/usr/bin/env bash

IMG=uwwee/rpi-dogg:latest


containerid=$(docker ps -aqf "ancestor=${IMG}") && echo $containerid
xhost +
docker exec -it \
    --privileged \
    -e DISPLAY=${DISPLAY} \
    -e LINES="$(tput lines)" \
    ${containerid} \
    bash
xhost -
