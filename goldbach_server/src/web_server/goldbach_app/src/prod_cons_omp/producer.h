#ifndef producer_H
#define producer_H
#include "queue.h"
#include "dynamic_array.h"

/**
*@brief The producer make thread count work intervals for each number, and stores in queue 
*@param data ptr to Prod-Cons data
*/
void producer_start(dynamic_array_t* input_numbers, queue_t* queue, size_t consumer_count, int64_t** results);

#endif  // producer_H
