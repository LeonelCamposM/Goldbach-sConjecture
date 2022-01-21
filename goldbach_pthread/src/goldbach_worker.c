#include "dynamic_array.h"
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "goldbach_worker.h"

#define STARTVALUE 2

/**
 * @brief Generic function to report an error
 */
void report_and_exit(bool error_condition, char* report_name);

/**
* @return True if n is prime
*/
bool is_prime(int64_t n);

/**
*@brief print the sums of the strong goldbach conjecture 
*@details works with 64-bit positive integers > 5
*@param number to verify
*@return ptr to array made up of the addends found
*/
dynamic_array_t* strongConjecture(int64_t number);

/**
*@brief print the sums of the weak goldbach conjecture 
*@details works with 64-bit positive integers > 5
*@param number to verify
*@return ptr to array made up of the addends found
*/
dynamic_array_t* weakConjecture(int64_t number);

/**
*@brief show all addings stored in array
*@param array to print
*@param num_addings : number of addings
*@param sums : amount of sums 
*/
void show_addings(int64_t* array, int num_addings, int sums);

/**
*@brief gives the format to the output for the user
*@param array to print
*@param sums : amount of sums
*@param number being broken down
*@param list : true = list false = don't list
*@param num_addings : number of addings 
*/
void show_goldbach_results(dynamic_array_t* array, int sums, int64_t number, bool list, int num_addings);

/**
*@brief validate user input
*@param value input
*/
bool analize_arguments(int64_t value);

/**
*@brief get goldbach sums of a value
*@param value number 
*/
void get_goldbach_sums(int64_t value);



void report_and_exit(bool error_condition, char* report_name) {
    if (error_condition == true) {
      printf("An error occurred with ");
      printf("%s", report_name);
      assert(error_condition != false);
      exit(EXIT_FAILURE);
    }
}

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

dynamic_array_t* strong_conjecture(int64_t number) {
  // Create addings array
  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);
  report_and_exit (addings == NULL, "addings array\n");
  
  // Fill addings array
  for (int64_t first_adding = STARTVALUE; first_adding <=  number; first_adding++) {
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

dynamic_array_t* weak_conjecture(int64_t number) {
  // Create addings array
  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);
  report_and_exit (addings == NULL, "addings array\n");

  // Fill addings array
  for (int64_t first_adding = STARTVALUE; first_adding <=  number; first_adding++) {
    if (is_prime(first_adding)) {
      for (int64_t second_adding = first_adding; second_adding <=  number; second_adding++) {
        if (is_prime(second_adding)) {
          int64_t third_adding = number - first_adding - second_adding;
          bool valid_goldbach_sum = (is_prime(third_adding) && second_adding <= third_adding);
          if (valid_goldbach_sum) {
            array_append(addings, first_adding);
            array_append(addings, second_adding);
            array_append(addings, third_adding);
          }
        }
      }
    }
  }
  return addings;
}

int count(dynamic_array_t* array, int num_addings) {
  int sums = 0;
  size_t iterAddings = 0;
    while (iterAddings < array->count) {
      sums +=1;
      iterAddings += num_addings;
    }
  return sums;
}

void show_addings(int64_t* array, int num_addings, int sums){
  int64_t iterAddings = 0;
  while (iterAddings <= num_addings*sums-num_addings) {
    if (iterAddings != 0) {
      printf(", ");
    }
    printf("%" PRIi64 " + ", array[iterAddings]);
    if (num_addings == 3) {
      printf("%" PRIi64 " + ", array[iterAddings+1]);
      printf("%" PRIi64 , array[iterAddings+2]);
    } else {
        printf("%" PRIi64 , array[iterAddings+1]);
      }
    iterAddings+=num_addings;
  }
}

void show_goldbach_results(dynamic_array_t* array, int sums, int64_t num, bool list, int num_addings) {
  if (list == true) {
    printf("-");
    printf("%" PRIi64 ": ", num);
    printf("%i sums", sums);
    printf(": ");
    show_addings(array->elements, num_addings, sums);
  } 
  else {
    printf("%" PRIi64 ": ", num);
    printf("%i sums", sums);
  }
}

bool analize_arguments(int64_t value) {
  bool valid = false;
  bool invalid_input = (0 <= value && value <= 5) || (0 >= value && value >= -5);
  if (invalid_input) {
    printf("%" PRIi64 ": NA\n", value);
  }else{
    valid = true;
  } 
  return valid;
}

int64_t* get_goldbach_sums(int64_t value) {
  // list : true = list the sum, false = don't list the sums
  bool list = false;
  if (value < 0) {
    list = true;
    value *= -1;
  }

  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);

  int num_addings = 0;
  // Verify parity of the number
  if (value % 2 == 0) {
    num_addings = 2;
    addings = strong_conjecture(value);
  } else {
    num_addings = 3;
    addings = weak_conjecture(value);
  }

  return addings->elements;
}

int64_t* goldbach_worker_run(int64_t num, int64_t start, int64_t finish) {
  int64_t* results = get_goldbach_sums(value);
  return results;
}

int main(int argc, char* argv[]) {
  run();
  return EXIT_SUCCESS;
}