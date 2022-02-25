
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
rm -rf goldbach_server/src/goldbach/bin
mv bin goldbach_server/src/goldbach

