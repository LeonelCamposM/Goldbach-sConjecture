#include <stdio.h>
#include <stdlib.h>
#include "input_handler.h"
#include "common.h"

dynamic_array_t* read_input() {
  dynamic_array_t* input_numbers = (dynamic_array_t*)
    calloc(1, sizeof(dynamic_array_t));
  report_and_exit(input_numbers == NULL, "could not create GoldbachModel input array");
  array_init(input_numbers);

  // Reads the numbers from stdin
  int64_t newNumber = 0;
  while (scanf("%" SCNd64, &newNumber) == 1) {
    array_append(input_numbers, newNumber);
  }
  return input_numbers;
}

int verify_input(int64_t value) {
  int error = EXIT_SUCCESS;
  if ((0 <= value && value <= 5) ||
      (0 >= value && value >= -5)) {
    printf("%" PRIi64 ": NA\n", value);
    error = EXIT_FAILURE;
  }
  return error;
}

int64_t analyze_arguments(int argc, char* argv[]) {
  int error = EXIT_SUCCESS;
  int64_t input = 0;
  if (argc == 2) {
    if (sscanf(argv[1], "%zu", &input) != 1 || input <= 0) {
      error = EXIT_FAILURE;
      fprintf(stderr, "error: invalid thread count \n");
    }
  }
  assert(error != EXIT_FAILURE);
  return input;
}
