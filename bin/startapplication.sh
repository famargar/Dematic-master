#!/bin/bash

cd ./dematic
python webserver.py  &

while true;

   do python check_data_DB.py --dir $(pwd)/static/images

   sleep 120

done
