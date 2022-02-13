#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include "common.h"
#include "producer.h"
#define STARTVALUE 2

/**
*@brief return min number of two numbers
*@param num1 number 1
*@param num2 number 2
*@return min number 
*/
int64_t min_num(int64_t num1, int64_t num2);

/**
*@brief calculates the beginning of the interval where a goldbachWorker
* will look for sums 
*@details STARTVALUE = 2, used for avoid assign ranges that N/A
*@param value work for thread = goldbach num
*@param thread_count number of working threads 
*@param thread_id thread id number
*@return start of thread work 
*/
int64_t calc_start(int64_t value, int64_t thread_count, int64_t thread_id);

/**
*@brief calculates the end of the interval where a goldbachWorker
* will look for sums  
*@param value work for thread = goldbach num
*@param thread_count number of working threads 
*@param thread_id thread id number
*@return finish of thread work 
*/
int64_t calc_finish(int64_t value, int64_t thread_count, int64_t thread_id);

int64_t min_num(int64_t num1, int64_t num2) {
  int64_t result = 0;
  if (num1 < num2) {
    result = num1;
  } else {
    result = num2;
  }
  return result;
}

int64_t calc_start(int64_t value, int64_t thread_count, int64_t thread_id) {
  int64_t result = 0;
  if (STARTVALUE < thread_count) {
    // Equitable distribution of work for each worker
    int64_t work = thread_id * ( (value-STARTVALUE) / thread_count);
    // Assigns which worker has overload
    int64_t overload = min_num(thread_id, (value-STARTVALUE) % thread_count);
    result = work+overload;
  }else{
    // Equitable distribution of work for each worker
    int64_t work = thread_id * ( value / thread_count);
    // Assigns which worker has overload
    int64_t overload = min_num(thread_id, (value) % thread_count);
    result = work+overload;
  }
  return STARTVALUE + result;
}

int64_t calc_finish(int64_t value, int64_t thread_count, int64_t thread_id) {
  return calc_start(value, thread_count, thread_id + 1);
}

void producer_start(dynamic_array_t* input_numbers, queue_t* queue, size_t consumer_count, int64_t** resultsa) {
  for (size_t index = 0; index < input_numbers->count; index++) {
    int64_t value = input_numbers->elements[index];
    value = value > 0 ? value :  value * -1;

    for (size_t thread_id = 0; thread_id < consumer_count; thread_id++) {
      work_unit_t* new_work = (work_unit_t*)
        calloc(1, sizeof(work_unit_t));
      report_and_exit(new_work == NULL, "Could not create new_work");
      new_work->start = calc_start(value, consumer_count, thread_id);
      new_work->finish = calc_finish(value, consumer_count, thread_id);
      new_work->goldbach_number = value;
      new_work->results_id = consumer_count*index+thread_id;
      new_work->results = resultsa;
      queue_enqueue(queue, *new_work);
      free(new_work);
    }
  }
}
