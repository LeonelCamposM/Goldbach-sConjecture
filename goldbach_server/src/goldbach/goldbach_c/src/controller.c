#include "input_handler.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>
#include <pthread.h>
#include <unistd.h>
#include "common.h"
#include "goldbach_worker.h"
#include "dynamic_array.h"
#include "prod_cons_omp.h"

int controller_run(int64_t goldbach_num);

void print_results(dynamic_array_t* input, int64_t** results,
  size_t thread_count);

/**
*@brief counts the number of sums in array
*@details counts the number of sums found in the array by iterating the 
* number of addings / Strong conjecture = 2, Weak conjecture = 3
*@param array array of addings to count
*@param num_addings : number of addings
*@return number of sums found in array
*/
int64_t count_array_sums(int64_t* array, int num_addings);

/**
*@brief show all addings stored in array
*@param array to print
*@param num_addings : number of addings
*@param sums : amount of sums 
*/
void show_array_addings(int64_t* array, int64_t sums,
    int64_t num_addings, bool first);

/**
*@brief free matrix results
*@param results ptr to matrix results
*@param thread_count number of working threads
*/
void free_results(int64_t** results, int64_t thread_count);

int controller_run(int64_t  goldbach_num) {
  int error = EXIT_SUCCESS;

  prod_cons_data_t* data = (prod_cons_data_t*)
    calloc(1, sizeof(prod_cons_data_t));
  report_and_exit(data == NULL, "Could not create producer consumer data");

  data->input_numbers = read_input();
  array_append(data->input_numbers, goldbach_num);

  data->threads = sysconf(_SC_NPROCESSORS_ONLN);

  //int64_t** results
  data->results = (int64_t**)
    calloc(data->threads*data->input_numbers->count, sizeof(int64_t*));
  report_and_exit(data->results == NULL, "could not create results array");

  data->results = prod_cons_omp_start(data, data->results);
  print_results(data->input_numbers, data->results, data->threads);
  free_results(data->results, data->threads);
  free(data);
  return error;
}

void print_results(dynamic_array_t* input, int64_t** results,
  size_t thread_count) {
  for (size_t inputIter = 0; inputIter < input->count; inputIter++) {
    // get nex number to be printed
    int64_t value = input->elements[inputIter];

    // Handle N/A Exceptions
    int valido = verify_input(value);

    if (valido == EXIT_SUCCESS) {
      // verify list
      bool list = false;
      if (value < 0) {
        value *= -1;
        list = true;
      }

      // Verify parity of the number
      int numAddings = 0;
      if (value % 2 == 0) {
        numAddings = 2;
      } else {
        numAddings = 3;
      }

      // calc start and finish positions of array
      size_t start = inputIter*thread_count;
      size_t finish = start + thread_count;

      //  count total amount of sums found
      bool first = true;
      int64_t sums = 0;
      for (size_t i = start; i < finish; i++) {
        sums += count_array_sums(results[i], numAddings);
      }

      //  print array stored in results[index]
      for (size_t index = start; index < finish; index++) {
        size_t thread_sums =
          count_array_sums(results[index], numAddings);

        //  list sums
        if (list == true) {
          // print format -value : x sums
          if (index == start) {
            write_output("-", 0, false);
            write_output("",value, true);
            write_output(": ", 0, false);
            write_output("", sums, true);
            write_output(" sums", 0, false);
            write_output(": ", 0, false);
          }
          // print array
          if (thread_sums != 0) {
            show_array_addings(results[index],
              thread_sums, numAddings, first);
            first = false;
          }
        } else {
          //  dont list sums
          if (index == start) {
            write_output("",value, true);
            write_output(": ", 0, false);
            write_output("", sums, true);
            write_output(" sums", 0, false);
            write_output(": ", 0, false);
          }
        }
      }
      write_output("\n",0, false);
    }
  }
}


int64_t count_array_sums(int64_t* array, int num_addings) {
  int64_t sums = 0;
  int64_t iterAddings = 0;
    int64_t num = array[iterAddings];
    while (num != 0) {
      sums +=1;
      iterAddings += num_addings;
      num = array[iterAddings];
    }
  return sums;
}

void show_array_addings(int64_t* array, int64_t sums,
    int64_t num_addings, bool first) {
  int64_t iterAddings = 0;
  while (iterAddings <= (num_addings*sums)-num_addings) {
    if (iterAddings != 0) {
      write_output(", ", 0, false);
    } else {
      if (!first) {
        write_output(", ", 0, false);
      }
    }
    write_output("", array[iterAddings],true);
    write_output(" + ", 0, false);
    if (num_addings == 3) {
      write_output("", array[iterAddings+1],true);
      write_output(" + ", 0, false);
      write_output("", array[iterAddings+2],true);
    } else {
      write_output("", array[iterAddings+1],true);
    }
    iterAddings+=num_addings;
  }
}

void free_results(int64_t** results, int64_t thread_count) {
  for (int64_t index = 0; index < thread_count; index++) {
    free(results[index]);
  }
  free(results);
}

int main(){
  return 0;
}