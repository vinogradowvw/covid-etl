#!/bin/bash
source .venv/bin/activate 
source .env

url="https://drive.google.com/uc?id=${CSV_2020}"
echo $url
gdown $url -O ./Data/data_2020.csv
