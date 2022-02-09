#include <stdio.h>
#include <stdlib.h>
#include "input_handler.h"
#include "common.h"

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
