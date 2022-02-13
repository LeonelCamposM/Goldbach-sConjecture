#include <stdio.h>
#include <stdlib.h>
#include "input_handler.h"

dynamic_array_t* read_input() {
  dynamic_array_t* input_numbers = (dynamic_array_t*)
    calloc(1, sizeof(dynamic_array_t));
  report_and_exit(input_numbers == NULL, "could not create GoldbachModel input array");
  array_init(input_numbers);
  return input_numbers;
}

int verify_input(int64_t value) {
  int error = EXIT_SUCCESS;
  if ((0 <= value && value <= 5) ||
      (0 >= value && value >= -5)) {
    error = EXIT_FAILURE;
  }
  return error;
}

int write_output(char* mesage, size_t number, bool number_flag){
  FILE *file = fopen("Output.txt", "a+");
  if (file == NULL) {
      printf("cannot open output");
      return 1;
  }else{
    if(number_flag == false){
      fprintf(file, "%s", mesage);
    }else{
      char str_number[100];
      sprintf(str_number, "%li", number);
      fprintf(file, "%s", str_number);
    }
  }
  fclose(file);
  return 0;
}