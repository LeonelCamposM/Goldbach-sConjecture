#include "common.h"
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>

void report_and_exit(bool error_condition, char* report_name) {
    if (error_condition == true) {
      printf("An error occurred with ");
      printf("%s", report_name);
      assert(error_condition != false);
      exit(EXIT_FAILURE);
    }
}