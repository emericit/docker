#!/bin/bash
docker build -t authentication:latest ./authentication
docker build -t authorization:latest  ./authorization
docker build -t content:latest        ./content
docker-compose up