#!/bin/bash
make
#make all
cd ..
time icdiff --no-headers tests/output001.txt <(./goldbach_serial/bin/goldbach_serial < tests/input001.txt)
time icdiff --no-headers tests/output002.txt <(./goldbach_serial/bin/goldbach_serial < tests/input002.txt)
time icdiff --no-headers tests/output003.txt <(./goldbach_serial/bin/goldbach_serial < tests/input003.txt)
time icdiff --no-headers tests/output004.txt <(./goldbach_serial/bin/goldbach_serial < tests/input004.txt)
time icdiff --no-headers tests/output005.txt <(./goldbach_serial/bin/goldbach_serial < tests/input005.txt)
time icdiff --no-headers tests/output006.txt <(./goldbach_serial/bin/goldbach_serial < tests/input006.txt)
time icdiff --no-headers tests/output007.txt <(./goldbach_serial/bin/goldbach_serial < tests/input007.txt)
time icdiff --no-headers tests/output008.txt <(./goldbach_serial/bin/goldbach_serial < tests/input008.txt)
time icdiff --no-headers tests/output020.txt <(./goldbach_serial/bin/goldbach_serial < tests/input020.txt)
time icdiff --no-headers tests/output021.txt <(./goldbach_serial/bin/goldbach_serial < tests/input021.txt)
time icdiff --no-headers tests/output022.txt <(./goldbach_serial/bin/goldbach_serial < tests/input022.txt)
time icdiff --no-headers tests/output023.txt <(./goldbach_serial/bin/goldbach_serial < tests/input023.txt)




