#include "input_handler.h"

int main(int argc, char* argv[]) {
  int error = EXIT_SUCCESS;
  error = start();
  return error;
}

int start(){
  int error = EXIT_SUCCESS;
  int64_t value = 0;
  while (fscanf(stdin, "%" SCNd64, &value) == 1) {
    error = verify_input(value);
    if (error == EXIT_SUCCESS) {
      int64_t threads = analyze_arguments(argc, argv);
      start(value, threads);
    }
  }
return error;
}