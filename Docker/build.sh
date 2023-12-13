#!/bin/bash

# docker build  --rm -t uwwee/rpi-dogg:lastest .
docker buildx build --load -t uwwee/rpi-dogg:lastest --platform linux/arm/v7 .