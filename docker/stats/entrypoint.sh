#!/bin/bash

cd ./scripts/ && python ./metadata_stats.py all -dt $1 $2 && python ./metadata_stats_stats.py all -dt $1 $2