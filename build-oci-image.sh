#!/usr/bin/env bash

docker builder prune --all --force
docker system prune --all --volumes --force

docker build -t hongsait/gha-webhook . --push
