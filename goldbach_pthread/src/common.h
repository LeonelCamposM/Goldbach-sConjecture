#ifndef common_H
#define common_H
#include <stdbool.h>
#define STARTVALUE 2

/**
 * @brief Generic function to report an error
 */
void report_and_exit(bool error_condition, char* report_name);

#endif  // common_H