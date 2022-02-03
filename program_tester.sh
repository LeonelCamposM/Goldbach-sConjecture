#!/bin/bash

# show menu
echo " "
echo "Select the program number to apply tests"
echo "1) goldbach_serial"
echo "2) goldbach_pthread"
echo "3) goldbach_omp)"
echo " "
echo -n number: 
read program_id

# ask for program_name
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
   *)
     program_name="goldbach_omp"
     ;;
esac

# make the program
cd $program_name
make
cd ..

# show results
clear
echo " "
echo "Results for $program_name"
time icdiff --no-headers tests/output001.txt <(./$program_name/bin/$program_name < tests/input001.txt)
time icdiff --no-headers tests/output002.txt <(./$program_name/bin/$program_name < tests/input002.txt)
time icdiff --no-headers tests/output003.txt <(./$program_name/bin/$program_name < tests/input003.txt)
time icdiff --no-headers tests/output004.txt <(./$program_name/bin/$program_name < tests/input004.txt)
time icdiff --no-headers tests/output005.txt <(./$program_name/bin/$program_name < tests/input005.txt)
time icdiff --no-headers tests/output006.txt <(./$program_name/bin/$program_name < tests/input006.txt)
time icdiff --no-headers tests/output007.txt <(./$program_name/bin/$program_name < tests/input007.txt)
time icdiff --no-headers tests/output008.txt <(./$program_name/bin/$program_name < tests/input008.txt)
time icdiff --no-headers tests/output020.txt <(./$program_name/bin/$program_name < tests/input020.txt)
time icdiff --no-headers tests/output021.txt <(./$program_name/bin/$program_name < tests/input021.txt)
time icdiff --no-headers tests/output022.txt <(./$program_name/bin/$program_name < tests/input022.txt)
time icdiff --no-headers tests/output023.txt <(./$program_name/bin/$program_name < tests/input023.txt)

# delete binaries
cd $program_name
echo " "
make clean

