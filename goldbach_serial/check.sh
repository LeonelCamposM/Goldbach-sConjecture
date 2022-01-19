#!/bin/bash
make
#make all
time icdiff --no-headers tests/output001.txt <(./bin/goldbach_serial < tests/input001.txt)
time icdiff --no-headers tests/output002.txt <(./bin/goldbach_serial < tests/input002.txt)
time icdiff --no-headers tests/output003.txt <(./bin/goldbach_serial < tests/input003.txt)
time icdiff --no-headers tests/output004.txt <(./bin/goldbach_serial < tests/input004.txt)
time icdiff --no-headers tests/output005.txt <(./bin/goldbach_serial < tests/input005.txt)
time icdiff --no-headers tests/output006.txt <(./bin/goldbach_serial < tests/input006.txt)
time icdiff --no-headers tests/output007.txt <(./bin/goldbach_serial < tests/input007.txt)
time icdiff --no-headers tests/output008.txt <(./bin/goldbach_serial < tests/input008.txt)
time icdiff --no-headers tests/output020.txt <(./bin/goldbach_serial < tests/input020.txt)
time icdiff --no-headers tests/output021.txt <(./bin/goldbach_serial < tests/input021.txt)
time icdiff --no-headers tests/output022.txt <(./bin/goldbach_serial < tests/input022.txt)
time icdiff --no-headers tests/output023.txt <(./bin/goldbach_serial < tests/input023.txt)
#perf stat ./bin/goldbach_serial < tests/input023.txt



