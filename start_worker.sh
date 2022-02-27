#!/bin/bash

# if does not work
# require ubuntu 20.04.3 or higher
# sed -i -e 's/\r$//' scriptname.sh

for program_id in $(seq 1 3); do
   program_name=" "
   case $program_id in
      1)
         program_name="goldbach_serial"
         ;;
      2)
         program_name="goldbach_pthread"
         ;;
      3)
         program_name="goldbach_omp"
         ;;
   esac
   echo " "
   echo "Making $program_name"
   make APPNAME=$program_name
done

echo " "
echo "Moving libraries to server"
clear
rm -rf goldbach_server/src/goldbach/bin
mv bin goldbach_server/src/goldbach

cd goldbach_server/src

python3 worker.py 

