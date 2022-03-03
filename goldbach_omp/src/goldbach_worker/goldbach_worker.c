#include "dynamic_array.h"
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "goldbach_worker.h"
#include "common.h"

/**
* @return True if n is prime
*/
bool is_prime(int64_t n);

/**
*@brief store in array the sums of the strong goldbach conjecture 
*@details works with 64-bit positive integers > 5
*@param num number of 64-bit positive integers
*@param start work start value for worker
*@param finish work finish value for worker
*@return ptr to array made up of the addends found
*/
dynamic_array_t* strongConjecture(int64_t number, int64_t start, int64_t finish);

/**
*@brief store in array the sums of the weak goldbach conjecture 
*@details works with 64-bit positive integers > 5
*@param num number of 64-bit positive integers
*@param start work start value for worker
*@param finish work finish value for worker
*@return ptr to array made up of the addends found
*/
dynamic_array_t* weakConjecture(int64_t number, int64_t start, int64_t finish);

/**
*@brief get goldbach sums of a value
*@param num number of 64-bit positive integers
*@param start work start value for worker
*@param finish work finish value for worker
*/
int64_t* get_goldbach_sums(int64_t number, int64_t start, int64_t finish);

bool is_prime(int64_t n) {
  bool signal = true;
  const int64_t max = sqrt(n);
  int64_t iter = 2;
  while (iter <= max) {
    if (n%iter == 0) {
      signal = false;
      break;
    }
  iter += 1;
  }
  return signal;
}

dynamic_array_t* strong_conjecture(int64_t number, int64_t start, int64_t finish) {
  // Create addings array
  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);
  report_and_exit (addings == NULL, "strong_conjecture");
  
  // Fill addings array
  for (int64_t first_adding = start; first_adding <  finish; first_adding++) {
    if (is_prime(first_adding)) {
      int64_t second_adding = number - first_adding;
      bool valid_goldbach_sum = (is_prime(second_adding) && first_adding <= second_adding);
      if (valid_goldbach_sum) {
        array_append(addings, first_adding);
        array_append(addings, second_adding);
      }
    }
  }
  return addings;
}

dynamic_array_t* weak_conjecture(int64_t number, int64_t start, int64_t finish) {
  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);
  report_and_exit (addings == NULL, "weak_conjecture");

  for (int64_t first_adding = start; first_adding <  finish; first_adding++) {
    if (is_prime(first_adding)) {
      for (int64_t second_adding = STARTVALUE; second_adding <=  number; second_adding++) {
        if (is_prime(second_adding)) {
          int64_t third_adding = number - first_adding - second_adding;
          if (is_prime(third_adding)) {
            if (first_adding <= second_adding && second_adding <= third_adding) {
              array_append(addings, first_adding);
              array_append(addings, second_adding);
              array_append(addings, third_adding);
            }
          }
        }
      }
    }
  }
  return addings;
}

int64_t* get_goldbach_sums(int64_t value, int64_t start, int64_t finish) {
  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);

  // Verify parity of the number
  if (value % 2 == 0) {
    addings = strong_conjecture(value, start, finish);
    array_append(addings,0);
    array_append(addings,0);
  } else {
    addings = weak_conjecture(value, start, finish);
    array_append(addings,0);
    array_append(addings,0);
    array_append(addings,0);
  }
  return addings->elements;
}

int64_t* goldbach_worker_run(int64_t num, int64_t start, int64_t finish) {
  int64_t* results = get_goldbach_sums(num, start, finish);
  return results;
}
