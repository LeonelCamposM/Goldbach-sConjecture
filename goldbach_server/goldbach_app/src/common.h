#ifndef common_H
#define common_H
#include <stdbool.h>
#define STARTVALUE 2
#include <inttypes.h>

typedef struct {
  int64_t start;
  int64_t finish;
  int64_t goldbach_number;
  int64_t results_id;
  int64_t** results;
} work_unit_t;

/**
 * @brief Generic function to report an error
 */
void report_and_exit(bool error_condition, char* report_name);

#endif  // common_H