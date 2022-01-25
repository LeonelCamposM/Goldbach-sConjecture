#ifndef prod_cons_omp_H
#define prod_cons_omp_H
#include "dynamic_array.h"
#include <math.h>


typedef struct {
} prod_cons_omp_t;

typedef struct {
    dynamic_array_t* input_numbers;
    size_t threads;
    int64_t** results;
} prod_cons_data_t;


int64_t** prod_cons_omp_start(prod_cons_data_t* data, int64_t** results);

#endif  // prod_cons_omp_H