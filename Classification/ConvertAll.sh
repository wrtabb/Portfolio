#!/bin/bash

for i in $(seq 0 8);
do
	python3 ConvertROOTFiles.py --var_num $i
done
